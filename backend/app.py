from flask import Flask
from flask_cors import CORS

from controllers.report_controller import report_bp
from controllers.resume_controller import resume_bp
from controllers.interview_controller import interview_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(resume_bp, url_prefix='/api/resume')
app.register_blueprint(interview_bp, url_prefix='/api/interview')
app.register_blueprint(report_bp, url_prefix='/api/report')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
