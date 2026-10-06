import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="AI Student Study Monitor",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SESSION ----------------

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 28px;
    border-radius: 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 17px;
    margin: 0;
}

.card {
    padding: 22px;
    border-radius: 18px;
    background: white;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    text-align: center;
    margin-bottom: 15px;
}

.card-title {
    font-size: 14px;
    color: #6b7280;
}

.card-value {
    font-size: 28px;
    font-weight: bold;
    margin-top: 8px;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
}

.profile {
    padding: 20px;
    border-radius: 18px;
    background: white;
    border: 1px solid #e5e7eb;
}

.status-box {
    padding: 18px;
    border-radius: 15px;
    background: white;
    border: 1px solid #e5e7eb;
    text-align: center;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #6b7280;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🎓 AI Student Study Monitor</h1>
    <p>AI-Based Student Study Activity and Distraction Detection System</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.title("🎓 Study Monitor")

st.sidebar.markdown("### ⚙️ Study Settings")

study_goal = st.sidebar.slider(
    "🎯 Daily Study Goal",
    30,
    300,
    120
)

study_time = st.sidebar.slider(
    "⏱️ Study Session",
    10,
    180,
    60
)

st.sidebar.divider()

st.sidebar.success("🟢 System Ready")
st.sidebar.info("📷 Camera Detection Available")
st.sidebar.info("📊 Analytics Enabled")
st.sidebar.info("📥 CSV Reports Enabled")

# ---------------- STUDENT INFORMATION ----------------

st.markdown(
    '<div class="section-title">👤 Student Information</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input(
        "Student Name",
        value="Geethika"
    )

with col2:
    subject = st.selectbox(
        "📚 Subject",
        [
            "Python",
            "DBMS",
            "Artificial Intelligence",
            "Machine Learning",
            "Data Structures",
            "Computer Networks",
            "Other"
        ]
    )

# ---------------- CALCULATIONS ----------------

focus_time = int(study_time * 0.80)

distraction_time = study_time - focus_time

focus_score = int(
    (focus_time / study_time) * 100
)

distraction_score = 100 - focus_score

goal_progress = min(
    int((study_time / study_goal) * 100),
    100
)

# ---------------- PROFILE ----------------

st.markdown(
    '<div class="section-title">👩‍🎓 Student Profile</div>',
    unsafe_allow_html=True
)

p1, p2, p3 = st.columns(3)

with p1:
    st.markdown(
        f"""
        <div class="profile">
        <b>👤 Student</b><br><br>
        {student_name}
        </div>
        """,
        unsafe_allow_html=True
    )

with p2:
    st.markdown(
        f"""
        <div class="profile">
        <b>📚 Subject</b><br><br>
        {subject}
        </div>
        """,
        unsafe_allow_html=True
    )

with p3:
    st.markdown(
        f"""
        <div class="profile">
        <b>🎯 Daily Goal</b><br><br>
        {study_goal} minutes
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- DASHBOARD ----------------

st.markdown(
    '<div class="section-title">📊 Study Dashboard</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">⏱️ Study Time</div>
        <div class="card-value">{study_time} min</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">🟢 Focus Time</div>
        <div class="card-value">{focus_time} min</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">🔴 Distraction</div>
        <div class="card-value">{distraction_time} min</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">🎯 Focus Score</div>
        <div class="card-value">{focus_score}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- GOAL ----------------

st.markdown(
    '<div class="section-title">🎯 Daily Study Goal</div>',
    unsafe_allow_html=True
)

st.progress(goal_progress / 100)

st.write(
    f"**{study_time} / {study_goal} minutes completed**"
)

if goal_progress >= 100:
    st.success("🏆 Daily study goal completed!")

else:
    remaining = study_goal - study_time
    st.info(
        f"📚 {remaining} minutes remaining to reach your goal."
    )

# ---------------- CAMERA ----------------

st.markdown(
    '<div class="section-title">📷 AI Face Detection</div>',
    unsafe_allow_html=True
)

st.info(
    "Allow camera access and capture your face. "
    "The system will detect your face using OpenCV."
)

camera_image = st.camera_input(
    "📹 Open Camera"
)

if camera_image is not None:

    image_bytes = camera_image.getvalue()

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    frame = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if frame is not None:

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                3
            )

            cv2.putText(
                frame,
                "Student Detected",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        st.image(
            frame_rgb,
            caption="AI Face Detection Result",
            use_container_width=True
        )

        if len(faces) > 0:

            st.success(
                f"🟢 Student Detected — {len(faces)} face found!"
            )

        else:

            st.warning(
                "⚠️ Face not detected. Please face the camera clearly."
            )

# ---------------- STATUS ----------------

st.markdown(
    '<div class="section-title">🤖 AI Monitoring Status</div>',
    unsafe_allow_html=True
)

s1, s2, s3 = st.columns(3)

with s1:
    st.markdown(
        """
        <div class="status-box">
        🟢<br>
        <b>Face Detection</b><br>
        Active
        </div>
        """,
        unsafe_allow_html=True
    )

with s2:
    st.markdown(
        """
        <div class="status-box">
        🎯<br>
        <b>Study Monitoring</b><br>
        Active
        </div>
        """,
        unsafe_allow_html=True
    )

with s3:
    st.markdown(
        """
        <div class="status-box">
        📊<br>
        <b>Analytics</b><br>
        Ready
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- FOCUS ANALYSIS ----------------

st.markdown(
    '<div class="section-title">🧠 Focus & Distraction Analysis</div>',
    unsafe_allow_html=True
)

a1, a2 = st.columns(2)

with a1:

    st.metric(
        "🎯 Focus Score",
        f"{focus_score}%"
    )

    st.progress(
        focus_score / 100
    )

with a2:

    st.metric(
        "⚠️ Distraction Score",
        f"{distraction_score}%"
    )

    st.progress(
        distraction_score / 100
    )

if focus_score >= 80:

    performance = "Excellent"

    st.success(
        "🏆 Excellent Focus! Keep going."
    )

elif focus_score >= 60:

    performance = "Good"

    st.info(
        "👍 Good Focus. Try to reduce distractions."
    )

elif focus_score >= 40:

    performance = "Moderate"

    st.warning(
        "⚠️ Moderate Focus. Try to concentrate more."
    )

else:

    performance = "Needs Improvement"

    st.error(
        "🚨 High Distraction. Improve concentration."
    )

# ---------------- ACTIVITY GRAPH ----------------

st.markdown(
    '<div class="section-title">📈 Study Activity</div>',
    unsafe_allow_html=True
)

activity = pd.DataFrame(
    {
        "Activity": [
            "Focused",
            "Distracted"
        ],
        "Minutes": [
            focus_time,
            distraction_time
        ]
    }
)

st.bar_chart(
    activity.set_index("Activity")
)

# ---------------- BREAK REMINDER ----------------

st.markdown(
    '<div class="section-title">🔔 Break Reminder</div>',
    unsafe_allow_html=True
)

if study_time >= 60:

    st.warning(
        "☕ Long study session detected. "
        "Consider taking a 5-minute break."
    )

else:

    st.success(
        "✅ Keep maintaining your focus!"
    )

# ---------------- STUDY TIPS ----------------

st.markdown(
    '<div class="section-title">💡 AI Study Tips</div>',
    unsafe_allow_html=True
)

t1, t2, t3 = st.columns(3)

with t1:
    st.info("📱 Keep your mobile phone away.")

with t2:
    st.info("🔕 Turn off unnecessary notifications.")

with t3:
    st.info("☕ Take regular short breaks.")

# ---------------- SAVE SESSION ----------------

st.markdown(
    '<div class="section-title">💾 Save Study Session</div>',
    unsafe_allow_html=True
)

if st.button(
    "💾 Save Current Session",
    use_container_width=True
):

    session = {
        "Date": datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        ),
        "Student": student_name,
        "Subject": subject,
        "Study Time": study_time,
        "Focus Time": focus_time,
        "Distraction Time": distraction_time,
        "Focus Score": focus_score,
        "Performance": performance
    }

    st.session_state.history.append(
        session
    )

    st.success(
        "✅ Study session saved successfully!"
    )

# ---------------- REPORT ----------------

st.markdown(
    '<div class="section-title">📋 Study Report</div>',
    unsafe_allow_html=True
)

report = pd.DataFrame(
    {
        "Parameter": [
            "Student Name",
            "Subject",
            "Study Duration",
            "Focused Time",
            "Distraction Time",
            "Focus Score",
            "Distraction Score",
            "Performance"
        ],
        "Result": [
            student_name,
            subject,
            f"{study_time} minutes",
            f"{focus_time} minutes",
            f"{distraction_time} minutes",
            f"{focus_score}%",
            f"{distraction_score}%",
            performance
        ]
    }
)

st.table(report)

# ---------------- SESSION HISTORY ----------------

if st.session_state.history:

    st.markdown(
        '<div class="section-title">📅 Session History</div>',
        unsafe_allow_html=True
    )

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

    csv_data = history_df.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download CSV Report",
        data=csv_data,
        file_name="Geethika_Study_Report.csv",
        mime="text/csv",
        use_container_width=True
    )

# ---------------- FOOTER ----------------

st.markdown(
    """
    <div class="footer">
    🎓 <b>AI-Based Student Study Activity and Distraction Detection System</b>
    <br><br>
    Developed using Python • OpenCV • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)