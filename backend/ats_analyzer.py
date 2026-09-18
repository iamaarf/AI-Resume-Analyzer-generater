import re

def analyze_resume_sections(text):
    text_lower = text.lower()

    section_details = {}

    # Summary
    section_details["summary"] = {
        "present": any(
            keyword in text_lower
            for keyword in [
                "summary",
                "objective",
                "profile",
                "career objective"
            ]
        ),
        "status": "Good" if any(
            keyword in text_lower
            for keyword in [
                "summary",
                "objective",
                "profile",
                "career objective"
            ]
        ) else "Missing"
    }

    # Skills
    section_details["skills"] = {
        "present": any(
            keyword in text_lower
            for keyword in [
                "skills",
                "technical skills",
                "core skills"
            ]
        ),
        "status": "Good" if any(
            keyword in text_lower
            for keyword in [
                "skills",
                "technical skills",
                "core skills"
            ]
        ) else "Missing"
    }

    # Experience
    section_details["experience"] = {
        "present": any(
            keyword in text_lower
            for keyword in [
                "experience",
                "work experience",
                "employment",
                "internship"
            ]
        ),
        "status": "Good" if any(
            keyword in text_lower
            for keyword in [
                "experience",
                "work experience",
                "employment",
                "internship"
            ]
        ) else "Missing"
    }

    # Education
    section_details["education"] = {
        "present": any(
            keyword in text_lower
            for keyword in [
                "education",
                "academic"
            ]
        ),
        "status": "Good" if any(
            keyword in text_lower
            for keyword in [
                "education",
                "academic"
            ]
        ) else "Missing"
    }

    # Projects
    section_details["projects"] = {
        "present": "project" in text_lower,
        "status": "Good" if "project" in text_lower else "Missing"
    }

    # Certifications
    section_details["certifications"] = {
        "present": any(
            keyword in text_lower
            for keyword in [
                "certification",
                "certifications",
                "courses"
            ]
        ),
        "status": "Good" if any(
            keyword in text_lower
            for keyword in [
                "certification",
                "certifications",
                "courses"
            ]
        ) else "Missing"
    }

    # Achievements
    section_details["achievements"] = {
        "present": any(
            keyword in text_lower
            for keyword in [
                "achievement",
                "achievements",
                "awards",
                "honors"
            ]
        ),
        "status": "Good" if any(
            keyword in text_lower
            for keyword in [
                "achievement",
                "achievements",
                "awards",
                "honors"
            ]
        ) else "Missing"
    }

    return section_details

