from fpdf import FPDF
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)  # ✅ Add Unicode font
        self.set_font("DejaVu", "", 12)

    def header(self):
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, "Candidate Evaluation Report", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(name, skills, summary, scores, save_path,
                 strengths=None, weaknesses=None, suggested_role=None):

    pdf = PDFReport()
    pdf.add_page()

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, f"Candidate: {name}", ln=True)

    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 10, "Evaluation Scores:", ln=True)
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 10, f"Resume Score: {scores.get('resume_score', 0)}%", ln=True)
    pdf.cell(0, 10, f"Summary Score: {scores.get('summary_score', 0)}%", ln=True)
    pdf.cell(0, 10, f"Final Score: {scores.get('final_score', 0)}%", ln=True)
    pdf.ln(5)

    if suggested_role:
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Suggested Role:", ln=True)
        pdf.set_font("DejaVu", "", 11)
        pdf.multi_cell(0, 8, suggested_role)
        pdf.ln(5)

    if strengths:
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Strengths:", ln=True)
        pdf.set_font("DejaVu", "", 11)
        for s in strengths:
            pdf.cell(0, 8, f"• {s}", ln=True)
        pdf.ln(5)

    if weaknesses:
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Weaknesses:", ln=True)
        pdf.set_font("DejaVu", "", 11)
        for w in weaknesses:
            pdf.cell(0, 8, f"• {w}", ln=True)
        pdf.ln(5)

    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 10, "Extracted Skills:", ln=True)
    pdf.set_font("DejaVu", "", 11)
    if skills:
        for skill in skills:
            pdf.cell(0, 8, f"• {skill}", ln=True)
    else:
        pdf.cell(0, 8, "No skills extracted.", ln=True)
    pdf.ln(5)

    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 10, "Interview Summary:", ln=True)
    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(0, 8, summary if summary else "N/A")

    # Score chart
    chart_path = "static/chart.png"
    plt.figure(figsize=(4, 3))
    plt.bar(scores.keys(), scores.values(), color="steelblue")
    plt.title("Score Breakdown")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    pdf.image(chart_path, x=pdf.get_x(), y=pdf.get_y(), w=150)
    os.remove(chart_path)

    pdf.output(save_path)
