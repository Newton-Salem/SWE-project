# Troubleshooting Guide

## PyODBC Connection Issues

### Error: "ModuleNotFoundError: No module named 'pyodbc'"

**Solution:**
```bash
pip install pyodbc
```

Or install from requirements:
```bash
pip install -r requirements.txt
```

### Error: "Interface Error" or "Driver not found"

**Cause:** ODBC Driver for SQL Server is not installed.

**Solution:**
1. Download and install "ODBC Driver 17 for SQL Server" or "ODBC Driver 18 for SQL Server" from Microsoft
2. Restart your application after installation

**Check available drivers:**
```python
import pyodbc
print(pyodbc.drivers())
```

### Error: "Operational Error" - Cannot connect to server

**Possible causes:**
1. SQL Server is not running
2. Server name is incorrect
3. Database does not exist
4. Network connectivity issues
5. Firewall blocking connection

**Solutions:**
1. **Check SQL Server is running:**
   - Open SQL Server Configuration Manager
   - Verify SQL Server service is running

2. **Verify server name:**
   - Default: `localhost` or `.` for local instance
   - Named instance: `localhost\INSTANCENAME`
   - Remote: `SERVERNAME` or `SERVERNAME\INSTANCENAME`

3. **Create database:**
   ```sql
   CREATE DATABASE EduTrack;
   ```

4. **Check firewall:**
   - Ensure SQL Server port (default 1433) is open
   - Allow SQL Server through Windows Firewall

5. **Enable SQL Server Authentication:**
   - If using SQL Authentication instead of Windows Authentication, update connection string:
   ```python
   connection_string = (
       f"DRIVER={{ODBC Driver 17 for SQL Server}};"
       f"SERVER={server};"
       f"DATABASE={database};"
       f"UID={username};"
       f"PWD={password};"
   )
   ```

### Error: "Database connection is not available"

**Cause:** Connection failed during initialization.

**Solution:**
1. Check error messages in console output
2. Verify SQL Server is accessible
3. Check connection string parameters
4. Ensure database exists

### Connection String Configuration

Set environment variables or update `config.py`:

```bash
# Windows PowerShell
$env:DB_SERVER="localhost"
$env:DB_NAME="EduTrack"
$env:DB_DRIVER="ODBC Driver 17 for SQL Server"
$env:DB_TRUSTED="yes"
```

Or in `config.py`:
```python
DB_SERVER = "localhost"
DB_NAME = "EduTrack"
DB_DRIVER = "ODBC Driver 17 for SQL Server"
DB_TRUSTED = "yes"
```

### Testing Connection

Test your connection with Python:

```python
import pyodbc

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=EduTrack;"
        "Trusted_Connection=yes;"
    )
    print("✓ Connection successful!")
    conn.close()
except Exception as e:
    print(f"✗ Connection failed: {e}")
```

### Common Issues

1. **"Login failed for user"**
   - Check Windows Authentication is enabled
   - Or use SQL Authentication with correct credentials

2. **"Cannot open database"**
   - Database doesn't exist - create it first
   - User doesn't have permissions

3. **"Timeout expired"**
   - SQL Server is not responding
   - Network issues
   - Firewall blocking

4. **"Driver version mismatch"**
   - Update ODBC Driver to latest version
   - Or use compatible driver version

## Getting Help

If issues persist:
1. Check SQL Server error logs
2. Verify ODBC driver installation
3. Test connection with SQL Server Management Studio (SSMS)
4. Review connection string format
5. Check network connectivity

