from database.connection import DatabaseConnection
from datetime import date, datetime
from werkzeug.security import generate_password_hash


def get_id(cursor, table, column, value):
    cursor.execute(f"SELECT {table[:-1]}_id FROM {table} WHERE {column} = ?", value)
    row = cursor.fetchone()
    return row[0] if row else None


def seed_data():
    db = DatabaseConnection()
    cursor = db.get_cursor()

    # USERS 
    users = [
        ('Admin User', 'admin@edu.com', generate_password_hash('admin123'), 'admin'),
        ('Dr. Ahmed', 'ahmed@edu.com', generate_password_hash('123456'), 'teacher'),
        ('Dr. Mona', 'mona@edu.com', generate_password_hash('123456'), 'teacher'),
        ('Student Ali', 'ali@edu.com', generate_password_hash('123456'), 'student'),
        ('Student Sara', 'sara@edu.com', generate_password_hash('123456'), 'student'),
        ('Student Omar', 'omar@edu.com', generate_password_hash('123456'), 'student'),
    ]

    for name, email, password, role in users:
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM users WHERE email = ?)
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, email, name, email, password, role)

    #GET IDS 
    teacher_ahmed = get_id(cursor, "users", "email", "ahmed@edu.com")
    teacher_mona = get_id(cursor, "users", "email", "mona@edu.com")

    student_ali = get_id(cursor, "users", "email", "ali@edu.com")
    student_sara = get_id(cursor, "users", "email", "sara@edu.com")
    student_omar = get_id(cursor, "users", "email", "omar@edu.com")

    #COURSES 
    courses = [
        (teacher_ahmed, 'Database Systems', 'DB101', 'Intro to Databases'),
        (teacher_mona, 'Software Engineering', 'SWE201', 'Software Dev Principles'),
    ]

    for teacher_id, title, code, desc in courses:
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM courses WHERE code = ?)
            INSERT INTO courses (teacher_id, title, code, description)
            VALUES (?, ?, ?, ?)
        """, code, teacher_id, title, code, desc)

    course_db = get_id(cursor, "courses", "code", "DB101")
    course_swe = get_id(cursor, "courses", "code", "SWE201")

    #ENROLLMENT
    enrollments = [
        (student_ali, course_db),
        (student_sara, course_db),
        (student_omar, course_swe),
        (student_ali, course_swe),
    ]

    for student_id, course_id in enrollments:
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM enrollment
                WHERE student_id = ? AND course_id = ?
            )
            INSERT INTO enrollment (student_id, course_id, enrolled_date)
            VALUES (?, ?, ?)
        """, student_id, course_id, student_id, course_id, date.today())

    #  LECTURES 
    lectures = [
        (course_db, 'Intro to DB', 'lec1.pdf'),
        (course_db, 'ER Diagrams', 'lec2.pdf'),
        (course_swe, 'SDLC Overview', 'lec1.pdf'),
    ]

    for course_id, title, file_path in lectures:
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM lectures
                WHERE course_id = ? AND title = ?
            )
            INSERT INTO lectures (course_id, title, file_path, upload_date)
            VALUES (?, ?, ?, ?)
        """, course_id, title, course_id, title, file_path, date.today())

    #  ASSIGNMENTS
    cursor.execute("""
        IF NOT EXISTS (SELECT 1 FROM assignments WHERE title = 'HW1')
        INSERT INTO assignments (course_id, title, description, due_date, max_grade)
        VALUES (?, 'HW1', 'Intro Assignment', ?, 100)
    """, course_db, date.today())

    assignment_hw1 = get_id(cursor, "assignments", "title", "HW1")

    #  SUBMISSIONS
    cursor.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM submissions
            WHERE student_id = ? AND assignment_id = ?
        )
        INSERT INTO submissions (assignment_id, student_id, file_path, timestamp, grade)
        VALUES (?, ?, ?, ?, ?)
    """, student_ali, assignment_hw1,
       assignment_hw1, student_ali, 'hw1_ali.pdf', datetime.now(), 85)

    # ATTENDANCE 
    cursor.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM attendance
            WHERE student_id = ? AND course_id = ? AND date = ?
        )
        INSERT INTO attendance (course_id, student_id, date, status)
        VALUES (?, ?, ?, 'Present')
    """, student_sara, course_db, date.today(),
       course_db, student_sara, date.today())

    # NOTIFICATIONS 
    cursor.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM notifications
            WHERE user_id = ? AND type = 'enrollment'
        )
        INSERT INTO notifications (user_id, message, type, created_at)
        VALUES (?, 'You have been enrolled in DB101', 'enrollment', ?)
    """, student_ali, student_ali, datetime.now())

    # USER PREFERENCES 
    cursor.execute("""
        IF NOT EXISTS (SELECT 1 FROM user_preferences WHERE user_id = ?)
        INSERT INTO user_preferences (user_id, email_notifications, theme, language)
        VALUES (?, 1, 'dark', 'en')
    """, student_ali, student_ali)

    # GRADE SUMMARY
    cursor.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM grade_summary
            WHERE student_id = ? AND course_id = ?
        )
        INSERT INTO grade_summary (
            student_id, course_id, total_assignments,
            completed_assignments, average_grade, last_updated
        )
        VALUES (?, ?, 1, 1, 85, ?)
    """, student_ali, course_db,
       student_ali, course_db, datetime.now())
    
    

    db.commit()
    print("Extended sample data seeded successfully")


if __name__ == "__main__":
    seed_data()