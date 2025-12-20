from models import row_to_dict

class User:
    def __init__(self, user_id, name, email, password, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password  
        self.role = role  

    @classmethod
    def from_row(cls, cursor, row):
        data = row_to_dict(cursor, row)
        if not data:
            return None
        return cls(
            user_id=data.get("user_id"),
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
        )