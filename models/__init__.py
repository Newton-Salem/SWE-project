"""Helper function for converting SQL Server row tuples to dictionaries"""

def row_to_dict(cursor, row):
    """Convert SQL Server tuple row to dictionary"""
    if not row:
        return None
    
    # SQL Server returns tuples, get column names from cursor
    if cursor and cursor.description:
        cols = [c[0] for c in cursor.description]
        return dict(zip(cols, row))
    else:
        # Fallback: assume row is already a dict or has column names
        if hasattr(row, 'keys'):
            return dict(row)
        return None

