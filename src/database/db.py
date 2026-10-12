import bcrypt
from src.database.config import supabase


def hash_pass(pwd: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_pass(pwd: str, hashed: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return bcrypt.checkpw(pwd.encode("utf-8"), hashed.encode("utf-8"))


def check_teacher_exists(username: str) -> bool:
    """Check if a teacher with the given username already exists."""
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


def create_teacher(username: str, password: str, name: str):
    """Create a new teacher in Supabase."""
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name,
    }
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username: str, password: str):
    """Authenticate teacher with username and password."""
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher.get("password", "")):
            return teacher
    return None


def get_all_students():
    """Fetch all students from Supabase."""
    response = supabase.table("students").select("*").execute()
    return response.data


def create_student(new_name: str, face_embedding=None, voice_embedding=None):
    """Register a new student with optional face/voice embeddings."""
    data = {
        "name": new_name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding,
    }
    response = supabase.table("students").insert(data).execute()
    return response.data


def create_subject(subject_code: str, name: str, section: str, teacher_id: str):
    """Create a new subject for a teacher."""
    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id,
    }
    response = supabase.table("subjects").insert(data).execute()
    return response.data


def get_teacher_subjects(teacher_id: str):
    """Fetch all subjects created by teacher, along with student count and class sessions."""
    response = (
        supabase.table("subjects")
        .select("*, subject_students(count), attendance_logs(timestamp)")
        .eq("teacher_id", teacher_id)
        .execute()
    )
    subjects = response.data

    for sub in subjects:
        sub["total_students"] = (
            sub.get("subject_students", [{}])[0].get("count", 0)
            if sub.get("subject_students")
            else 0
        )
        attendance = sub.get("attendance_logs", [])
        unique_sessions = len(set(log["timestamp"] for log in attendance))
        sub["total_classes"] = unique_sessions

        sub.pop("subject_students", None)
        sub.pop("attendance_logs", None)

    return subjects


def enroll_student_to_subject(student_id: str, subject_id: str):
    """Enroll a student into a subject."""
    data = {"student_id": student_id, "subject_id": subject_id}
    response = supabase.table("subject_students").insert(data).execute()
    return response.data


def unenroll_student_to_subject(student_id: str, subject_id: str):
    """Unenroll a student from a subject."""
    response = (
        supabase.table("subject_students")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )
    return response.data


def get_student_subjects(student_id: str):
    """Fetch subjects enrolled by a student."""
    response = (
        supabase.table("subject_students")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )
    return response.data


def get_student_attendance(student_id: str):
    """Fetch attendance records for a student."""
    response = (
        supabase.table("attendance_logs")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )
    return response.data


def create_attendance(logs: list):
    """Batch insert attendance log records."""
    response = supabase.table("attendance_logs").insert(logs).execute()
    return response.data


def get_attendance_for_teacher(teacher_id: str):
    """Fetch all attendance records for teacher's subjects."""
    response = (
        supabase.table("attendance_logs")
        .select("*, subjects!inner(*), students!inner(*)")
        .eq("subjects.teacher_id", teacher_id)
        .execute()
    )
    return response.data
