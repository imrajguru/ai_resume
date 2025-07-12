import streamlit as st
import requests

API_BASE = "http://localhost:5000/api"

st.set_page_config(page_title="Candidate Evaluation", layout="wide")
st.title("🧠 AI-Powered Candidate Evaluation System")

resume_file = st.file_uploader("📄 Upload Resume (.pdf or .docx)", type=["pdf", "docx"])
audio_file = st.file_uploader("🎙️ Upload Interview Audio (.wav)", type=["wav"])
candidate_name = st.text_input("👤 Candidate Name")

if st.button("🚀 Generate Report"):
    if not resume_file and not audio_file:
        st.warning("❗ Upload at least a resume or audio file.")
        st.stop()
    if not candidate_name.strip():
        st.warning("❗ Candidate name is required.")
        st.stop()

    skills = []
    strengths = []
    weaknesses = []
    suggested_role = ""
    summary = ""

    # --- Resume Upload ---
    if resume_file:
        st.info("📁 Uploading resume...")

        resume_bytes = resume_file.read()
        resume_response = requests.post(
            f"{API_BASE}/resume/upload",
            files={"file": (resume_file.name, resume_bytes)},
        )

        if resume_response.ok:
            resume_data = resume_response.json()

            # ✅ Cleanly extract skills (string or dict)
            skills_raw = resume_data.get("skills", [])
            skills = []

            for s in skills_raw:
                if isinstance(s, dict) and "name" in s:
                    skills.append(s["name"])
                elif isinstance(s, str):
                    skills.append(s)

            strengths = resume_data.get("strengths", [])
            weaknesses = resume_data.get("weaknesses", [])
            suggested_role = resume_data.get("suggested_role", "")

            st.success(f"✅ Extracted {len(skills)} skill(s)")
        else:
            st.error("❌ Failed to parse resume.")
            st.stop()

    # --- Audio Upload ---
    if audio_file:
        st.info("🎙️ Transcribing interview...")
        audio_response = requests.post(
            f"{API_BASE}/interview/upload",
            files={"file": audio_file.getvalue()},
        )
        transcript = audio_response.json().get("text", "")

        st.info("🧠 Summarizing...")
        summary_response = requests.post(
            f"{API_BASE}/interview/summarize",
            json={"transcript": transcript},
        )
        summary = summary_response.json().get("summary", "")
        st.success("✅ Summary ready!")

    # --- Scoring ---
    st.info("📊 Scoring...")
    score_response = requests.post(
        f"{API_BASE}/report/score",
        json={"skills": skills, "summary": summary},
    )
    scores = score_response.json()
    st.success("✅ Scoring done!")

    # 🛡️ Prevent 0-score PDF
    if scores.get("final_score", 0) == 0:
        st.error("❌ No valid score returned. Check resume/audio content.")
        st.stop()

    # --- Display Insights ---
    if suggested_role:
        st.subheader("🎯 Suggested Role")
        st.info(suggested_role)

    if strengths:
        st.subheader("💪 Strengths")
        for s in strengths:
            st.success(f"• {s}")

    if weaknesses:
        st.subheader("⚠️ Weaknesses")
        for w in weaknesses:
            st.warning(f"• {w}")

    if summary:
        st.subheader("📝 Interview Summary")
        st.info(summary)

    st.subheader("📈 Scores")
    st.write(scores)

    # --- Generate PDF Report ---
    report_response = requests.post(
        f"{API_BASE}/report/report",
        json={
            "name": candidate_name,
            "skills": skills,
            "summary": summary,
            "scores": scores,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggested_role": suggested_role,
        },
    )

    if report_response.status_code == 200:
        st.success("📄 Report ready!")
        st.download_button(
            label="📥 Download Report",
            data=report_response.content,
            file_name=f"{candidate_name.replace(' ', '_')}_report.pdf",
            mime="application/pdf",
        )
    else:
        st.error("❌ Failed to generate PDF.")
