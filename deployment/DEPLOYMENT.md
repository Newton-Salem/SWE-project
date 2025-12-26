# Deployment Guide

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure SQL Server:**
   - Ensure SQL Server is running
   - Create database "EduTrack" in SSMS
   - Update `config.py` with your SQL Server connection details, or set environment variables:
     ```bash
     set DB_SERVER=localhost
     set DB_NAME=EduTrack
     set DB_DRIVER=ODBC Driver 17 for SQL Server
     set DB_TRUSTED=yes
     ```

3. **Initialize database:**
   ```bash
   python -c "from database.create_tables import create_tables; create_tables()"
   ```

4. **Run application:**
   ```bash
   python app.py
   ```

5. **Access at http://localhost:5000**

## Docker Deployment

### Build Image
```bash
docker build -t edutrack:latest .
```

### Run Container
```bash
docker run -d -p 5000:5000 \
  -v $(pwd)/edutrack.db:/app/edutrack.db \
  -v $(pwd)/src/uploads:/app/src/uploads \
  --name edutrack edutrack:latest
```

### Stop Container
```bash
docker stop edutrack
docker rm edutrack
```

## Production Deployment

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `FLASK_ENV`: Set to `production`
- `DATABASE_PATH`: Path to SQLite database file

### Using Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  edutrack:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./edutrack.db:/app/edutrack.db
      - ./src/uploads:/app/src/uploads
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key-here
```

Run:
```bash
docker-compose up -d
```

## Database Backup

To backup SQL Server database, use SSMS:
1. Right-click on "EduTrack" database
2. Select "Tasks" > "Back Up..."
3. Configure backup settings and execute

Or use SQL command:
```sql
BACKUP DATABASE EduTrack TO DISK = 'C:\backup\EduTrack.bak'
```

## Troubleshooting

1. **SQL Server connection error**: 
   - Verify SQL Server is running
   - Check connection string in `config.py`
   - Ensure ODBC Driver is installed
   - Verify database "EduTrack" exists

2. **ODBC Driver not found**: 
   - Install "ODBC Driver 17 for SQL Server" from Microsoft
   - Update `DB_DRIVER` in config if using different driver

3. **File upload fails**: Check uploads directory permissions

4. **Static files not loading**: Verify static folder path in app.py

5. **Authentication issues**: Ensure SQL Server authentication is configured correctly

