"""
Inventory management routes and views.
Handles inventory items, stock levels, and transaction tracking.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.user import db
from app.models.inventory import InventoryItem, InventoryTransaction, TransactionType
from app.forms import InventoryItemForm, InventoryTransactionForm, InventorySearchForm
from app.utils import staff_required, paginate_query, commit_changes

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')


@inventory_bp.route('/')
@login_required
def index():
    """Inventory dashboard."""
    # Get low stock items
    low_stock_items = InventoryItem.query.filter(
        InventoryItem.quantity <= InventoryItem.reorder_level
    ).all()
    
    # Get summary statistics
    total_items = InventoryItem.query.count()
    active_items = InventoryItem.query.filter_by(is_active=True).count()
    
    return render_template(
        'inventory/index.html',
        low_stock_items=low_stock_items,
        total_items=total_items,
        active_items=active_items
    )


@inventory_bp.route('/items')
@login_required
def list_items():
    """List inventory items."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    category = request.args.get('category', '')
    low_stock_only = request.args.get('low_stock_only', 'false')
    
    query = InventoryItem.query
    
    if search_query:
        query = query.filter(InventoryItem.name.ilike(f'%{search_query}%'))
    
    if category:
        query = query.filter_by(category=category)
    
    if low_stock_only == 'true':
        query = query.filter(InventoryItem.quantity <= InventoryItem.reorder_level)
    
    query = query.order_by(InventoryItem.name)
    items, total, pages = paginate_query(query, page, per_page=20)
    
    # Get unique categories for filter
    categories = db.session.query(InventoryItem.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template(
        'inventory/list.html',
        items=items,
        total=total,
        pages=pages,
        current_page=page,
        search_query=search_query,
        category=category,
        categories=categories,
        low_stock_only=low_stock_only
    )


@inventory_bp.route('/items/<int:item_id>')
@login_required
def view_item(item_id):
    """View inventory item details."""
    item = InventoryItem.query.get_or_404(item_id)
    
    # Get recent transactions
    transactions = item.transactions.order_by(InventoryTransaction.date.desc()).limit(10).all()
    
    return render_template(
        'inventory/detail.html',
        item=item,
        transactions=transactions
    )


@inventory_bp.route('/items/new', methods=['GET', 'POST'])
@staff_required
def create_item():
    """Create a new inventory item."""
    form = InventoryItemForm()
    
    if form.validate_on_submit():
        item = InventoryItem(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data,
            quantity=form.quantity.data,
            unit=form.unit.data,
            unit_cost=form.unit_cost.data,
            reorder_level=form.reorder_level.data,
            reorder_quantity=form.reorder_quantity.data,
            supplier=form.supplier.data,
            location=form.location.data,
            notes=form.notes.data,
        )
        
        db.session.add(item)
        success, message = commit_changes('Item created successfully')
        
        if success:
            flash(message, 'success')
            return redirect(url_for('inventory.view_item', item_id=item.id))
        else:
            flash(message, 'danger')
    
    return render_template('inventory/item_form.html', form=form, item=None)


@inventory_bp.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
@staff_required
def edit_item(item_id):
    """Edit inventory item."""
    item = InventoryItem.query.get_or_404(item_id)
    form = InventoryItemForm()
    
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.category = form.category.data
        item.quantity = form.quantity.data
        item.unit = form.unit.data
        item.unit_cost = form.unit_cost.data
        item.reorder_level = form.reorder_level.data
        item.reorder_quantity = form.reorder_quantity.data
        item.supplier = form.supplier.data
        item.location = form.location.data
        item.notes = form.notes.data
        
        success, message = commit_changes('Item updated successfully')
        
        if success:
            flash(message, 'success')
            return redirect(url_for('inventory.view_item', item_id=item.id))
        else:
            flash(message, 'danger')
    
    elif request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.category.data = item.category
        form.quantity.data = item.quantity
        form.unit.data = item.unit
        form.unit_cost.data = item.unit_cost
        form.reorder_level.data = item.reorder_level
        form.reorder_quantity.data = item.reorder_quantity
        form.supplier.data = item.supplier
        form.location.data = item.location
        form.notes.data = item.notes
    
    return render_template('inventory/item_form.html', form=form, item=item)


@inventory_bp.route('/items/<int:item_id>/delete', methods=['POST'])
@staff_required
def delete_item(item_id):
    """Delete inventory item."""
    item = InventoryItem.query.get_or_404(item_id)
    name = item.name
    
    db.session.delete(item)
    success, message = commit_changes('Item deleted successfully')
    
    if success:
        flash(f'{name} has been deleted.', 'success')
    else:
        flash(f'Error deleting item: {message}', 'danger')
    
    return redirect(url_for('inventory.list_items'))


@inventory_bp.route('/transactions')
@login_required
def list_transactions():
    """List all inventory transactions."""
    page = request.args.get('page', 1, type=int)
    
    query = InventoryTransaction.query.order_by(InventoryTransaction.date.desc())
    items, total, pages = paginate_query(query, page, per_page=20)
    
    return render_template(
        'inventory/transactions.html',
        transactions=items,
        total=total,
        pages=pages,
        current_page=page
    )


@inventory_bp.route('/items/<int:item_id>/transaction/in', methods=['GET', 'POST'])
@staff_required
def add_stock(item_id):
    """Record stock IN transaction."""
    item = InventoryItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        try:
            quantity = int(request.form.get('quantity', 0))
            notes = request.form.get('notes', '')
            
            if quantity <= 0:
                raise ValueError('Quantity must be positive')
            
            item.add_stock(quantity, notes)
            success, message = commit_changes('Stock added successfully')
            
            if success:
                flash(message, 'success')
                return redirect(url_for('inventory.view_item', item_id=item.id))
            else:
                flash(message, 'danger')
        except (ValueError, Exception) as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('inventory/stock_transaction.html', item=item, transaction_type='in')


@inventory_bp.route('/items/<int:item_id>/transaction/out', methods=['GET', 'POST'])
@staff_required
def remove_stock(item_id):
    """Record stock OUT transaction."""
    item = InventoryItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        try:
            quantity = int(request.form.get('quantity', 0))
            notes = request.form.get('notes', '')
            
            if quantity <= 0:
                raise ValueError('Quantity must be positive')
            
            item.remove_stock(quantity, notes)
            success, message = commit_changes('Stock removed successfully')
            
            if success:
                flash(message, 'success')
                return redirect(url_for('inventory.view_item', item_id=item.id))
            else:
                flash(message, 'danger')
        except ValueError as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('inventory/stock_transaction.html', item=item, transaction_type='out')
