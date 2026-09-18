import re


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def detect_education_section(text):
    text_lower = text.lower()

    keywords = [
        "education",
        "academic background",
        "academic qualification",
        "academic qualifications",
        "educational background",
        "qualifications",
    ]

    return any(keyword in text_lower for keyword in keywords)


def detect_degrees(text):
    text_lower = text.lower()

    degrees = [
        "b.tech",
        "btech",
        "b.e",
        "be",
        "bachelor of technology",
        "bachelor of engineering",
        "b.sc",
        "bsc",
        "bachelor of science",
        "bca",
        "bachelor of computer applications",
        "m.tech",
        "mtech",
        "m.e",
        "me",
        "master of technology",
        "master of engineering",
        "m.sc",
        "msc",
        "master of science",
        "mca",
        "master of computer applications",
        "mba",
        "master of business administration",
        "phd",
        "doctorate",
        "bachelor",
        "master",
        "diploma",
    ]

    found = []

    for degree in degrees:
        if re.search(r"\b" + re.escape(degree) + r"\b", text_lower):
            if degree not in found:
                found.append(degree)

    return found


def detect_institutions(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    institutions = []

    institution_keywords = [
        "university",
        "college",
        "institute",
        "school",
        "academy",
    ]

    for line in lines:
        line_lower = line.lower()

        if any(keyword in line_lower for keyword in institution_keywords):
            institutions.append(line)

    return institutions[:10]


def detect_graduation_years(text):
    years = re.findall(
        r"\b(?:19|20)\d{2}\b",
        text
    )

    unique_years = []

    for year in years:
        if year not in unique_years:
            unique_years.append(year)

    return unique_years


def detect_cgpa_percentage(text):
    patterns = [
        r"\b\d+(?:\.\d+)?\s*(?:cgpa|gpa)\b",
        r"\b(?:cgpa|gpa)\s*[:\-]?\s*\d+(?:\.\d+)?\b",
        r"\b\d+(?:\.\d+)?\s*%",
        r"\b(?:percentage|percent)\s*[:\-]?\s*\d+(?:\.\d+)?\b",
    ]

    results = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text.lower()
        )

        for match in matches:
            if match not in results:
                results.append(match)

    return results


def detect_fields_of_study(text):
    text_lower = text.lower()

    fields = [
        "computer science",
        "information technology",
        "information science",
        "software engineering",
        "data science",
        "artificial intelligence",
        "machine learning",
        "electronics",
        "electrical engineering",
        "mechanical engineering",
        "civil engineering",
        "business administration",
        "commerce",
        "mathematics",
        "physics",
        "chemistry",
    ]

    found = []

    for field in fields:
        if field in text_lower:
            found.append(field)

    return found


