from repositories.base_repository import BaseRepository
from models.assignment import Assignment


class AssignmentRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def create_assignment(self, course_id, title, description, due_date, max_grade):
        self.cursor.execute("""
            INSERT INTO assignments (course_id, title, description, due_date, max_grade)
            VALUES (?, ?, ?, ?, ?)
        """, (course_id, title, description, due_date, max_grade))
        self.conn.commit()

    def get_by_course(self, course_id):
        self.cursor.execute(
            "SELECT * FROM assignments WHERE course_id = ?",
            (course_id,)
        )
        return [
            Assignment.from_row(self.cursor, r)
            for r in self.cursor.fetchall()
        ]

    def get_by_id(self, assignment_id):
        self.cursor.execute(
            "SELECT * FROM assignments WHERE assignment_id = ?",
            (assignment_id,)
        )
        row = self.cursor.fetchone()
        return Assignment.from_row(self.cursor, row)

    
    def delete(self, assignment_id):
        self.cursor.execute(
            "DELETE FROM submissions WHERE assignment_id = ?",
            (assignment_id,)
        )
        self.cursor.execute(
            "DELETE FROM assignments WHERE assignment_id = ?",
            (assignment_id,)
        )
        self.conn.commit()