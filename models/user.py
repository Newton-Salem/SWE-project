class User:
    def __init__(self, user_id, name, email, password, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password  # hashed later
        self.role = role  # student, teacher, admin

    @classmethod
    def from_row(cls, cursor, row):
        if not row:
            return None
        cols = [c[0] for c in cursor.description]
        data = dict(zip(cols, row))
        return cls(
            user_id=data.get("user_id"),
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
        )