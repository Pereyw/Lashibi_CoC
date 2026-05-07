"""
Member and membership management models.
Handles member profiles, contact information, and ministry group assignments.
"""

from datetime import datetime
from enum import Enum
from .user import db


class MemberStatus(Enum):
    """Membership status enumeration."""
    ACTIVE = "active"          # Regular active member
    INACTIVE = "inactive"      # Inactive member (not attending)
    VISITOR = "visitor"        # Visiting member
    TRANSFERRED = "transferred"  # Transferred to another church
    DECEASED = "deceased"      # Deceased member


class Member(db.Model):
    """
    Member model for church membership records.
    
    Attributes:
        id: Unique identifier
        first_name: Member's first name
        last_name: Member's last name
        email: Member's email address
        phone: Member's phone number
        address: Residential address
        city: City of residence
        state: State of residence
        zip_code: Postal code
        date_of_birth: Member's date of birth
        gender: Member's gender (M/F/Other)
        status: Membership status
        join_date: Date member joined
        notes: Additional notes about member
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        
    Relationships:
        groups: Many-to-many relationship with MemberGroup
        attendance_records: One-to-many with Attendance
        offerings: One-to-many with Offering
    """
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False, index=True)
    last_name = db.Column(db.String(120), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)  # M, F, Other
    status = db.Column(db.Enum(MemberStatus), nullable=False, default=MemberStatus.ACTIVE, index=True)
    join_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    baptism_date = db.Column(db.Date, nullable=True, index=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    groups = db.relationship(
        'MemberGroup',
        secondary='member_group_association',
        backref=db.backref('members', lazy='dynamic')
    )
    attendance_records = db.relationship('Attendance', backref='member', lazy='dynamic', cascade='all, delete-orphan')
    offerings = db.relationship('Offering', backref='member', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Member {self.get_full_name()}>'
    
    def get_full_name(self):
        """Get member's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_age(self):
        """Calculate member's age based on date of birth."""
        if not self.date_of_birth:
            return None
        today = datetime.utcnow().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def is_active_member(self):
        """Check if member is active."""
        return self.status == MemberStatus.ACTIVE
    
    def is_baptized(self):
        """Check if member has baptism date recorded."""
        return self.baptism_date is not None
    
    def get_years_since_baptism(self):
        """Calculate years since baptism if date exists."""
        if not self.baptism_date:
            return None
        today = datetime.utcnow().date()
        return today.year - self.baptism_date.year - (
            (today.month, today.day) < (self.baptism_date.month, self.baptism_date.day)
        )
    
    def get_attendance_count(self, start_date=None, end_date=None):
        """
        Get count of services attended.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            int: Number of services attended
        """
        query = self.attendance_records.filter_by(attended=True)
        
        if start_date:
            query = query.filter(Attendance.service.has(Service.date >= start_date))
        if end_date:
            query = query.filter(Attendance.service.has(Service.date <= end_date))
        
        return query.count()
    
    def get_total_offerings(self, start_date=None, end_date=None):
        """
        Get total offerings by this member.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            float: Total offering amount
        """
        from .financial import Offering
        query = self.offerings
        
        if start_date:
            query = query.filter(Offering.date >= start_date)
        if end_date:
            query = query.filter(Offering.date <= end_date)
        
        total = db.session.query(db.func.sum(Offering.amount)).filter(
            Offering.member_id == self.id
        )
        if start_date:
            total = total.filter(Offering.date >= start_date)
        if end_date:
            total = total.filter(Offering.date <= end_date)
        
        result = total.scalar()
        return float(result) if result else 0.0
    
    def to_dict(self):
        """Convert member to dictionary."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'baptism_date': self.baptism_date.isoformat() if self.baptism_date else None,
            'is_baptized': self.is_baptized(),
            'years_since_baptism': self.get_years_since_baptism(),
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.get_age(),
            'gender': self.gender,
            'status': self.status.value,
            'join_date': self.join_date.isoformat(),
            'groups': [g.name for g in self.groups],
            'created_at': self.created_at.isoformat(),
        }


class MemberGroup(db.Model):
    """
    Ministry groups or teams that members can join.
    
    Attributes:
        id: Unique identifier
        name: Group name (e.g., "Worship Team", "Ushers", "Children's Ministry")
        description: Description of the group's purpose
        leader_name: Name of the group leader
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = 'member_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    leader_name = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MemberGroup {self.name}>'
    
    def get_member_count(self):
        """Get number of members in this group."""
        return self.members.count()
    
    def to_dict(self):
        """Convert group to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'leader_name': self.leader_name,
            'member_count': self.get_member_count(),
            'created_at': self.created_at.isoformat(),
        }


class MemberGroupAssociation(db.Model):
    """
    Association table for many-to-many relationship between Members and Groups.
    """
    __tablename__ = 'member_group_association'
    
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('member_groups.id'), primary_key=True)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MemberGroupAssociation member_id={self.member_id}, group_id={self.group_id}>'


# Import at end to avoid circular imports
from .service import Attendance, Service
