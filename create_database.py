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

    db.get_connection().commit()

if __name__ == "__main__":
    create_tables()