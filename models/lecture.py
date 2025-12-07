
class Lecture:
    def __init__(self, lecture_id, course_id, title, file_path, video_link, upload_date):
        self.lecture_id = lecture_id
        self.course_id = course_id
        self.title = title
        self.file_path = file_path
        self.video_link = video_link
        self.upload_date = upload_date

    @classmethod
    def from_row(cls, cursor, row):
        if not row:
            return None
        cols = [c[0] for c in cursor.description]
        data = dict(zip(cols, row))
        return cls(
            lecture_id=data.get("lecture_id"),
            course_id=data.get("course_id"),
            title=data.get("title"),
            file_path=data.get("file_path"),
            video_link=data.get("video_link"),
            upload_date=data.get("upload_date"),
        )
