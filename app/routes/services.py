"""
Services and attendance routes and views.
Handles service CRUD operations and attendance tracking.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import datetime
from app.models.user import db
from app.models.service import Service, Attendance, ServiceType
from app.models.member import Member
from app.forms import ServiceForm, AttendanceForm
from app.utils import staff_required, paginate_query, commit_changes

services_bp = Blueprint('services', __name__, url_prefix='/services')


@services_bp.route('/')
@login_required
def list_services():
    """List all services."""
    page = request.args.get('page', 1, type=int)
    
    query = Service.query.order_by(Service.date.desc())
    items, total, pages = paginate_query(query, page, per_page=20)
    
    return render_template(
        'services/list.html',
        services=items,
        total=total,
        pages=pages,
        current_page=page
    )


@services_bp.route('/<int:service_id>')
@login_required
def view_service(service_id):
    """View service details and attendance."""
    service = Service.query.get_or_404(service_id)
    
    # Get attendance records
    attendance_records = service.attendance_records.all()
    
    return render_template(
        'services/detail.html',
        service=service,
        attendance_records=attendance_records
    )


@services_bp.route('/new', methods=['GET', 'POST'])
@staff_required
def create_service():
    """Create a new service."""
    form = ServiceForm()
    
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            service_type=ServiceType[form.service_type.data.upper()],
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            location=form.location.data,
            notes=form.notes.data,
        )
        
        db.session.add(service)
        db.session.flush()  # Get service ID
        
        # Auto-create attendance records for all active members
        active_members = Member.query.filter_by(status='active').all()
        for member in active_members:
            attendance = Attendance(
                member_id=member.id,
                service_id=service.id,
                attended=False
            )
            db.session.add(attendance)
        
        success, message = commit_changes('Service created successfully')
        
        if success:
            flash(message, 'success')
            return redirect(url_for('services.view_service', service_id=service.id))
        else:
            flash(message, 'danger')
    
    return render_template('services/form.html', form=form, service=None)


@services_bp.route('/<int:service_id>/edit', methods=['GET', 'POST'])
@staff_required
def edit_service(service_id):
    """Edit service."""
    service = Service.query.get_or_404(service_id)
    form = ServiceForm()
    
    if form.validate_on_submit():
        service.name = form.name.data
        service.service_type = ServiceType[form.service_type.data.upper()]
        service.date = form.date.data
        service.start_time = form.start_time.data
        service.end_time = form.end_time.data
        service.location = form.location.data
        service.notes = form.notes.data
        
        success, message = commit_changes('Service updated successfully')
        
        if success:
            flash(message, 'success')
            return redirect(url_for('services.view_service', service_id=service.id))
        else:
            flash(message, 'danger')
    
    elif request.method == 'GET':
        form.name.data = service.name
        form.service_type.data = service.service_type.value
        form.date.data = service.date
        form.start_time.data = service.start_time
        form.end_time.data = service.end_time
        form.location.data = service.location
        form.notes.data = service.notes
    
    return render_template('services/form.html', form=form, service=service)


@services_bp.route('/<int:service_id>/delete', methods=['POST'])
@staff_required
def delete_service(service_id):
    """Delete service."""
    service = Service.query.get_or_404(service_id)
    name = service.name
    
    db.session.delete(service)
    success, message = commit_changes('Service deleted successfully')
    
    if success:
        flash(f'{name} has been deleted.', 'success')
    else:
        flash(f'Error deleting service: {message}', 'danger')
    
    return redirect(url_for('services.list_services'))


@services_bp.route('/<int:service_id>/attendance', methods=['GET', 'POST'])
@staff_required
def attendance(service_id):
    """Record attendance for a service."""
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'POST':
        # Process attendance updates
        attendance_data = request.form.getlist('member_id')
        
        for member_id in attendance_data:
            att = Attendance.query.filter_by(
                member_id=member_id,
                service_id=service_id
            ).first()
            
            if att:
                att.attended = True
        
        success, message = commit_changes('Attendance recorded successfully')
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'danger')
    
    # Get attendance records
    attendance_records = service.attendance_records.all()
    
    return render_template(
        'services/attendance.html',
        service=service,
        attendance_records=attendance_records
    )
