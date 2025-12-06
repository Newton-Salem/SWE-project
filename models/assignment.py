class Assignment:
    def _init_(self, assignment_id, course_id, title, description, due_date, max_grade):
        self.assignment_id = assignment_id
        self.course_id = course_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.max_grade = max_grade