from tkinter import END
from database.connection import DatabaseConnection

def create_tables():
    db = DatabaseConnection()
    cursor = db.get_cursor()

    #  USERS 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
        BEGIN
            CREATE TABLE users (
                user_id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(100) NOT NULL,
                email NVARCHAR(100) UNIQUE NOT NULL,
                password NVARCHAR(255) NOT NULL,
                role NVARCHAR(20) CHECK (role IN ('student','teacher','admin')) NOT NULL
            )
        END
    """)

    #  COURSES 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'courses')
        BEGIN
            CREATE TABLE courses (
                course_id INT IDENTITY(1,1) PRIMARY KEY,
                teacher_id INT NOT NULL,
                title NVARCHAR(200) NOT NULL,
                code NVARCHAR(20) UNIQUE NOT NULL,
                description NVARCHAR(MAX),
                FOREIGN KEY (teacher_id) REFERENCES users(user_id)
            )
        END
    """)

    #  ENROLLMENT 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'enrollment')
        BEGIN
            CREATE TABLE enrollment (
                id INT IDENTITY(1,1) PRIMARY KEY,
                student_id INT NOT NULL,
                course_id INT NOT NULL,
                enrolled_date DATE NOT NULL,
                FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                CONSTRAINT UQ_StudentCourse UNIQUE (student_id, course_id)
            )
        END
    """)

    #  LECTURES 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'lectures')
        BEGIN
            CREATE TABLE lectures (
                lecture_id INT IDENTITY(1,1) PRIMARY KEY,
                course_id INT NOT NULL,
                title NVARCHAR(200) NOT NULL,
                file_path NVARCHAR(255),
                video_link NVARCHAR(255),
                upload_date DATE NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        END
    """)

    #  ASSIGNMENTS 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'assignments')
        BEGIN
            CREATE TABLE assignments (
                assignment_id INT IDENTITY(1,1) PRIMARY KEY,
                course_id INT NOT NULL,
                title NVARCHAR(200) NOT NULL,
                description NVARCHAR(MAX),
                due_date DATE NOT NULL,
                max_grade INT NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        END
    """)

    #  SUBMISSIONS 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'submissions')
        BEGIN
            CREATE TABLE submissions (
                submission_id INT IDENTITY(1,1) PRIMARY KEY,
                assignment_id INT NOT NULL,
                student_id INT NOT NULL,
                file_path NVARCHAR(255) NOT NULL,
                timestamp DATETIME NOT NULL,
                grade INT,
                feedback NVARCHAR(MAX),
                FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        END
    """)

    #  ATTENDANCE 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'attendance')
        BEGIN
            CREATE TABLE attendance (
                attendance_id INT IDENTITY(1,1) PRIMARY KEY,
                course_id INT NOT NULL,
                student_id INT NOT NULL,
                date DATE NOT NULL,
                status NVARCHAR(20) CHECK (status IN ('Present','Absent','Excused')) NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
                CONSTRAINT UQ_Attendance UNIQUE (course_id, student_id, date)
            )
        END
    """)

    #  CHAT 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'chat_messages')
        BEGIN
             CREATE TABLE chat_messages (
                chat_id INT IDENTITY(1,1) PRIMARY KEY,
                course_id INT NOT NULL,
                student_id INT NOT NULL,    
                sender_id INT NOT NULL,      
                message NVARCHAR(MAX) NOT NULL,
                timestamp DATETIME NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(course_id),
                FOREIGN KEY (student_id) REFERENCES users(user_id),
                FOREIGN KEY (sender_id) REFERENCES users(user_id)
            )
        END
     """)

    #  NOTIFICATIONS 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'notifications')
        BEGIN
            CREATE TABLE notifications (
                notification_id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT NOT NULL,
                message NVARCHAR(MAX) NOT NULL,
                type NVARCHAR(50) NOT NULL,
                related_id INT,
                is_read INT DEFAULT 0,
                created_at DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        END
    """)

    #  COURSE MATERIALS 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'course_materials')
        BEGIN
            CREATE TABLE course_materials (
                material_id INT IDENTITY(1,1) PRIMARY KEY,
                course_id INT NOT NULL,
                title NVARCHAR(200) NOT NULL,
                material_type NVARCHAR(50) NOT NULL,
                file_path NVARCHAR(255),
                url NVARCHAR(255),
                description NVARCHAR(MAX),
                created_at DATETIME NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        END
    """)

    # GRADE SUMMARY 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'grade_summary')
        BEGIN
            CREATE TABLE grade_summary (
                summary_id INT IDENTITY(1,1) PRIMARY KEY,
                student_id INT NOT NULL,
                course_id INT NOT NULL,
                total_assignments INT DEFAULT 0,
                completed_assignments INT DEFAULT 0,
                average_grade FLOAT,
                last_updated DATETIME NOT NULL,
                FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                CONSTRAINT UQ_GradeSummary UNIQUE (student_id, course_id)
            )
        END
    """)

    #  USER PREFERENCES 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'user_preferences')
        BEGIN
            CREATE TABLE user_preferences (
                preference_id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT NOT NULL UNIQUE,
                email_notifications INT DEFAULT 1,
                theme NVARCHAR(20) DEFAULT 'light',
                language NVARCHAR(10) DEFAULT 'en',
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        END
    """)
    # ANNOUNCEMENTS 
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'announcements')
        BEGIN
           CREATE TABLE announcements (
                announcement_id INT IDENTITY(1,1) PRIMARY KEY,
                course_id INT NOT NULL,
                teacher_id INT NOT NULL,
                title NVARCHAR(255) NOT NULL,
                content NVARCHAR(MAX) NOT NULL,
                created_at DATETIME NOT NULL DEFAULT GETDATE(),
                FOREIGN KEY (course_id) REFERENCES courses(course_id),
                FOREIGN KEY (teacher_id) REFERENCES users(user_id)
             )
        END
    """)

    db.get_connection().commit()
    print("[OK] Database tables created successfully")

if __name__ == "__main__":
    create_tables()