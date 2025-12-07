from database.connection import MySQLConnection

def create_tables():
    db = MySQLConnection()
    cursor = db.get_cursor()

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
    BEGIN
        CREATE TABLE users (
            user_id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100),
            email NVARCHAR(100) UNIQUE,
            password NVARCHAR(255),
            role NVARCHAR(20) CHECK (role IN ('student','teacher','admin'))
        )
    END
    """)

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'courses')
    BEGIN
        CREATE TABLE courses (
            course_id INT IDENTITY(1,1) PRIMARY KEY,
            teacher_id INT NOT NULL,
            title NVARCHAR(200),
            code NVARCHAR(20) UNIQUE,
            description NVARCHAR(MAX),
            FOREIGN KEY (teacher_id) REFERENCES users(user_id)
        )
    END
    """)

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'enrollment')
    BEGIN
        CREATE TABLE enrollment (
            id INT IDENTITY(1,1) PRIMARY KEY,
            student_id INT NOT NULL,
            course_id INT NOT NULL,
            enrolled_date DATE,
            FOREIGN KEY (student_id) REFERENCES users(user_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            CONSTRAINT UQ_StudentCourse UNIQUE (student_id, course_id)
        )
    END
    """)

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'lectures')
    BEGIN
        CREATE TABLE lectures (
            lecture_id INT IDENTITY(1,1) PRIMARY KEY,
            course_id INT NOT NULL,
            title NVARCHAR(200) NOT NULL,
            file_path NVARCHAR(255),
            video_link NVARCHAR(255),
            upload_date DATE,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    END
    """)

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'assignments')
    BEGIN
        CREATE TABLE assignments (
            assignment_id INT IDENTITY(1,1) PRIMARY KEY,
            course_id INT NOT NULL,
            title NVARCHAR(200) NOT NULL,
            description NVARCHAR(MAX),
            due_date DATE,
            max_grade INT,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    END
    """)

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'submissions')
    BEGIN
        CREATE TABLE submissions (
            submission_id INT IDENTITY(1,1) PRIMARY KEY,
            assignment_id INT NOT NULL,
            student_id INT NOT NULL,
            file_path NVARCHAR(255),
            timestamp DATETIME,
            grade INT,
            feedback NVARCHAR(MAX),
            FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id),
            FOREIGN KEY (student_id) REFERENCES users(user_id)
        )
    END
    """)

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'attendance')
    BEGIN
        CREATE TABLE attendance (
            attendance_id INT IDENTITY(1,1) PRIMARY KEY,
            course_id INT NOT NULL,
            student_id INT NOT NULL,
            date DATE,
            status NVARCHAR(20) CHECK (status IN ('Present','Absent','Excused')),
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (student_id) REFERENCES users(user_id)
        )
    END
    """)

    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'chat_messages')
    BEGIN
        CREATE TABLE chat_messages (
            chat_id INT IDENTITY(1,1) PRIMARY KEY,
            course_id INT NOT NULL,
            sender_id INT NOT NULL,
            message NVARCHAR(MAX),
            timestamp DATETIME,
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (sender_id) REFERENCES users(user_id)
        )
    END
    """)

    db.get_connection().commit()

if __name__ == "__main__":
    create_tables()
