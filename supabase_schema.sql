-- ====================================================================
-- SnapClass AI Attendance System - Supabase SQL Schema
-- Copy and paste this script into Supabase SQL Editor and click 'Run'
-- ====================================================================

-- 1. Enable UUID Extension (if needed)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Teachers Table
CREATE TABLE IF NOT EXISTS public.teachers (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Students Table
CREATE TABLE IF NOT EXISTS public.students (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    face_embeddings JSONB,
    voice_embeddings JSONB,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Subjects Table
CREATE TABLE IF NOT EXISTS public.subjects (
    id BIGSERIAL PRIMARY KEY,
    subject_code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    section TEXT,
    teacher_id BIGINT NOT NULL REFERENCES public.teachers(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 5. Subject Students Mapping (Enrollment)
CREATE TABLE IF NOT EXISTS public.subject_students (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES public.students(id) ON DELETE CASCADE,
    subject_id BIGINT NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    CONSTRAINT unique_student_subject UNIQUE (student_id, subject_id)
);

-- 6. Attendance Logs Table
CREATE TABLE IF NOT EXISTS public.attendance_logs (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES public.students(id) ON DELETE CASCADE,
    subject_id BIGINT NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
    timestamp TEXT NOT NULL,
    is_present BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ====================================================================
-- Row Level Security (RLS) Configuration
-- For development / direct client access via publishable key:
-- ====================================================================
ALTER TABLE public.teachers DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.students DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.subjects DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.subject_students DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.attendance_logs DISABLE ROW LEVEL SECURITY;

-- Optional: If you ever enable RLS, allow full access to anon:
-- ALTER TABLE public.teachers ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Allow public full access" ON public.teachers FOR ALL USING (true) WITH CHECK (true);
-- CREATE POLICY "Allow public full access" ON public.students FOR ALL USING (true) WITH CHECK (true);
-- CREATE POLICY "Allow public full access" ON public.subjects FOR ALL USING (true) WITH CHECK (true);
-- CREATE POLICY "Allow public full access" ON public.subject_students FOR ALL USING (true) WITH CHECK (true);
-- CREATE POLICY "Allow public full access" ON public.attendance_logs FOR ALL USING (true) WITH CHECK (true);
