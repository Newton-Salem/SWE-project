# SQL Server Setup Guide

## Prerequisites

1. **Install SQL Server**
   - Download and install SQL Server from Microsoft
   - Or use SQL Server Express (free version)

2. **Install SSMS (SQL Server Management Studio)**
   - Download from Microsoft website
   - Used for managing databases

3. **Install ODBC Driver**
   - Download "ODBC Driver 17 for SQL Server" from Microsoft
   - Or use "ODBC Driver 13 for SQL Server" (older version)

## Database Setup

### Step 1: Create Database

1. Open SSMS
2. Connect to your SQL Server instance
3. Right-click on "Databases" > "New Database"
4. Name it "EduTrack"
5. Click "OK"

### Step 2: Configure Connection

Update `config.py` or set environment variables:

```python
# In config.py
DB_SERVER = "localhost"  # or your server name
DB_NAME = "EduTrack"
DB_DRIVER = "ODBC Driver 17 for SQL Server"
DB_TRUSTED = "yes"  # Use Windows Authentication
```

Or set environment variables:
```bash
set DB_SERVER=localhost
set DB_NAME=EduTrack
set DB_DRIVER=ODBC Driver 17 for SQL Server
set DB_TRUSTED=yes
```

### Step 3: Initialize Tables

Run the following command to create all tables:

```bash
python -c "from database.create_tables import create_tables; create_tables()"
```

Or run directly:
```bash
python database/create_tables.py
```

### Step 4: Verify Tables

In SSMS, expand "EduTrack" database > "Tables" to see all created tables:
- users
- courses
- enrollment
- lectures
- assignments
- submissions
- attendance
- chat_messages
- notifications
- announcements
- (and other bonus feature tables)

## Connection String Format

The application uses the following connection string format:
```
DRIVER={ODBC Driver 17 for SQL Server};
SERVER=localhost;
DATABASE=EduTrack;
Trusted_Connection=yes;
```

## Troubleshooting

### Error: "ODBC Driver not found"
- Install ODBC Driver from Microsoft
- Check driver name matches exactly (case-sensitive)
- List available drivers: `pyodbc.drivers()` in Python

### Error: "Cannot open database"
- Verify database "EduTrack" exists
- Check SQL Server is running
- Verify user has permissions

### Error: "Login failed"
- For Windows Authentication: Ensure user has SQL Server access
- For SQL Authentication: Update connection string to include username/password

## Testing Connection

Test your connection with Python:

```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=EduTrack;"
    "Trusted_Connection=yes;"
)
print("Connection successful!")
conn.close()
```

