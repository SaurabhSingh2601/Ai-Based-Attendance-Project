from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def check_teacher_exists(username):
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
    data = {"username": username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data or []

def create_students(new_name, face_embedding=None, voice_embedding=None):
    data = {
        "name": new_name,
        "face_embeddings": face_embedding,
        "voice_embeddings": voice_embedding
    }
    response = supabase.table("students").insert(data).execute()
    return response.data

def create_subject(subject_code, name, section, teacher_id):
    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = supabase.table("subjects").select("*,subject_students(count),attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data or []

    for sub in subjects:
        stu_list = sub.get("subject_students")
        sub["total_students"] = stu_list[0].get("count", 0) if stu_list and len(stu_list) > 0 else 0

        attendance = sub.get("attendance_logs") or []
        unique_sessions = len(set(log["timestamp"] for log in attendance if "timestamp" in log))
        sub["total_classes"] = unique_sessions

        sub.pop("subject_students", None)
        sub.pop("attendance_logs", None)

    return subjects

def enroll_student_to_subject(student_id, subject_id):
    data = {
        "student_id": student_id,
        "subject_id": subject_id
    }
    response = supabase.table("subject_students").insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id, subject_id):
    response = supabase.table("subject_students").delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data

def get_student_subjects(student_id):
    response = supabase.table("subject_students").select("*,subjects(*)").eq("student_id", student_id).execute()
    return response.data or []

def get_student_attendance(student_id):
    response = supabase.table("attendance_logs").select("*,subjects(*)").eq("student_id", student_id).execute()
    return response.data or []

def create_attendance(logs):
    formatted_logs = []
    for item in logs:
        log_copy = dict(item)
        val = log_copy.pop('is_present', None)
        if val is not None and 'ispresent' not in log_copy:
            log_copy['ispresent'] = bool(val)
        elif 'ispresent' in log_copy:
            log_copy['ispresent'] = bool(log_copy['ispresent'])
        formatted_logs.append(log_copy)
    response = supabase.table('attendance_logs').insert(formatted_logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select('*,subjects!inner(*)').eq('subjects.teacher_id', teacher_id).execute()
    return response.data or []
