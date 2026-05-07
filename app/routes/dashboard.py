"""
Dashboard routes and views.
Displays KPIs and key metrics.
"""

from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models.user import db
from app.models.member import Member, MemberStatus
from app.models.service import Service, Attendance
from app.models.financial import Offering
from app.models.inventory import InventoryItem
from app.utils import get_date_range, calculate_percentage

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard view with KPIs."""
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)
    
    # Member metrics
    total_members = Member.query.count()
    active_members = Member.query.filter_by(status=MemberStatus.ACTIVE).count()
    new_members_this_month = Member.query.filter(
        Member.join_date >= month_start
    ).count()
    
    # Service metrics
    total_services = Service.query.count()
    services_this_month = Service.query.filter(
        Service.date >= month_start
    ).count()
    
    # Get total attendance and calculate rate
    total_attendance_records = Attendance.query.count()
    attended_records = Attendance.query.filter_by(attended=True).count()
    attendance_rate = calculate_percentage(attended_records, total_attendance_records)
    
    # Financial metrics
    total_offerings = db.session.query(func.sum(Offering.amount)).scalar() or 0
    offerings_this_month = db.session.query(func.sum(Offering.amount)).filter(
        Offering.date >= month_start
    ).scalar() or 0
    offering_count = Offering.query.count()
    
    # Inventory metrics
    total_items = InventoryItem.query.filter_by(is_active=True).count()
    low_stock_items = InventoryItem.query.filter(
        InventoryItem.quantity <= InventoryItem.reorder_level
    ).count()
    
    # Calculate total inventory value
    inventory_value = db.session.query(
        func.sum(InventoryItem.quantity * InventoryItem.unit_cost)
    ).scalar() or 0
    
    # Get recent activity
    recent_offerings = Offering.query.order_by(Offering.date.desc()).limit(5).all()
    recent_services = Service.query.order_by(Service.date.desc()).limit(5).all()
    recent_members = Member.query.order_by(Member.created_at.desc()).limit(5).all()
    
    return render_template(
        'dashboard/index.html',
        # Members
        total_members=total_members,
        active_members=active_members,
        new_members_this_month=new_members_this_month,
        # Services
        total_services=total_services,
        services_this_month=services_this_month,
        attendance_rate=attendance_rate,
        # Financial
        total_offerings=float(total_offerings),
        offerings_this_month=float(offerings_this_month),
        offering_count=offering_count,
        # Inventory
        total_items=total_items,
        low_stock_items=low_stock_items,
        inventory_value=float(inventory_value),
        # Recent activity
        recent_offerings=recent_offerings,
        recent_services=recent_services,
        recent_members=recent_members,
    )


@dashboard_bp.route('/reports')
@login_required
def reports():
    """Advanced reports and analytics."""
    # Attendance trends by month
    today = datetime.utcnow().date()
    
    # Last 12 months data
    attendance_by_month = []
    for i in range(11, -1, -1):
        month_date = today - timedelta(days=30*i)
        month_start = month_date.replace(day=1)
        
        if i > 0:
            month_end = (month_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        else:
            month_end = today
        
        services = Service.query.filter(
            (Service.date >= month_start) & (Service.date <= month_end)
        ).count()
        
        attendance_records = Attendance.query.join(Service).filter(
            (Service.date >= month_start) & (Service.date <= month_end) & (Attendance.attended == True)
        ).count()
        
        attendance_by_month.append({
            'month': month_start.strftime('%B'),
            'services': services,
            'attendance': attendance_records,
        })
    
    return render_template(
        'dashboard/reports.html',
        attendance_by_month=attendance_by_month,
    )
