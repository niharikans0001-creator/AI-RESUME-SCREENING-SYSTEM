from flask import Flask, render_template, request , redirect
import os
from werkzeug.utils import secure_filename
from resume_parser import extract_resume_text, guess_candidate_name 
from skills import extract_skills
from matcher import calculate_match_score   
from database import init_db, save_screening, get_screening_history, clear_screening_history

app = Flask(__name__) 

# Folder where uploaded resumes will be stored
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/history")
def history():
    screening_history = get_screening_history()

    total_candidates = len(screening_history)

    if total_candidates > 0:
        scores = [float(record[2]) for record in screening_history]

        average_score = round(sum(scores) / total_candidates, 1)
        best_score = max(scores)

        best_record = max(
            screening_history,
            key=lambda record: float(record[2])
        )


        best_candidate = best_record[1]

    else:
        average_score = 0
        best_score = 0
        best_candidate = "N/A"

    return render_template(
        "history.html",
        history=screening_history,
        total_candidates=total_candidates,
        average_score=average_score,
        best_score=best_score,
        best_candidate=best_candidate
    )
@app.route("/clear-history", methods=["POST"])
def clear_history():
    clear_screening_history()
    return redirect("/history")  


@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return "No resume selected"

    file = request.files["resume"]

    if file.filename == "":
        return "No resume selected"

    allowed_extensions = [".pdf", ".docx"]
    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        return "Only PDF and DOCX files are allowed"

    job_description = request.form.get("job_description", "")

    filename = secure_filename(file.filename)

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(file_path)

    resume_text = extract_resume_text(file_path)
    candidate_name = guess_candidate_name(resume_text)

    detected_skills = extract_skills(resume_text)
    match_score, required_skills, matched_skills = calculate_match_score(
        detected_skills,
        job_description,
        extract_skills
    )
    missing_skills = [
        skill for skill in required_skills
        if skill not in matched_skills
    ]
    if match_score >= 80:
        match_status = "Strong Match"
    elif match_score >= 50:
        match_status = "Moderate Match"
    else:
        match_status = "Low Match"

    save_screening(
        candidate_name,
        match_score,
        matched_skills,
        missing_skills
    )
    return render_template(
        "result.html",
        candidate_name=candidate_name,
        score=match_score,
        match_status=match_status, 
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        resume_skills=detected_skills,
    ) 
    


init_db()

if __name__ == "__main__":
    app.run(debug=True)