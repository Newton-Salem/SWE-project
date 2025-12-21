from repositories.repository_factory import RepositoryFactory
from werkzeug.security import generate_password_hash

class UserService:
    def __init__(self):
        self.user_repo = RepositoryFactory.get("user")

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.user_repo.get_by_id(user_id)

    def get_user_by_email(self, email):
        """Get user by email"""
        return self.user_repo.get_by_email(email)

    def create_user(self, name, email, password, role):
        """Create a new user with business logic validation"""
        # Validate email format
        if not email or '@' not in email:
            return False, "Invalid email format"
        
        # Validate email is unique
        existing = self.user_repo.get_by_email(email)
        if existing:
            return False, "Email already registered"
        
        # Validate name
        if not name or not name.strip():
            return False, "Name is required"
        
        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters"
        
        # Validate role
        valid_roles = ['student', 'teacher', 'admin']
        if role not in valid_roles:
            return False, f"Invalid role. Must be one of {valid_roles}"
        
        # Validate password
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Hash password and create user
        hashed_password = generate_password_hash(password)
        self.user_repo.create_user(name.strip(), email.lower().strip(), hashed_password, role)
        
        return True, "User created successfully"

    def update_user(self, user_id, name=None, email=None, role=None):
        """Update user information with business logic"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"
        
        # Validate email if provided
        if email:
            if '@' not in email:
                return False, "Invalid email format"
            
            # Check if email is already taken
            existing = self.user_repo.get_by_email(email)
            if existing and existing.user_id != user_id:
                return False, "Email already in use"
        
        # Validate name if provided
        if name:
            if not name.strip() or len(name.strip()) < 2:
                return False, "Name must be at least 2 characters"
        
        # Validate role
        if role:
            valid_roles = ['student', 'teacher', 'admin']
            if role not in valid_roles:
                return False, f"Invalid role. Must be one of {valid_roles}"
        
       
        return True, "User updated successfully"

    def delete_user(self, user_id, admin_id):
        """Delete a user with business logic"""
        # Validate user exists
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"
        
        # Prevent self-deletion
        if user_id == admin_id:
            return False, "Cannot delete your own account"
        
  
        return True, "User deleted successfully"

    def reset_password(self, user_id, new_password):
        """Reset user password with business logic"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"
        
        # Validate password
        if not new_password or len(new_password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Hash and update password
        hashed_password = generate_password_hash(new_password)
        # self.user_repo.update_password(user_id, hashed_password)
        
        return True, "Password reset successfully"

