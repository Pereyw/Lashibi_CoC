"""
Members management routes and views.
Handles member CRUD operations, search, and ministry group management.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.user import db
from app.models.member import Member, MemberStatus, MemberGroup
from app.forms import MemberForm, MemberSearchForm
from app.utils import staff_required, paginate_query, commit_changes

members_bp = Blueprint('members', __name__, url_prefix='/members')


@members_bp.route('/')
@login_required
def list_members():
    """List all members with search and filter."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    
    query = Member.query
    
    # Apply search filter
    if search_query:
        query = query.filter(
            (Member.first_name.ilike(f'%{search_query}%')) |
            (Member.last_name.ilike(f'%{search_query}%')) |
            (Member.email.ilike(f'%{search_query}%'))
        )
    
    # Apply status filter
    if status_filter:
        try:
            status = MemberStatus[status_filter.upper()]
            query = query.filter_by(status=status)
        except KeyError:
            pass
    
    # Sort by name
    query = query.order_by(Member.last_name, Member.first_name)
    
    items, total, pages = paginate_query(query, page, per_page=20)
    
    return render_template(
        'members/list.html',
        members=items,
        total=total,
        pages=pages,
        current_page=page,
        search_query=search_query,
        status_filter=status_filter
    )


@members_bp.route('/<int:member_id>')
@login_required
def view_member(member_id):
    """View member details."""
    member = Member.query.get_or_404(member_id)
    
    # Get attendance statistics
    attendance_count = member.get_attendance_count()
    total_offerings = member.get_total_offerings()
    
    return render_template(
        'members/detail.html',
        member=member,
        attendance_count=attendance_count,
        total_offerings=total_offerings
    )


@members_bp.route('/new', methods=['GET', 'POST'])
@staff_required
def create_member():
    """Create a new member."""
    form = MemberForm()
    
    if form.validate_on_submit():
        member = Member(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            date_of_birth=form.date_of_birth.data,
            baptism_date=form.baptism_date.data,
            gender=form.gender.data,
            status=MemberStatus[form.status.data.upper()],
            notes=form.notes.data,
        )
        
        db.session.add(member)
        success, message = commit_changes('Member created successfully')
        
        if success:
            flash(message, 'success')
            return redirect(url_for('members.view_member', member_id=member.id))
        else:
            flash(message, 'danger')
    
    return render_template('members/form.html', form=form, member=None)


@members_bp.route('/<int:member_id>/edit', methods=['GET', 'POST'])
@staff_required
def edit_member(member_id):
    """Edit member details."""
    member = Member.query.get_or_404(member_id)
    form = MemberForm()
    
    if form.validate_on_submit():
        member.first_name = form.first_name.data
        member.last_name = form.last_name.data
        member.email = form.email.data
        member.phone = form.phone.data
        member.address = form.address.data
        member.city = form.city.data
        member.state = form.state.data
        member.zip_code = form.zip_code.data
        member.date_of_birth = form.date_of_birth.data
        member.baptism_date = form.baptism_date.data
        member.gender = form.gender.data
        member.status = MemberStatus[form.status.data.upper()]
        member.notes = form.notes.data
        
        success, message = commit_changes('Member updated successfully')
        
        if success:
            flash(message, 'success')
            return redirect(url_for('members.view_member', member_id=member.id))
        else:
            flash(message, 'danger')
    
    elif request.method == 'GET':
        form.first_name.data = member.first_name
        form.last_name.data = member.last_name
        form.email.data = member.email
        form.phone.data = member.phone
        form.address.data = member.address
        form.city.data = member.city
        form.state.data = member.state
        form.zip_code.data = member.zip_code
        form.baptism_date.data = member.baptism_date
        form.date_of_birth.data = member.date_of_birth
        form.gender.data = member.gender
        form.status.data = member.status.value
        form.notes.data = member.notes
    
    return render_template('members/form.html', form=form, member=member)


@members_bp.route('/<int:member_id>/delete', methods=['POST'])
@staff_required
def delete_member(member_id):
    """Delete member."""
    member = Member.query.get_or_404(member_id)
    name = member.get_full_name()
    
    db.session.delete(member)
    success, message = commit_changes('Member deleted successfully')
    
    if success:
        flash(f'{name} has been deleted.', 'success')
    else:
        flash(f'Error deleting member: {message}', 'danger')
    
    return redirect(url_for('members.list_members'))


@members_bp.route('/groups')
@login_required
def list_groups():
    """List ministry groups."""
    groups = MemberGroup.query.all()
    return render_template('members/groups.html', groups=groups)


@members_bp.route('/groups/new', methods=['GET', 'POST'])
@staff_required
def create_group():
    """Create a new ministry group."""
    if request.method == 'POST':
        group = MemberGroup(
            name=request.form.get('name'),
            description=request.form.get('description'),
            leader_name=request.form.get('leader_name'),
        )
        
        db.session.add(group)
        success, message = commit_changes('Group created successfully')
        
        if success:
            flash(message, 'success')
            return redirect(url_for('members.list_groups'))
        else:
            flash(message, 'danger')
    
    return render_template('members/group_form.html', group=None)