def analyze_resume(text, job_description=""):
    section_details = analyze_resume_sections(text)

    job_description_lower = job_description.lower().strip()

    text_lower = text.lower()

    # --------------------------------------------------
    # 1. COMMON RESUME SECTIONS
    # --------------------------------------------------

    sections = {
        "contact": ["email", "phone", "linkedin"],
        "summary": ["summary", "objective", "profile", "career objective"],
        "skills": ["skills", "technical skills", "core skills"],
        "experience": ["experience", "work experience", "employment", "internship"],
        "education": ["education", "academic"],
        "projects": ["projects", "project"],
        "certifications": ["certifications", "certification", "courses"],
        "achievements": ["achievements", "awards", "honors"],
    }

    section_score = 0
    found_sections = []

    for section, keywords in sections.items():
        if any(keyword in text_lower for keyword in keywords):
            section_score += 1
            found_sections.append(section)

    section_score = round(
        (section_score / len(sections)) * 100
    )

    # --------------------------------------------------
    # 2. CONTACT INFORMATION
    # --------------------------------------------------

    email_found = bool(
        re.search(
            r"[\w\.-]+@[\w\.-]+\.\w+",
            text
        )
    )

    phone_match = re.search(
        r"(?:\+91[\s-]?)?(?:\d[\s-]?){10}",
        text
    )

    phone_found = bool(phone_match)

    linkedin_found = "linkedin" in text_lower
    github_found = "github" in text_lower

    contact_score = 0

    if email_found:
        contact_score += 40

    if phone_found:
        contact_score += 40

    if linkedin_found:
        contact_score += 10

    if github_found:
        contact_score += 10

       # --------------------------------------------------
    # 3. JOB-SPECIFIC ATS KEYWORDS
    # --------------------------------------------------

    common_keywords = [
        "python", "java", "javascript", "react", "sql", "html", "css",
        "c++", "machine learning", "deep learning", "data analysis",
        "data science", "power bi", "tableau", "excel", "aws", "azure",
        "git", "github", "communication", "leadership", "problem solving",
        "project management", "artificial intelligence",
    ]

    stop_words = {
        "the", "and", "for", "with", "from", "that", "this", "your",
        "you", "are", "our", "will", "have", "has", "was", "were",
        "their", "they", "them", "job", "role", "work", "working",
        "using", "use", "used", "team", "teams", "good", "strong",
        "looking", "candidate", "required", "preferred", "ability",
        "skills", "skill", "experience", "years", "year",
        "responsibilities", "responsibility", "including", "include",
        "also", "must", "should", "within", "into", "about", "more",
        "than", "who", "can", "all", "any",
    }

    jd_keywords = []

    if job_description_lower:
        jd_words = re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
            job_description_lower
        )

        for word in jd_words:
            if (
                word not in stop_words
                and word not in jd_keywords
            ):
                jd_keywords.append(word)

    # Detect common ATS keywords from resume
    found_common_keywords = [
        keyword
        for keyword in common_keywords
        if keyword in text_lower
    ]

    # --------------------------------------------------
    # FILTER GENERIC JD WORDS
    # --------------------------------------------------

    generic_words = {
        "company",
        "business",
        "position",
        "department",
        "office",
        "location",
        "salary",
        "benefits",
        "requirements",
        "requirement",
        "qualifications",
        "qualification",
        "preferred",
        "required",
        "ability",
        "knowledge",
        "skills",
        "skill",
        "experience",
        "years",
        "role",
        "job",
        "work",
        "working",
        "team",
        "teams",
        "environment",
        "opportunity",
        "responsible",
        "responsibilities",
        "responsibility",
        "including",
        "provide",
        "support",
        "ensure",
        "manage",
        "strong",
        "excellent",
        "good",
    }

    jd_keywords = [
        keyword
        for keyword in jd_keywords
        if keyword not in generic_words
    ]

    # Detect job-specific keywords present in resume
    found_jd_keywords = [
        keyword
        for keyword in jd_keywords
        if keyword in text_lower
    ]

    # Combine both lists without duplicates
    found_keywords = list(dict.fromkeys(
        found_common_keywords + found_jd_keywords
    ))

    # --------------------------------------------------
    # KEYWORD SCORE
    # --------------------------------------------------

    if jd_keywords:
        jd_match_count = len(found_jd_keywords)

        keyword_score = round(
            (jd_match_count / len(jd_keywords)) * 100
        )

        keyword_score = min(
            max(keyword_score, 0),
            100
        )

    else:
        keyword_score = min(
            len(found_common_keywords) * 5,
            100
        )

    # --------------------------------------------------
    # 4. RESUME STRENGTHS
    # --------------------------------------------------

    strengths = []

    if email_found and phone_found:
        strengths.append(
            "Complete basic contact information is available."
        )

    if linkedin_found:
        strengths.append(
            "LinkedIn profile was detected."
        )

    if github_found:
        strengths.append(
            "GitHub profile was detected."
        )

    if "skills" in found_sections:
        strengths.append(
            "A dedicated skills section is present."
        )

    if "education" in found_sections:
        strengths.append(
            "Education details are included."
        )

    if "projects" in found_sections:
        strengths.append(
            "Projects section is included."
        )

    if "experience" in found_sections:
        strengths.append(
            "Experience or internship information was detected."
        )

    if "certifications" in found_sections:
        strengths.append(
            "Certifications or courses were detected."
        )

    if len(found_keywords) >= 5:
        strengths.append(
            "The resume contains a good number of relevant keywords."
        )

    # --------------------------------------------------
    # 5. RESUME WEAKNESSES
    # --------------------------------------------------

    weaknesses = []

    if not email_found:
        weaknesses.append(
            "Email address was not detected."
        )

    if not phone_found:
        weaknesses.append(
            "Phone number was not detected."
        )

    if not linkedin_found:
        weaknesses.append(
            "LinkedIn profile was not detected."
        )

    if "summary" not in found_sections:
        weaknesses.append(
            "Professional summary or objective was not detected."
        )

    if "experience" not in found_sections:
        weaknesses.append(
            "Work experience or internship section was not detected."
        )

    if "skills" not in found_sections:
        weaknesses.append(
            "Skills section was not detected."
        )

    if "projects" not in found_sections:
        weaknesses.append(
            "Projects section was not detected."
        )

    if "certifications" not in found_sections:
        weaknesses.append(
            "Certifications or courses were not detected."
        )

    if len(found_keywords) < 5:
        weaknesses.append(
            "The resume contains a limited number of detected ATS keywords."
        )

    # --------------------------------------------------
    # 6. RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = []

    if not email_found or not phone_found:
        recommendations.append(
            "Make sure your email address and phone number are clearly visible."
        )

    if not linkedin_found:
        recommendations.append(
            "Add your LinkedIn profile URL to your resume."
        )

    if not github_found:
        recommendations.append(
            "If you have technical projects, consider adding your GitHub profile."
        )

    if "summary" not in found_sections:
        recommendations.append(
            "Add a short professional summary tailored to your target job."
        )

    if "experience" not in found_sections:
        recommendations.append(
            "Add internships, freelance work, training, or relevant professional experience if applicable."
        )

    if "projects" not in found_sections:
        recommendations.append(
            "Add 2-3 relevant projects with technologies used and measurable results."
        )

    if "certifications" not in found_sections:
        recommendations.append(
            "Add relevant certifications, courses, or professional training."
        )

    if len(found_keywords) < 5:
        recommendations.append(
            "Add relevant job-specific keywords naturally throughout your resume."
        )

    recommendations.append(
        "Use measurable achievements wherever possible, such as percentages, numbers, users served, revenue, time saved, or performance improvements."
    )

    recommendations.append(
        "Tailor your resume keywords and content to the specific job description you are applying for."
    )

          # --------------------------------------------------
    # 7. FINAL ATS SCORE
    # --------------------------------------------------

    if job_description_lower:
        # Balanced ATS score when a job description is provided.
        keyword_component = keyword_score * 0.45
        section_component = section_score * 0.40
        contact_component = contact_score * 0.25
        base_component = 50 * 0.20

        final_score = round(
            keyword_component
            + section_component
            + contact_component
            + base_component
        )

    else:
        # ATS score without a job description.
        final_score = round(
            (section_score * 0.60)
            + (contact_score * 0.41)
            + (keyword_score * 0.30)
        )

    final_score = min(max(final_score, 0), 100)

    # --------------------------------------------------
    # 8. FINAL RESPONSE
    # --------------------------------------------------

    return {
        "ats_score": final_score,

        "section_score": section_score,

        "contact_score": contact_score,

        "keyword_score": keyword_score,

        "found_sections": found_sections,

        "found_keywords": found_keywords,

        "personal_information": {
            "email": (
                re.search(
                    r"[\w\.-]+@[\w\.-]+\.\w+",
                    text
                ).group(0)
                if email_found
                else None
            ),
                   "phone": (
            phone_match.group(0).strip()
            if phone_match
            else None
        ),
            "linkedin": linkedin_found,
            "github": github_found,
        },
        "section_details": section_details,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations,
    }