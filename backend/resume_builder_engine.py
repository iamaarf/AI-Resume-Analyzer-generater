from ai_resume_generator import generate_ai_resume


def build_resume(resume_data: dict) -> dict:

    ai_resume = generate_ai_resume(resume_data)

    return {
        "personal_information": {
            "name": resume_data.get("name", ""),
            "email": resume_data.get("email", ""),
            "phone": resume_data.get("phone", ""),
            "location": resume_data.get("location", ""),
            "linkedin": resume_data.get("linkedin", ""),
        },

        "target_role": resume_data.get(
            "targetRole",
            ""
        ),

        "professional_summary": ai_resume.get(
            "professional_summary",
            ""
        ),

        "skills": ai_resume.get(
            "skills",
            []
        ),

        "work_experience": ai_resume.get(
            "work_experience",
            []
        ),

        "education": ai_resume.get(
            "education",
            []
        ),

        "projects": ai_resume.get(
            "projects",
            []
        ),

        "certifications": ai_resume.get(
            "certifications",
            []
        ),

        "languages": ai_resume.get(
            "languages",
            []
        ),

        "matched_keywords": ai_resume.get(
            "matched_keywords",
            []
        ),

        "missing_requirements": ai_resume.get(
            "missing_requirements",
            []
        ),

        "job_description": resume_data.get(
            "jobDescription",
            ""
        ),
    }