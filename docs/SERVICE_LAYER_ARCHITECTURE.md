# Service Layer Architecture

## Overview

The EduTrack application follows a **Service Layer Pattern** where:

1. **Controllers** handle HTTP requests/responses and call **Services**
2. **Services** contain business logic and call **Repositories**
3. **Repositories** handle data access (database operations)

## Architecture Flow

```
Controller → Service → Repository → Database
```

## Service Layer Responsibilities

### Business Logic
- Input validation
- Business rule enforcement
- Data transformation
- Cross-cutting concerns (notifications, logging)

### Data Access Abstraction
- Controllers never directly access repositories
- All database operations go through services
- Services coordinate multiple repositories when needed

## Service Files

### 1. AuthService (`services/auth_service.py`)
- User registration
- User authentication
- Password hashing/verification

### 2. CourseService (`services/course_service.py`)
- Course creation with validation
- Course code generation
- Student enrollment
- Course retrieval

### 3. AssignmentService (`services/assignment_service.py`)
- Assignment creation with validation
- Due date validation
- Grade validation
- Submission validation
- Notification triggers

### 4. LectureService (`services/lecture_service.py`)
- Lecture upload with file validation
- File size validation
- File type validation
- Video link validation
- Notification triggers

### 5. SubmissionService (`services/submission_service.py`)
- Submission validation
- Due date checking
- Duplicate submission prevention
- Submission retrieval with enrichment

### 6. AttendanceService (`services/attendance_service.py`)
- Attendance recording
- Student enrollment validation
- Attendance status validation
- Attendance summaries

### 7. ChatService (`services/chat_service.py`)
- Message validation
- Access control (enrollment check)
- Message length validation
- Message retrieval with enrichment

### 8. UserService (`services/user_service.py`)
- User creation with validation
- User update
- User deletion
- Password reset
- Email validation

### 9. AnnouncementService (`services/announcement_service.py`)
- Announcement creation
- Teacher authorization
- Content validation
- Notification triggers

### 10. NotificationService (`services/notification_service.py`)
- Notification creation
- Notification retrieval
- Mark as read functionality
- Unread count

## Benefits

1. **Separation of Concerns**: Business logic separated from HTTP handling
2. **Reusability**: Services can be used by multiple controllers
3. **Testability**: Services can be tested independently
4. **Maintainability**: Business rules centralized in services
5. **Consistency**: Validation and business rules applied consistently

## Example Flow

### Creating an Assignment

1. **Controller** (`controllers/assignment_controller.py`):
   - Receives HTTP POST request
   - Extracts form data
   - Calls `AssignmentService.create_assignment()`

2. **Service** (`services/assignment_service.py`):
   - Validates course exists
   - Validates due date is in future
   - Validates max grade is positive
   - Creates assignment via repository
   - Triggers notifications
   - Returns (success, message)

3. **Repository** (`repositories/assignment_repository.py`):
   - Executes SQL INSERT
   - Commits transaction

## Best Practices

1. **Services return tuples**: `(success: bool, message: str)`
2. **Services handle all validation**: Controllers just pass data
3. **Services coordinate repositories**: Multiple repos if needed
4. **Services trigger side effects**: Notifications, logging, etc.
5. **Services are stateless**: No instance variables for request data

## Migration Notes

All controllers have been refactored to:
- Remove direct repository access
- Use services for all operations
- Handle service return values (success/failure)
- Display appropriate flash messages

