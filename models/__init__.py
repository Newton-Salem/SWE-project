"""Helper function for converting SQL Server row tuples to dictionaries"""

def row_to_dict(cursor, row):
    """Convert SQL Server tuple row to dictionary"""
    if not row:
        return None
    
    if cursor and cursor.description:
        cols = [c[0] for c in cursor.description]
        return dict(zip(cols, row))
    else:
  
        if hasattr(row, 'keys'):
            return dict(row)
        return None
