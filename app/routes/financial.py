"""
Financial management routes and views.
Handles offerings, donations, and financial reports.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models.user import db
from app.models.financial import FinancialCategory, Offering
from app.models.member import Member
from app.forms import FinancialCategoryForm, OfferingForm, OfferingSearchForm
from app.utils import staff_required, admin_required, paginate_query, commit_changes, get_date_range

financial_bp = Blueprint('financial', __name__, url_prefix='/financial')


@financial_bp.route('/')
@login_required
def index():
    """Financial management dashboard."""
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)
    
    # Calculate totals
    total_offerings_month = db.session.query(func.sum(Offering.amount)).filter(
        Offering.date >= month_start
    ).scalar() or 0
    
    total_offerings_all = db.session.query(func.sum(Offering.amount)).scalar() or 0
    
    offering_count_month = Offering.query.filter(
        Offering.date >= month_start
    ).count()
    
    categories = FinancialCategory.query.all()
    
    return render_template(
        'financial/index.html',
        total_offerings_month=float(total_offerings_month),
        total_offerings_all=float(total_offerings_all),
        offering_count_month=offering_count_month,
        categories=categories
    )


@financial_bp.route('/offerings')
@login_required
def list_offerings():
    """List offerings with filter and search."""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Offering.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if start_date:
        try:
            start_date_obj = datetime.fromisoformat(start_date).date()
            query = query.filter(Offering.date >= start_date_obj)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date_obj = datetime.fromisoformat(end_date).date()
            query = query.filter(Offering.date <= end_date_obj)
        except ValueError:
            pass
    
    query = query.order_by(Offering.date.desc())
    items, total, pages = paginate_query(query, page, per_page=20)
    
    categories = FinancialCategory.query.all()
    
    return render_template(
        'financial/offerings.html',
        offerings=items,
        total=total,
        pages=pages,
        current_page=page,
        categories=categories,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date
    )


@financial_bp.route('/offerings/new', methods=['GET', 'POST'])
@staff_required
def create_offering():
    """Create a new offering record."""
    form = OfferingForm()
    
    if form.validate_on_submit():
        offering = Offering(
            amount=form.amount.data,
            date=form.date.data,
            category_id=form.category_id.data,
            member_id=form.member_id.data if form.member_id.data != 0 else None,
            received_by_user_id=form.received_by_user_id.data,
            is_anonymous=form.is_anonymous.data,
            payment_method=form.payment_method.data,
            reference_number=form.reference_number.data,
            notes=form.notes.data,
        )
        
        db.session.add(offering)
        success, message = commit_changes('Offering recorded successfully')
        
        if success:
            flash(message, 'success')
            return redirect(url_for('financial.list_offerings'))
        else:
            flash(message, 'danger')
    
    return render_template('financial/offering_form.html', form=form)


@financial_bp.route('/offerings/<int:offering_id>/delete', methods=['POST'])
@staff_required
def delete_offering(offering_id):
    """Delete an offering record."""
    offering = Offering.query.get_or_404(offering_id)
    
    db.session.delete(offering)
    success, message = commit_changes('Offering deleted successfully')
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('financial.list_offerings'))


@financial_bp.route('/categories')
@login_required
def list_categories():
    """List financial categories."""
    categories = FinancialCategory.query.all()
    return render_template('financial/categories.html', categories=categories)


@financial_bp.route('/categories/new', methods=['GET', 'POST'])
@staff_required
def create_category():
    """Create a new financial category."""
    form = FinancialCategoryForm()
    
    if form.validate_on_submit():
        category = FinancialCategory(
            name=form.name.data,
            description=form.description.data,
        )
        
        db.session.add(category)
        success, message = commit_changes('Category created successfully')
        
        if success:
            flash(message, 'success')
            return redirect(url_for('financial.list_categories'))
        else:
            flash(message, 'danger')
    
    return render_template('financial/category_form.html', form=form, category=None)


@financial_bp.route('/reports')
@login_required
def reports():
    """Financial reports and summaries."""
    today = datetime.utcnow().date()
    
    # Get data for different periods
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    
    # This month offerings by category
    this_month_data = db.session.query(
        FinancialCategory.name,
        func.sum(Offering.amount).label('total')
    ).join(Offering).filter(
        Offering.date >= this_month_start
    ).group_by(FinancialCategory.name).all()
    
    # All time data
    all_time_data = db.session.query(
        FinancialCategory.name,
        func.sum(Offering.amount).label('total')
    ).join(Offering).group_by(FinancialCategory.name).all()
    
    return render_template(
        'financial/reports.html',
        this_month_data=this_month_data,
        all_time_data=all_time_data
    )
