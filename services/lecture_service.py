from repositories.repository_factory import RepositoryFactory
from services.notification_service import NotificationService
from repositories.enrollment_repository import EnrollmentRepository
from datetime import date
import os
import uuid


class LectureService:
    def __init__(self):
        self.lecture_repo = RepositoryFactory.get("lecture")
        self.course_repo = RepositoryFactory.get("course")
        self.enrollment_repo = EnrollmentRepository()
        self.notification_service = NotificationService()

    # ==================================================
    # ================= UPLOAD LECTURE =================
    # ==================================================
    def upload_lecture(
        self,
        course_id,
        title,
        file_path,
        video_link,
        upload_folder,
        max_file_size=10 * 1024 * 1024
    ):
        # ---------- Validate course ----------
        course = self.course_repo.get_by_id(course_id)
        if not course:
            return False, "Course not found"

        # ---------- Validate title ----------
        if not title or not title.strip():
            return False, "Title is required"

        # ---------- Validate input ----------
        if not file_path and not video_link:
            return False, "Either a file or video link must be provided"

        # ---------- Validate file ----------
        if file_path:
            full_path = os.path.join(upload_folder, os.path.basename(file_path))

            if not os.path.exists(full_path):
                return False, "File not found"

            file_size = os.path.getsize(full_path)
            if file_size > max_file_size:
                return False, "File too large"

            if not file_path.lower().endswith(".pdf"):
                return False, "Only PDF files are allowed"

        # ---------- Validate video link ----------
        if video_link and not video_link.startswith(("http://", "https://")):
            return False, "Invalid video link"

        # ---------- Save lecture ----------
        lecture_id = self.lecture_repo.add_lecture(
            course_id,
            title,
            file_path,
            video_link,
            date.today()
        )

        # ---------- Notify students ----------
        students = self.enrollment_repo.get_enrolled_students(course_id)

        for s in students:
            self.notification_service.create_notification(
                s.user_id,
                f"New lecture '{title}' uploaded in {course.title}",
                "lecture",
                lecture_id
            )

        return True, "Lecture uploaded successfully"

    # ==================================================
    # ================= DELETE LECTURE =================
    # ==================================================
    def delete_lecture(self, lecture_id):
        lecture = self.lecture_repo.get_by_id(lecture_id)
        if not lecture:
            return False, "Lecture not found"

        if lecture.file_path:
            file_path = os.path.join("src", "static", lecture.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)

        self.lecture_repo.delete(lecture_id)
        return True, "Lecture deleted successfully"

    # ==================================================
    # ================= EDIT LECTURE ===================
    # ==================================================
    def edit_lecture(self, lecture_id, title, video_link):
        lecture = self.lecture_repo.get_by_id(lecture_id)
        if not lecture:
            return False, "Lecture not found"

        if not title or not title.strip():
            return False, "Title is required"

        self.lecture_repo.update(
            lecture_id,
            title,
            video_link
        )
        return True, "Lecture updated successfully"

    # ==================================================
    # ================= READ METHODS ===================
    # ==================================================
    def get_lectures_by_course(self, course_id):
        return self.lecture_repo.get_by_course(course_id)

    def get_lecture_by_id(self, lecture_id):
        return self.lecture_repo.get_by_id(lecture_id)

    # ==================================================
    # ================= FILE HANDLING ==================
    # ==================================================
    def save_uploaded_file(self, file, upload_folder):
        os.makedirs(upload_folder, exist_ok=True)

        filename = f"{uuid.uuid4()}_{file.filename}"
        full_path = os.path.join(upload_folder, filename)
        file.save(full_path)

        return f"uploads/{filename}"
