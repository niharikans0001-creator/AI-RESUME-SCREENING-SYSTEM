def calculate_match_score(resume_skills, job_description, extract_skills_function):

    required_skills = extract_skills_function(job_description)

    if len(required_skills) == 0:
        return 0, [], []

    matched_skills = []

    for skill in required_skills:
        if skill in resume_skills:
            matched_skills.append(skill)

    score = (len(matched_skills) / len(required_skills)) * 100

    return round(score, 2), required_skills, matched_skills