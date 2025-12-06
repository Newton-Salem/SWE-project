from database.db import MySQLConnection

def create_tables():
    db = MySQLConnection()
    cursor = db.get_cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            role ENUM('student','teacher','admin')
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INT PRIMARY KEY AUTO_INCREMENT,
            teacher_id INT,
            title VARCHAR(200),
            code VARCHAR(20) UNIQUE,
            description TEXT,
            FOREIGN KEY (teacher_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollment (
            id INT PRIMARY KEY AUTO_INCREMENT,
            student_id INT NOT NULL,
            course_id INT NOT NULL,
            enrolled_date DATE,
            
            FOREIGN KEY (student_id) REFERENCES users(user_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id),

            UNIQUE (student_id, course_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lectures (
            lecture_id INT PRIMARY KEY AUTO_INCREMENT,
            course_id INT NOT NULL,
            title VARCHAR(200) NOT NULL,
            file_path VARCHAR(255),
            video_link VARCHAR(255),
            upload_date DATE,
            
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    """)



    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id INT PRIMARY KEY AUTO_INCREMENT,
            course_id INT NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            due_date DATE,
            max_grade INT,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        );
    """)

 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            submission_id INT PRIMARY KEY AUTO_INCREMENT,
            assignment_id INT NOT NULL,
            student_id INT NOT NULL,
            file_path VARCHAR(255),
            timestamp DATETIME,
            grade INT,
            feedback TEXT,
            FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id),
            FOREIGN KEY (student_id) REFERENCES users(user_id)
        );
    """)

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INT PRIMARY KEY AUTO_INCREMENT,
            course_id INT NOT NULL,
            student_id INT NOT NULL,
            date DATE,
            status ENUM('Present','Absent','Excused'),
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (student_id) REFERENCES users(user_id)
        );
    """)

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            chat_id INT PRIMARY KEY AUTO_INCREMENT,
            course_id INT NOT NULL,
            sender_id INT NOT NULL,
            message TEXT,
            timestamp DATETIME,
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (sender_id) REFERENCES users(user_id)
        );
    """)

    db.get_connection().commit()

if __name__ == "__main__":
    create_tables()