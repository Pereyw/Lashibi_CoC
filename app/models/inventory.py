"""
Inventory management models.
Handles inventory items, stock levels, and transaction tracking.
"""

from datetime import datetime
from enum import Enum
from .user import db


class TransactionType(Enum):
    """Types of inventory transactions."""
    IN = "in"           # Stock received/purchased
    OUT = "out"         # Stock used/donated out
    ADJUSTMENT = "adjustment"  # Inventory adjustment/correction


class InventoryItem(db.Model):
    """
    Inventory item model.
    
    Attributes:
        id: Unique identifier
        name: Item name
        description: Item description
        category: Item category (supplies, equipment, etc.)
        quantity: Current stock quantity
        unit: Unit of measurement (pieces, boxes, liters, etc.)
        unit_cost: Cost per unit
        reorder_level: Minimum stock level before reorder
        reorder_quantity: Quantity to order when restocking
        supplier: Supplier name
        location: Storage location in church
        notes: Additional notes
        is_active: Whether item is actively tracked
        created_at: Creation timestamp
        updated_at: Last update timestamp
        
    Relationships:
        transactions: One-to-many with InventoryTransaction
    """
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(120), nullable=True, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=0, index=True)
    unit = db.Column(db.String(50), nullable=True)  # pieces, boxes, liters, etc.
    unit_cost = db.Column(db.Numeric(10, 2), nullable=True, default=0)
    reorder_level = db.Column(db.Integer, nullable=False, default=10)
    reorder_quantity = db.Column(db.Integer, nullable=False, default=50)
    supplier = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('InventoryTransaction', backref='item', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<InventoryItem {self.name} - Qty: {self.quantity}>'
    
    def is_low_stock(self):
        """Check if item is below reorder level."""
        return self.quantity <= self.reorder_level
    
    def get_stock_value(self):
        """Get total value of stock on hand."""
        if not self.unit_cost:
            return 0.0
        return float(self.quantity * self.unit_cost)
    
    def add_stock(self, quantity, notes="", transaction_type=TransactionType.IN):
        """
        Add stock to inventory.
        
        Args:
            quantity: Number of units to add
            notes: Notes about the addition
            transaction_type: Type of transaction
            
        Raises:
            ValueError: If quantity is invalid
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        self.quantity += quantity
        db.session.add(
            InventoryTransaction(
                item_id=self.id,
                transaction_type=transaction_type,
                quantity=quantity,
                notes=notes,
            )
        )
        self.updated_at = datetime.utcnow()
    
    def remove_stock(self, quantity, notes=""):
        """
        Remove stock from inventory.
        
        Args:
            quantity: Number of units to remove
            notes: Notes about the removal
            
        Raises:
            ValueError: If quantity is invalid or exceeds available stock
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.quantity - quantity < 0:
            raise ValueError(f"Insufficient stock. Available: {self.quantity}, Requested: {quantity}")
        
        self.quantity -= quantity
        db.session.add(
            InventoryTransaction(
                item_id=self.id,
                transaction_type=TransactionType.OUT,
                quantity=quantity,
                notes=notes,
            )
        )
        self.updated_at = datetime.utcnow()
    
    def adjust_stock(self, new_quantity, reason=""):
        """
        Adjust stock to specific quantity (for corrections).
        
        Args:
            new_quantity: New stock quantity
            reason: Reason for adjustment
        """
        difference = new_quantity - self.quantity
        if difference > 0:
            self.add_stock(difference, f"Adjustment: {reason}", TransactionType.ADJUSTMENT)
        elif difference < 0:
            self.remove_stock(abs(difference), f"Adjustment: {reason}")
    
    def get_transaction_history(self, limit=10):
        """Get recent transactions for this item."""
        return self.transactions.order_by(InventoryTransaction.date.desc()).limit(limit).all()
    
    def to_dict(self):
        """Convert item to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'quantity': self.quantity,
            'unit': self.unit,
            'unit_cost': float(self.unit_cost) if self.unit_cost else 0,
            'stock_value': self.get_stock_value(),
            'reorder_level': self.reorder_level,
            'is_low_stock': self.is_low_stock(),
            'supplier': self.supplier,
            'location': self.location,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }


class InventoryTransaction(db.Model):
    """
    Inventory transaction log.
    Records all stock movements for audit purposes.
    
    Attributes:
        id: Unique identifier
        item_id: Foreign key to InventoryItem
        transaction_type: Type of transaction (IN, OUT, ADJUSTMENT)
        quantity: Quantity involved
        date: Transaction date/time
        notes: Notes about transaction
        created_at: Creation timestamp
        
    Relationships:
        item: Relationship to InventoryItem
    """
    __tablename__ = 'inventory_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False, index=True)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<InventoryTransaction {self.transaction_type.value} - {self.quantity} - {self.date}>'
    
    def to_dict(self):
        """Convert transaction to dictionary."""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item_name': self.item.name if self.item else None,
            'transaction_type': self.transaction_type.value,
            'quantity': self.quantity,
            'date': self.date.isoformat(),
            'notes': self.notes,
        }
