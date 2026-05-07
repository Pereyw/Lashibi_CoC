"""
Helper functions for common operations.
"""

from datetime import datetime, timedelta
from app.models.user import db


def get_date_range(period='month'):
    """
    Get date range for filtering.
    
    Args:
        period: 'week', 'month', 'quarter', 'year'
        
    Returns:
        tuple: (start_date, end_date)
    """
    today = datetime.utcnow().date()
    
    if period == 'week':
        start = today - timedelta(days=today.weekday())
    elif period == 'month':
        start = today.replace(day=1)
    elif period == 'quarter':
        quarter = (today.month - 1) // 3
        start = today.replace(month=quarter * 3 + 1, day=1)
    elif period == 'year':
        start = today.replace(month=1, day=1)
    else:
        start = today
    
    return start, today


def calculate_percentage(part, total):
    """Calculate percentage safely."""
    if total == 0:
        return 0
    return round((part / total) * 100, 2)


def paginate_query(query, page=1, per_page=20):
    """
    Paginate a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        per_page: Items per page
        
    Returns:
        tuple: (items, total, pages)
    """
    total = query.count()
    pages = (total + per_page - 1) // per_page
    
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    
    return items, total, pages


def flash_message(category, message):
    """Helper to create flash message dict."""
    return {
        'category': category,
        'message': message,
    }


def commit_changes(message="Changes saved"):
    """Commit database changes with error handling."""
    try:
        db.session.commit()
        return True, message
    except Exception as e:
        db.session.rollback()
        return False, f"Error: {str(e)}"
