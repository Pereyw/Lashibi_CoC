"""
Service and attendance tracking models.
Handles church services/events and member attendance records.
"""

from datetime import datetime
from enum import Enum
from .user import db


class ServiceType(Enum):
    """Types of services and events."""
    SUNDAY_WORSHIP = "sunday_worship"
    MIDWEEK_SERVICE = "midweek_service"
    PRAYER_MEETING = "prayer_meeting"
    BIBLE_STUDY = "bible_study"
    SMALL_GROUP = "small_group"
    SPECIAL_EVENT = "special_event"
    TRAINING = "training"
    CONFERENCE = "conference"


class Service(db.Model):
    """
    Service or event model.
    
    Attributes:
        id: Unique identifier
        name: Service name/title
        service_type: Type of service
        date: Date of the service
        start_time: Start time
        end_time: End time
        location: Location where service is held
        notes: Additional notes about the service
        created_at: Creation timestamp
        updated_at: Last update timestamp
        
    Relationships:
        attendance_records: One-to-many with Attendance
    """
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    service_type = db.Column(db.Enum(ServiceType), nullable=False, default=ServiceType.SUNDAY_WORSHIP)
    date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendance_records = db.relationship('Attendance', backref='service', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Service {self.name} - {self.date}>'
    
    def get_attendance_count(self):
        """Get count of members who attended this service."""
        return self.attendance_records.filter_by(attended=True).count()
    
    def get_registered_count(self):
        """Get total number of members registered for this service."""
        return self.attendance_records.count()
    
    def get_attendance_rate(self):
        """Calculate attendance rate as percentage."""
        registered = self.get_registered_count()
        if registered == 0:
            return 0
        attended = self.get_attendance_count()
        return round((attended / registered) * 100, 2)
    
    def to_dict(self):
        """Convert service to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'service_type': self.service_type.value,
            'date': self.date.isoformat(),
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'location': self.location,
            'notes': self.notes,
            'attendance_count': self.get_attendance_count(),
            'registered_count': self.get_registered_count(),
            'attendance_rate': self.get_attendance_rate(),
            'created_at': self.created_at.isoformat(),
        }


class Attendance(db.Model):
    """
    Attendance tracking model.
    Links members to services they attended.
    
    Attributes:
        id: Unique identifier
        member_id: Foreign key to Member
        service_id: Foreign key to Service
        attended: Whether member attended (boolean)
        notes: Additional notes (e.g., excused absence)
        recorded_at: Timestamp when attendance was recorded
        
    Relationships:
        member: Relationship to Member
        service: Relationship to Service
    """
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, index=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False, index=True)
    attended = db.Column(db.Boolean, default=False, index=True)
    notes = db.Column(db.String(255), nullable=True)  # e.g., "Excused", "Guest"
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Composite index for efficient queries
    __table_args__ = (
        db.UniqueConstraint('member_id', 'service_id', name='unique_member_service'),
    )
    
    def __repr__(self):
        return f'<Attendance member_id={self.member_id}, service_id={self.service_id}>'
    
    def to_dict(self):
        """Convert attendance to dictionary."""
        return {
            'id': self.id,
            'member_id': self.member_id,
            'service_id': self.service_id,
            'attended': self.attended,
            'notes': self.notes,
            'recorded_at': self.recorded_at.isoformat(),
        }
