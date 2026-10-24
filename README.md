# 🎓 SnapClass - AI-Based Smart Attendance System

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E.svg)](https://supabase.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-Deployable-46E3B7.svg)](https://render.com/)

**SnapClass** is a modern, full-stack AI attendance management platform designed to replace manual roll calls. It automates student verification using **Biometric Face Recognition** and **Voice Speaker Identification**, saving class time and eliminating proxy attendance.

---

## 🌟 Key Features

### 👨‍🏫 Teacher Portal
- **Secure Authentication**: Teacher registration and password login with salted `bcrypt` hashing.
- **Subject Management**: Create courses/sections and view real-time class stats (enrolled students, total classes conducted).
- **Shareable Join Codes & QR Codes**: Generate instant QR codes and shareable links for student self-enrollment.
- **AI Classroom Photo Attendance**: Capture or upload classroom photos. The system detects multiple faces simultaneously, extracts high-dimensional biometric descriptors with `dlib`, and predicts attendance using machine learning models.
- **Voice Attendance**: Record classroom audio of students saying roll calls or phrases, split utterances, and match against enrolled student voice profiles using deep speaker embeddings.
- **Attendance Records & Analytics**: Grouped attendance session history with presence rates and exportable logs.

### 🧑‍🎓 Student Portal
- **FaceID Login**: Sign in instantly using your webcam without typing passwords.
- **Biometric Profile Registration**: 
  - Captures face embeddings (128-dimensional biometric vectors).
  - Optional voice enrollment using `Resemblyzer`.
- **Subject Enrollment**: Join courses directly using teacher join codes or QR link parameters (`?join-code=...`).
- **Student Dashboard**: View enrolled courses, class attendance counts, and unenroll with one click.

---

## 🛠️ Tech Stack & Architecture

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/) with customized UI layout & CSS.
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL with relational foreign keys and JSONB embedding storage).
- **Computer Vision Pipeline**:
  - `dlib`: Frontal face detector & 68-point shape predictor.
  - `face_recognition_models`: Pretrained ResNet face recognition model.
  - `scikit-learn`: Linear Support Vector Classifier (SVC) & Nearest Neighbor Euclidean distance matching.
- **Audio Processing Pipeline**:
  - `librosa`: Audio loading, sample rate conversion, and silence trimming.
  - `resemblyzer`: Deep voice encoder model generating voice embeddings.
- **Deployment**: `Docker` multi-stage containerization & `Render` Cloud Web Services.

---

## 🗄️ Database Setup (Supabase)

The project includes an SQL migration script: [`supabase_schema.sql`](./supabase_schema.sql).