def analyze_education(resume_text, job_description=""):

    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_description)

    section_present = detect_education_section(
        resume_text
    )

    degrees = detect_degrees(
        resume_text
    )

    institutions = detect_institutions(
        resume_text
    )

    graduation_years = detect_graduation_years(
        resume_text
    )

    academic_scores = detect_cgpa_percentage(
        resume_text
    )

    fields_of_study = detect_fields_of_study(
        resume_text
    )

       # --------------------------------------------------
    # JOB DESCRIPTION EDUCATION RELEVANCE
    # --------------------------------------------------

    education_keywords = []

    if job_clean:
        jd_words = re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
            job_clean
        )

        generic_words = {
            "the", "and", "for", "with", "from", "that",
            "this", "your", "you", "are", "our", "will",
            "have", "has", "was", "were", "their", "they",
            "them", "job", "role", "work", "working",
            "using", "use", "used", "team", "teams",
            "good", "strong", "looking", "candidate",
            "required", "preferred", "ability", "skills",
            "skill", "experience", "years", "year",
            "responsibilities", "responsibility", "including",
            "include", "also", "must", "should", "within",
            "into", "about", "more", "than", "company",
            "business", "position", "department", "office",
            "location", "requirements", "requirement",
            "qualifications", "qualification", "knowledge",
            "environment", "opportunity", "provide", "support",
            "ensure", "responsible", "excellent"
        }

        for word in jd_words:
            if (
                word not in generic_words
                and word not in education_keywords
            ):
                education_keywords.append(word)

    resume_education_keywords = [
        keyword
        for keyword in education_keywords
        if keyword in resume_clean
    ]

    job_education_keywords = list(
        dict.fromkeys(education_keywords)
    )

    matched_education_keywords = list(
        dict.fromkeys(resume_education_keywords)
    )

    if job_education_keywords:
        job_relevance_score = round(
            (
                len(matched_education_keywords)
                / len(job_education_keywords)
            ) * 100
        )
    else:
        job_relevance_score = 100

    # --------------------------------------------------
    # EDUCATION SCORE
    # --------------------------------------------------

    score = 0

    if section_present:
        score += 25

    if degrees:
        score += 25

    if institutions:
        score += 20

    if graduation_years:
        score += 10

    if academic_scores:
        score += 10

    if fields_of_study:
        score += 10

    score = min(score, 100)

    # --------------------------------------------------
    # STRENGTHS
    # --------------------------------------------------

    strengths = []

    if section_present:
        strengths.append(
            "A clear education section was detected."
        )

    if degrees:
        strengths.append(
            "Degree or qualification information was detected."
        )

    if institutions:
        strengths.append(
            "Educational institution information was detected."
        )

    if graduation_years:
        strengths.append(
            "Graduation or academic years were detected."
        )

    if academic_scores:
        strengths.append(
            "Academic performance information such as CGPA or percentage was detected."
        )

    if fields_of_study:
        strengths.append(
            "Field of study or academic specialization was detected."
        )

    if job_description:

        if job_relevance_score >= 70:
            strengths.append(
                "Education information has a strong match with the provided job description."
            )

    # --------------------------------------------------
    # WEAKNESSES
    # --------------------------------------------------

    weaknesses = []

    if not section_present:
        weaknesses.append(
            "A clear education section was not detected."
        )

    if not degrees:
        weaknesses.append(
            "Degree or qualification information was not clearly detected."
        )

    if not institutions:
        weaknesses.append(
            "Educational institution information was not clearly detected."
        )

    if not graduation_years:
        weaknesses.append(
            "Graduation or academic years were not clearly detected."
        )

    if not academic_scores:
        weaknesses.append(
            "CGPA or percentage information was not detected."
        )

    if not fields_of_study:
        weaknesses.append(
            "Field of study or specialization was not clearly detected."
        )

    if job_description:

        if job_relevance_score < 70:
            weaknesses.append(
                "Education information has limited relevance to the provided job description."
            )

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = []

    if not section_present:
        recommendations.append(
            "Add a clearly labeled Education section to your resume."
        )

    if not degrees:
        recommendations.append(
            "Clearly mention your degree or qualification."
        )

    if not institutions:
        recommendations.append(
            "Mention the college, university, or institution name."
        )

    if not graduation_years:
        recommendations.append(
            "Add graduation year or expected graduation year where appropriate."
        )

    if not academic_scores:
        recommendations.append(
            "Consider adding CGPA or percentage if it strengthens your application."
        )

    if not fields_of_study:
        recommendations.append(
            "Mention your major, specialization, or field of study."
        )

    if job_description and job_relevance_score < 70:
        recommendations.append(
            "Highlight education details that directly match the target job requirements."
        )

    return {
        "education_score": score,
        "section_present": section_present,
        "degrees_detected": degrees,
        "institutions_detected": institutions,
        "graduation_years": graduation_years,
        "academic_scores": academic_scores,
        "fields_of_study": fields_of_study,
        "job_relevance_score": job_relevance_score,
        "matched_job_education_keywords": matched_education_keywords,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
    }