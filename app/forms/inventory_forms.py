"""
Inventory management forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length
from app.models.inventory import TransactionType
from app.utils.validators import validate_positive_number


class InventoryItemForm(FlaskForm):
    """Form to create/edit inventory items."""
    name = StringField('Item Name', validators=[
        DataRequired(),
        Length(min=2, max=255)
    ])
    description = TextAreaField('Description', validators=[Optional()])
    category = StringField('Category', validators=[Optional(), Length(max=120)])
    quantity = IntegerField('Current Quantity', validators=[
        DataRequired(),
        validate_positive_number('Quantity must be positive')
    ])
    unit = StringField('Unit of Measurement', validators=[
        Optional(),
        Length(max=50)
    ])
    unit_cost = DecimalField('Unit Cost', places=2, validators=[
        Optional(),
        validate_positive_number('Cost must be positive')
    ])
    reorder_level = IntegerField('Reorder Level', validators=[
        DataRequired(),
        validate_positive_number('Reorder level must be positive')
    ])
    reorder_quantity = IntegerField('Reorder Quantity', validators=[
        DataRequired(),
        validate_positive_number('Reorder quantity must be positive')
    ])
    supplier = StringField('Supplier', validators=[Optional(), Length(max=120)])
    location = StringField('Storage Location', validators=[Optional(), Length(max=255)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Item')


class InventoryTransactionForm(FlaskForm):
    """Form to record inventory transactions."""
    item_id = SelectField('Item', coerce=int, validators=[DataRequired()])
    transaction_type = SelectField('Transaction Type', choices=[
        (t.value, t.value.replace('_', ' ').upper()) for t in TransactionType
    ])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        validate_positive_number('Quantity must be positive')
    ])
    notes = StringField('Notes', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Record Transaction')


class InventorySearchForm(FlaskForm):
    """Form to search inventory items."""
    search_query = StringField('Search by name', validators=[
        Optional(),
        Length(min=2)
    ])
    category = StringField('Category', validators=[Optional(), Length(max=120)])
    low_stock_only = SelectField('Stock Status', choices=[
        ('all', 'All Items'),
        ('low', 'Low Stock Only'),
        ('out', 'Out of Stock')
    ])
    submit = SubmitField('Search')
