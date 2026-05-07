"""
Financial management models.
Handles offerings, donations, and financial categories.
"""

from datetime import datetime
from .user import db


class FinancialCategory(db.Model):
    """
    Financial category for categorizing offerings and donations.
    
    Attributes:
        id: Unique identifier
        name: Category name (e.g., "General Offering", "Building Fund", "Missions")
        description: Description of the category
        created_at: Creation timestamp
        updated_at: Last update timestamp
        
    Relationships:
        offerings: One-to-many with Offering
    """
    __tablename__ = 'financial_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    offerings = db.relationship('Offering', backref='category', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<FinancialCategory {self.name}>'
    
    def get_total_offerings(self, start_date=None, end_date=None):
        """
        Get total offerings in this category.
        
        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            float: Total amount
        """
        query = self.offerings
        
        if start_date:
            query = query.filter(Offering.date >= start_date)
        if end_date:
            query = query.filter(Offering.date <= end_date)
        
        total = db.session.query(db.func.sum(Offering.amount)).filter(
            Offering.category_id == self.id
        )
        if start_date:
            total = total.filter(Offering.date >= start_date)
        if end_date:
            total = total.filter(Offering.date <= end_date)
        
        result = total.scalar()
        return float(result) if result else 0.0
    
    def get_offering_count(self, start_date=None, end_date=None):
        """Get count of offerings in this category."""
        query = self.offerings
        
        if start_date:
            query = query.filter(Offering.date >= start_date)
        if end_date:
            query = query.filter(Offering.date <= end_date)
        
        return query.count()
    
    def to_dict(self, include_offerings=False):
        """Convert category to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
        }


class Offering(db.Model):
    """
    Offering or donation record.
    
    Attributes:
        id: Unique identifier
        amount: Offering amount
        date: Date of offering
        category_id: Foreign key to FinancialCategory
        member_id: Optional foreign key to Member (if identified)
        is_anonymous: Whether offering is anonymous
        payment_method: How payment was made (cash, check, card, etc.)
        reference_number: Check number, transaction ID, etc.
        notes: Additional notes
        created_at: Creation timestamp
        updated_at: Last update timestamp
        
    Relationships:
        category: Relationship to FinancialCategory
        member: Relationship to Member
    """
    __tablename__ = 'offerings'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('financial_categories.id'), nullable=False, index=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=True, index=True)
    received_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.String(50), nullable=True)  # cash, check, card, transfer
    reference_number = db.Column(db.String(100), nullable=True)  # Check #, transaction ID
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to User (staff member who received the offering)
    received_by = db.relationship('User', backref='offerings_received')
    
    def __repr__(self):
        return f'<Offering ${float(self.amount):.2f} - {self.date}>'
    
    def get_donor_name(self):
        """Get donor name or 'Anonymous'."""
        if self.is_anonymous:
            return "Anonymous"
        if self.member_id and self.member:
            return self.member.get_full_name()
        return "Unknown"
    
    def get_staff_name(self):
        """Get name of staff member who received this offering."""
        if self.received_by:
            return f"{self.received_by.first_name} {self.received_by.last_name}".strip()
        return "Unknown"
    
    def to_dict(self):
        """Convert offering to dictionary."""
        return {
            'id': self.id,
            'amount': float(self.amount),
            'date': self.date.isoformat(),
            'category': self.category.name if self.category else None,
            'member_id': self.member_id,
            'donor_name': self.get_donor_name(),
            'is_anonymous': self.is_anonymous,
            'payment_method': self.payment_method,
            'reference_number': self.reference_number,
            'received_by_user_id': self.received_by_user_id,
            'received_by_staff': self.get_staff_name(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
        }