### Steps to configure Supabase:
1. Go to your [Supabase Dashboard](https://supabase.com/dashboard) and create a new project.
2. In the left sidebar, click on **SQL Editor** -> **New Query**.
3. Open [`supabase_schema.sql`](./supabase_schema.sql), copy all contents, paste into the editor, and click **Run**.
4. The following tables will be created automatically:
   - `teachers`: Stores teacher accounts and password hashes.
   - `students`: Stores student names, 128D face embeddings, and voice embeddings.
   - `subjects`: Courses created by teachers with unique subject codes.
   - `subject_students`: Relational mapping table for student course enrollments.
   - `attendance_logs`: Logs every student's timestamped attendance status.

---

## 💻 Local Installation & Setup

### Prerequisites
- Python 3.10 or 3.11 installed.
- Git installed.
- Webcam and microphone (for testing biometrics).

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Ai-Based-Attendance-Project.git
cd Ai-Based-Attendance-Project
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

> **Note for Windows Users**: `requirements.txt` is configured with environment markers (`dlib-bin; sys_platform == 'win32'`) so that pre-compiled dlib wheels install cleanly without requiring C++ build tools.

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_publishable_or_anon_key
```

### 5. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🚀 Deployment on Render (via Docker)

Because this application relies on C++ libraries (`dlib`, `cmake`, and audio codecs), **Docker deployment on Render** is the recommended, zero-configuration method.

### Step 1: Push Code to GitHub
Ensure all files including `Dockerfile`, `.dockerignore`, `render.yaml`, and `requirements.txt` are committed:
```bash
git add .
git commit -m "Configure production database and Render deployment"
git push origin main
```

### Step 2: Create Web Service on Render
1. Log in to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository (`Ai-Based-Attendance-Project`).

### Step 3: Configure Settings
- **Name**: `snapclass-ai-attendance`
- **Region**: Closest to you (e.g., *Singapore* or *Frankfurt*)
- **Runtime**: **Docker** *(Render detects the included `Dockerfile` automatically)*
- **Instance Type**: **Free**

### Step 4: Add Environment Variables
In the **Environment Variables** section on Render, add:
| Key | Value | Description |
|---|---|---|
| `SUPABASE_URL` | `https://your-project.supabase.co` | Your Supabase Project URL |
| `SUPABASE_KEY` | `your_supabase_key` | Your Supabase Anon/Publishable API Key |
| `PORT` | `8501` | Port exposed by Streamlit |

### Step 5: Deploy
Click **Deploy Web Service**. Render will build the Docker container and provide a live URL (e.g., `https://snapclass-ai-attendance.onrender.com`).

---

## 📂 Project Directory Structure

```text
Ai-Based-Attendance-Project/
├── .dockerignore                  # Files excluded from Docker builds
├── .env                           # Local environment credentials (git-ignored)
├── .gitignore                     # Git ignore rules
├── Dockerfile                     # Production Linux container for Render
├── README.md                      # Project documentation
├── render.yaml                    # Render Blueprint configuration
├── requirements.txt               # Cross-platform Python dependencies
├── supabase_schema.sql            # Supabase PostgreSQL schema script
├── app.py                         # Streamlit entry point and routing
└── src/
    ├── components/                # Reusable UI dialogs and widgets
    │   ├── dialog_add_photo.py    # Photo capture and file uploader dialog
    │   ├── dialog_attendance_results.py # Attendance confirmation modal
    │   ├── dialog_auto_enroll.py  # Query-param auto-enrollment modal
    │   ├── dialog_create_subject.py # Teacher subject creation modal
    │   ├── dialog_enroll.py       # Student manual code enrollment
    │   ├── dialog_share_subject.py# Subject code and QR code generator
    │   ├── dialog_voice_attendance.py # Voice attendance recording modal
    │   ├── footer.py              # Custom footer
    │   ├── header.py              # Header logo and title
    │   └── subject_card.py        # Course information card component
    ├── database/
    │   ├── config.py              # Supabase client initialization
    │   └── db.py                  # Database CRUD helper functions
    ├── pipelines/
    │   ├── face_pipeline.py       # dlib face detection & SVM classifier
    │   └── voice_pipeline.py      # Resemblyzer audio embedding & speaker matching
    ├── screens/
    │   ├── home_screen.py         # Landing screen (role selector)
    │   ├── student_screen.py      # Student dashboard & FaceID login
    │   └── teacher_screen.py      # Teacher dashboard, attendance, & reports
    └── ui/
        └── base_layout.py         # Global styling and CSS themes
```

---

## ❓ Troubleshooting

1. **Camera Not Loading in Browser**:
   Ensure you grant camera and microphone permissions in your browser. When running locally, Streamlit uses `http://localhost:8501`. On Render, camera access requires an `https://` domain (which Render provides automatically).

2. **Supabase "Invalid API key" or "Connect Error"**:
   Check that your `SUPABASE_URL` and `SUPABASE_KEY` in `.env` match the credentials in your Supabase project settings (*Project Settings -> API*).

3. **Face Recognition with Single Student**:
   The facial recognition pipeline automatically switches between Support Vector Machines (when $\ge 2$ classes exist) and Euclidean nearest-neighbor distance matching (when only 1 student is enrolled), ensuring recognition works even with a small test database.

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
