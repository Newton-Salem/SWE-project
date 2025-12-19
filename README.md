# EduTrack - Smart Classroom System

EduTrack is a comprehensive online smart classroom system designed to improve communication and simplify academic processes between students and faculty.

## Team Information

- **Team Number:** 29
- **Team Members:**
  - Habiba Mohammed (202402213)
  - Ahmed Mahmoud (202401491)
  - Mohamed Essam (202401171)
- **Contact:** s-ahmed.abda@zewailcity.edu.eg

## Features

### Core Functional Requirements (10)

1. **User Registration & Authentication** - Secure user registration and login with role-based access
2. **Admin User Management** - Admin can create, edit, and delete users
3. **Course Management** - Teachers can create courses, students can join via code
4. **Lecture Upload and Management** - Upload PDF files and video links for course materials
5. **Assignment Creation and Submission** - Create assignments with due dates, submit files
6. **Grading and Feedback** - Teachers can grade submissions and provide feedback
7. **Attendance Tracking** - Record and track student attendance per session
8. **Course Chat** - Real-time messaging within courses
9. **Dashboards and Notifications** - Role-based dashboards with notifications
10. **File Download & Storage** - Download lecture files and submissions

### Bonus Features (5 additional)

11. **Notifications System** - Comprehensive notification system for grades, assignments, etc.
12. **Course Announcements** - Teachers can post announcements to courses
13. **Grade Summary** - Automatic calculation of average grades per course
14. **User Preferences** - Customizable user settings
15. **Course Materials Organization** - Enhanced material management system

### Non-Functional Requirements

- **Security:** Password hashing, session management, role-based access control
- **Usability:** Modern, responsive UI with intuitive navigation
- **Performance:** Optimized database queries, efficient file handling
- **Maintainability:** MVC architecture, modular code structure

## Technology Stack

- **Backend:** Python 3.11, Flask 3.1.2
- **Frontend:** HTML5, CSS3
- **Database:** SQL Server (SSMS)
- **Database Driver:** pyodbc
- **Architecture:** MVC (Model-View-Controller) Pattern
- **Design Patterns:**
  - Factory Pattern (App Factory, Repository Factory)
  - Singleton Pattern (Database Connection)
  - Repository Pattern (Data Access Layer)
- **Testing:** pytest

## Project Structure

```
SWE-project/
├── app.py                 # Application factory
├── config.py              # Configuration
├── database/
│   ├── connection.py      # Singleton DB connection
│   └── create_tables.py    # Database schema
├── models/                # Data models
├── repositories/          # Repository pattern (DAO layer)
├── services/              # Business logic
├── controllers/           # Route handlers (blueprints)
├── templates/             # HTML templates
├── src/
│   ├── static/
│   │   └── css/
│   │       └── style.css  # Modern CSS styling
│   └── uploads/           # File uploads directory
├── tests/                 # Unit and integration tests
├── docs/                  # Documentation
├── deployment/            # Deployment files
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Installation and Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- SQL Server (SSMS) installed and running
- ODBC Driver 17 for SQL Server (or compatible version)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd SWE-project
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure SQL Server:**
   - Ensure SQL Server is running
   - Create a database named "EduTrack" (or update DB_NAME in config.py)
   - Update connection settings in `config.py` or set environment variables:
     - `DB_SERVER`: SQL Server instance (default: localhost)
     - `DB_NAME`: Database name (default: EduTrack)
     - `DB_DRIVER`: ODBC Driver name (default: ODBC Driver 17 for SQL Server)
     - `DB_TRUSTED`: Use Windows Authentication (default: yes)

5. **Initialize database:**
   ```bash
   python -c "from database.create_tables import create_tables; create_tables()"
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the application:**
   - Open browser: http://localhost:5000
   - Register a new account or login

### Docker Deployment

1. **Build Docker image:**
   ```bash
   docker build -t edutrack:latest .
   ```

2. **Run container:**
   ```bash
   docker run -d -p 5000:5000 --name edutrack edutrack:latest
   ```

3. **Access the application:**
   - Open browser: http://localhost:5000

## Usage

### For Teachers

1. Register/Login as a teacher
2. Create courses with unique codes
3. Upload lecture materials (PDFs or video links)
4. Create assignments with due dates
5. Record attendance for each session
6. Grade student submissions
7. Post announcements
8. Communicate via course chat

### For Students

1. Register/Login as a student
2. Join courses using course codes
3. View and download lecture materials
4. Submit assignments before due dates
5. View grades and feedback
6. Check attendance records
7. Participate in course chat
8. View notifications

### For Admins

1. Login as admin
2. Manage all users (create, edit, delete)
3. View system logs
4. Manage courses

## Testing

Run unit tests with pytest:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_auth.py -v
```

**Note:** Tests require SQL Server to be running and accessible.

## Design Patterns Implemented

1. **MVC (Model-View-Controller)** - Core architecture
2. **Factory Pattern** - App Factory and Repository Factory
3. **Singleton Pattern** - Database connection
4. **Repository Pattern** - Data access abstraction

## CI/CD

The project includes GitHub Actions workflow for:
- Automated testing on push/PR
- Docker image building
- Code coverage reporting

## Documentation

- **SRS Document:** See `docs/` folder
- **Design Document:** See `docs/` folder
- **API Documentation:** See inline code comments

## License

This project is developed for educational purposes as part of CSAI 203 course.

## Contributors

- Habiba Mohammed
- Ahmed Mahmoud
- Mohamed Essam

## Acknowledgments

- Dr. Mohamed Sami Rakha - Course Instructor
- Zewail City of Science, Technology and Innovation
