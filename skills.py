import re
SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "flask",
    "django",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "git",
    "github",
    "mongodb",
    "mysql",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "power bi",
    "excel",
]


import re


def extract_skills(text):
    text = text.lower()

    detected_skills = []

    for skill in SKILLS:
        skill = skill.lower()

        if " " in skill or "-" in skill:
            # Multi-word skills such as machine learning
            if skill in text:
                detected_skills.append(skill)

        else:
            # Match complete words only
            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, text):
                detected_skills.append(skill)

    return detected_skills 


