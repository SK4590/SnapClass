<p align="center">
  <img src="https://i.ibb.co/YTYGn5qV/logo.png" alt="SnapClass Logo" width="100" />
</p>

<h1 align="center">SnapClass – AI-Powered Smart Attendance System</h1>

<p align="center">
  <b>An intelligent, full-stack biometric attendance management system</b><br>
  Built with <b>Streamlit</b>, <b>Supabase (PostgreSQL)</b>, and <b>Computer Vision (dlib / Face Recognition)</b>
</p>

SnapClass replaces cumbersome manual paper attendance and roll calls with instant facial recognition and QR-code enrollment.

---

## ✨ Features

### 👨‍🏫 Teacher Portal
- **Secure Authentication**: Encrypted password authentication powered by `bcrypt`.
- **Course & Subject Management**: Create courses with subject codes, course titles, and sections.
- **QR Code & Link Generation**: Instantly generate scannable QR codes (powered by `segno`) and direct URLs for class enrollment.
- **AI Classroom Attendance**:
  - Live webcam snapshots or multi-file photo uploads.
  - Multi-face detection scanning all students in the classroom simultaneously.
  - Visual attendance review dialog with confirm/discard actions before syncing to database.
- **Voice Attendance (Optional)**: Audio phrase recognition module for voice roll call.
- **Analytics & Reporting**:
  - Session timestamps and present/absent student breakdown.
  - Per-student attendance percentages and historical logs.

### 🎓 Student Portal
- **FaceID Login**: Frictionless authentication by looking directly at the camera (128-dimensional facial embeddings).
- **One-Shot Biometric Registration**: Automatically registers face embeddings for new students.
- **Course Enrollment**:
  - Quick QR scan auto-enrollment via URL query parameters (`?join-code=...`).
  - Manual enrollment modal using course codes.
- **Student Dashboard**:
  - Enrolled course cards with total sessions held, classes attended, and attendance rates.
  - Course unenrollment option.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend & UI** | Streamlit, Custom Vanilla CSS, Google Fonts (*Climate Crisis*, *Outfit*) |
| **Database** | Supabase (PostgreSQL) |
| **Computer Vision / AI** | `dlib`, `face_recognition_models`, `scikit-learn`, `numpy` |
| **Security & Auth** | `bcrypt` (Salted Password Hashing) |
| **QR Code Engine** | `segno` |
| **Image Processing** | `Pillow` (PIL) |

---

## 📂 Project Structure

```
SnapClass/
├── .streamlit/
│   ├── secrets.toml            # Private Supabase credentials (git-ignored)
│   └── secrets.toml.example    # Configuration template
├── src/
│   ├── components/
│   │   ├── dialog_add_photo.py          # Camera & upload modal for classroom photos
│   │   ├── dialog_attendance_results.py # Attendance review & sync dialog
│   │   ├── dialog_auto_enroll.py        # One-click QR code link enrollment
│   │   ├── dialog_create_subject.py     # Teacher course creation dialog
│   │   ├── dialog_enroll.py             # Student manual course enrollment
│   │   ├── dialog_share_subject.py      # QR code generator dialog
│   │   ├── dialog_voice_attendance.py   # Voice attendance audio modal
│   │   ├── footer.py                    # App footer components
│   │   ├── header.py                    # Branding headers & logos
│   │   └── subject_card.py              # Subject card widget with custom stats
│   ├── database/
│   │   ├── config.py           # Supabase client instantiation
│   │   └── db.py               # Complete CRUD and authentication layer
│   ├── pipelines/
│   │   ├── face_pipeline.py    # dlib face detection & 128-d Euclidean matcher
│   │   └── voice_pipeline.py   # Speaker similarity audio pipeline
│   ├── screens/
│   │   ├── home_screen.py      # Role selection landing page
│   │   ├── student_screen.py   # Student FaceID login & dashboard
│   │   └── teacher_screen.py   # Teacher login, management & analytics
│   └── ui/
│       └── style_base_layout.py # Custom CSS styling & typography
├── app.py                      # Main entrypoint & session router
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Documentation
```

---

## 🗄️ Database Schema (Supabase SQL)

To initialize the database in your Supabase project, execute the following SQL in your **Supabase SQL Editor**:

```sql
-- 1. Teachers table
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Students table
CREATE TABLE IF NOT EXISTS students (
    student_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    face_embedding JSONB,
    voice_embedding JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Subjects table
CREATE TABLE IF NOT EXISTS subjects (
    subject_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    section TEXT NOT NULL,
    teacher_id UUID REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Course enrollment table
CREATE TABLE IF NOT EXISTS subject_students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id UUID REFERENCES subjects(subject_id) ON DELETE CASCADE,
    UNIQUE(student_id, subject_id)
);

-- 5. Attendance logs table
CREATE TABLE IF NOT EXISTS attendance_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id UUID REFERENCES subjects(subject_id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    is_present BOOLEAN DEFAULT FALSE
);
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/SK4590/SnapClass.git
cd SnapClass
```

### 2. Set up virtual environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Supabase Credentials
Create a `.streamlit/secrets.toml` file in the root directory:
```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
```

### 5. Launch the Application
```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

---

## 💡 How It Works

1. **Course Setup**: A teacher logs in, creates a subject (e.g. `CS101`), and generates a **QR Code** for students to join.
2. **Student Onboarding**: Students scan the QR code or navigate to the Student Portal. Looking into the webcam registers their face embedding.
3. **Taking Attendance**:
   - The teacher uploads or snaps a photo of the classroom.
   - The AI pipeline locates every face, extracts 128-dimensional facial descriptors, and compares them against enrolled students.
   - Present students are automatically recognized and recorded into Supabase with session timestamps.
4. **Insights**: Both teachers and students can view attendance rates and analytics instantly.
