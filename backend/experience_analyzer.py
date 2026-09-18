import re


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================================================
# EXPERIENCE SECTION DETECTION
# =========================================================

def find_experience_section(text):
    """
    Finds the actual Work Experience / Employment / Internship
    section and returns only that section's text.

    Projects, Education, Skills, etc. are treated as separate
    sections and are not counted as work experience.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    experience_headings = [
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "professional history",
        "experience",
        "internship experience",
        "internships",
        "internship",
    ]

    stop_headings = [
        "education",
        "academic background",
        "academic qualifications",
        "skills",
        "technical skills",
        "projects",
        "personal projects",
        "academic projects",
        "certifications",
        "certificates",
        "achievements",
        "awards",
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective",
        "contact",
        "personal details",
        "languages",
        "interests",
        "hobbies",
        "references",
    ]

    start_index = None

    for index, line in enumerate(lines):
        normalized = re.sub(r"[^a-z\s]", "", line.lower()).strip()

        if normalized in experience_headings:
            start_index = index + 1
            break

    if start_index is None:
        return ""

    section_lines = []

    for line in lines[start_index:]:
        normalized = re.sub(
            r"[^a-z\s]",
            "",
            line.lower()
        ).strip()

        if normalized in stop_headings:
            break

        section_lines.append(line)

    return "\n".join(section_lines)


# =========================================================
# DATE DETECTION
# =========================================================

def detect_dates(text):

    date_patterns = [
        r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b",

        r"\b(?:january|february|march|april|may|june|july|august|"
        r"september|october|november|december)\s+\d{4}\b",

        r"\b\d{1,2}[/-]\d{4}\b",

        r"\b\d{4}\s*[-–]\s*(?:\d{4}|present|current)\b",

        r"\b\d{4}\s+to\s+(?:\d{4}|present|current)\b",

        r"\b\d{4}\s*[-–]\s*\d{4}\b",
    ]

    dates = []

    for pattern in date_patterns:

        matches = re.findall(
            pattern,
            text.lower()
        )

        for match in matches:

            if match not in dates:
                dates.append(match)

    return dates


# =========================================================
# EXPERIENCE DURATION
# =========================================================

def detect_experience_years(text):

    patterns = [

        r"\b(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)"
        r"\s+(?:of\s+)?experience\b",

        r"\b(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\b",
    ]

    values = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text.lower()
        )

        for match in matches:

            try:

                value = float(match)

                if 0 < value <= 50:

                    if value not in values:
                        values.append(value)

            except ValueError:
                continue

    if not values:
        return None

    return max(values)


# =========================================================
# ROLE DETECTION
# =========================================================

def detect_experience_entries(section_text):

    if not section_text:
        return []

    role_patterns = [

        # Software / Technology
        r"\bsoftware engineer\b",
        r"\bsoftware developer\b",
        r"\bfrontend developer\b",
        r"\bfront[- ]end developer\b",
        r"\bbackend developer\b",
        r"\bback[- ]end developer\b",
        r"\bfull stack developer\b",
        r"\bfull[- ]stack developer\b",
        r"\bweb developer\b",
        r"\bapplication developer\b",
        r"\bmobile app developer\b",
        r"\bandroid developer\b",
        r"\bios developer\b",
        r"\bdevops engineer\b",
        r"\bcloud engineer\b",
        r"\bdata engineer\b",
        r"\bmachine learning engineer\b",
        r"\bml engineer\b",
        r"\bdata scientist\b",
        r"\bdata analyst\b",
        r"\bbusiness analyst\b",
        r"\bqa engineer\b",
        r"\btest engineer\b",
        r"\bautomation engineer\b",
        r"\bai engineer\b",
        r"\bai developer\b",
        r"\btechnical support engineer\b",

        # Design
        r"\bui designer\b",
        r"\bux designer\b",
        r"\bui/ux designer\b",
        r"\bgraphic designer\b",
        r"\bproduct designer\b",
        r"\bweb designer\b",

        # Management
        r"\bproduct manager\b",
        r"\bproject manager\b",
        r"\bprogram manager\b",
        r"\boperations manager\b",
        r"\bengineering manager\b",

        # Business / Sales / Marketing
        r"\bsales executive\b",
        r"\bsales manager\b",
        r"\bmarketing executive\b",
        r"\bmarketing manager\b",
        r"\bdigital marketing executive\b",
        r"\bbusiness development executive\b",
        r"\bbusiness development associate\b",

        # HR / Finance
        r"\bhr executive\b",
        r"\bhr associate\b",
        r"\bhr manager\b",
        r"\brecruiter\b",
        r"\bfinancial analyst\b",
        r"\baccountant\b",
        r"\baccount executive\b",

        # General professional roles
        r"\bconsultant\b",
        r"\bassociate\b",
        r"\bexecutive\b",
        r"\btrainee\b",
        r"\bmanager\b",
        r"\banalyst\b",
        r"\bengineer\b",
        r"\bdeveloper\b",
        r"\bdesigner\b",

        # Internship roles
        r"\bsoftware engineer intern\b",
        r"\bsoftware developer intern\b",
        r"\bdeveloper intern\b",
        r"\bdata analyst intern\b",
        r"\bmachine learning intern\b",
        r"\bengineering intern\b",
        r"\bmarketing intern\b",
        r"\bhr intern\b",
        r"\bweb development intern\b",
        r"\bintern\b",
        r"\binternship\b",
    ]

    lines = [
        line.strip()
        for line in section_text.splitlines()
        if line.strip()
    ]

    entries = []

    for index, line in enumerate(lines):

        line_lower = line.lower()

        if len(line) > 120:
            continue

        has_role = any(
            re.search(
                pattern,
                line_lower
            )
            for pattern in role_patterns
        )

        if not has_role:
            continue

        # Ignore obvious bullet responsibilities.
        if (
            line.startswith("-")
            or line.startswith("•")
            or line.startswith("*")
        ):
            continue

        # A role is stronger evidence when a date is on the
        # same line or immediately nearby.
        nearby_text = line

        if index + 1 < len(lines):
            nearby_text += " " + lines[index + 1]

        if index + 2 < len(lines):
            nearby_text += " " + lines[index + 2]

        has_nearby_date = bool(
            detect_dates(nearby_text)
        )

        # Internship itself is strong evidence.
        is_internship = bool(
            re.search(
                r"\bintern(ship)?\b",
                line_lower
            )
        )

        if has_nearby_date or is_internship:

            if line not in entries:
                entries.append(line)

    return entries[:10]


# =========================================================
# INTERNSHIP DETECTION
# =========================================================

def detect_internship(section_text):

    if not section_text:
        return False

    return bool(
        re.search(
            r"\bintern(ship)?\b",
            section_text.lower()
        )
    )


# =========================================================
# EXPERIENCE LEVEL
# =========================================================

def detect_experience_level(
    resume_text,
    experience_years,
    internship_detected
):

    text_lower = resume_text.lower()

    # Explicit fresher indicators
    fresher_phrases = [
        "fresher",
        "fresh graduate",
        "recent graduate",
        "entry level",
        "entry-level",
    ]

    if any(
        phrase in text_lower
        for phrase in fresher_phrases
    ):

        if internship_detected:
            return "Internship / Entry Level"

        return "Fresher / Entry Level"

    if experience_years is not None:

        if experience_years < 1:
            return "Entry Level"

        if experience_years < 3:
            return "Junior"

        if experience_years < 5:
            return "Mid Level"

        if experience_years < 8:
            return "Senior"

        return "Lead / Experienced"

    if internship_detected:
        return "Internship / Entry Level"

    return "Not Detected"


# =========================================================
# METRICS / ACHIEVEMENTS
# =========================================================

def detect_metrics(text):

    metric_patterns = [

        r"\b\d+(?:\.\d+)?%",

        r"\b\d+\+?\s*"
        r"(?:users|clients|customers|projects|employees|members)\b",

        r"\b\d+(?:\.\d+)?\s*"
        r"(?:years?|months?)\b",

        r"\b\d+(?:\.\d+)?\s*"
        r"(?:hours?|days?)\b",

        r"\$\s?\d+(?:,\d{3})*(?:\.\d+)?",

        r"\b\d+(?:,\d{3})+\b",
    ]

    metrics = []

    for pattern in metric_patterns:

        matches = re.findall(
            pattern,
            text.lower()
        )

        for match in matches:

            if match not in metrics:
                metrics.append(match)

    return metrics


# =========================================================
# BULLET ANALYSIS
# =========================================================

def analyze_bullets(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    bullet_lines = []

    for line in lines:

        if (
            line.startswith("-")
            or line.startswith("•")
            or line.startswith("*")
        ):

            bullet_lines.append(line)

    return bullet_lines


# =========================================================
# ACTION VERBS
# =========================================================

def analyze_action_verbs(text):

    action_verbs = [

        "developed",
        "built",
        "created",
        "designed",
        "implemented",
        "managed",
        "led",
        "improved",
        "optimized",
        "automated",
        "analyzed",
        "engineered",
        "deployed",
        "tested",
        "integrated",
        "configured",
        "delivered",
        "launched",
        "coordinated",
        "maintained",
    ]

    text_lower = text.lower()

    found = [

        verb

        for verb in action_verbs

        if re.search(
            r"\b" + re.escape(verb) + r"\b",
            text_lower
        )
    ]

    return list(
        dict.fromkeys(found)
    )


# =========================================================
# MAIN EXPERIENCE ANALYZER
# =========================================================

def analyze_experience(
    resume_text,
    job_description=""
):

    resume_clean = clean_text(
        resume_text
    )

    job_clean = clean_text(
        job_description
    )

    # -----------------------------------------------------
    # Find actual experience section
    # -----------------------------------------------------

    experience_section = find_experience_section(
        resume_text
    )

    # -----------------------------------------------------
    # Detect actual roles/internships
    # -----------------------------------------------------

    entries = detect_experience_entries(
        experience_section
    )

    internship_detected = detect_internship(
        experience_section
    )

    dates = detect_dates(
        experience_section
    )

    experience_years = detect_experience_years(
        experience_section
    )

    metrics = detect_metrics(
        experience_section
    )

    bullets = analyze_bullets(
        experience_section
    )

    action_verbs = analyze_action_verbs(
        experience_section
    )

    # -----------------------------------------------------
    # IMPORTANT:
    # Actual experience exists only when we have strong
    # evidence from a role/internship.
    # -----------------------------------------------------

    has_experience = bool(
        entries
    )

    # -----------------------------------------------------
    # If there is NO actual experience:
    # Return a clean empty result.
    # -----------------------------------------------------

    if not has_experience:

        return {
            "has_experience": False,
            "experience_score": 0,
            "experience_level": "Not Detected",
            "experience_years": None,
            "section_present": bool(
                experience_section
            ),
            "internship_detected": False,
            "entries": [],
            "dates_detected": [],
            "metrics_detected": [],
            "bullet_count": 0,
            "action_verbs_detected": [],
            "job_relevance_score": 0,
            "matched_job_experience_keywords": [],
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
        }

    # -----------------------------------------------------
    # Experience level
    # -----------------------------------------------------

    experience_level = detect_experience_level(
        resume_text,
        experience_years,
        internship_detected
    )
    # -----------------------------------------------------
    # Job relevance
    # -----------------------------------------------------

    experience_keywords = []

    if job_clean:
        jd_words = re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
            job_clean
        )

        generic_words = {
            "the", "and", "for", "with", "from", "that",
            "this", "your", "you", "are", "our", "will",
            "have", "has", "was", "were", "their", "they",
            "them", "job", "role", "work", "working", "using",
            "use", "used", "team", "teams", "good", "strong",
            "looking", "candidate", "required", "preferred",
            "ability", "skills", "skill", "experience", "years",
            "year", "responsibilities", "responsibility",
            "including", "include", "also", "must", "should",
            "within", "into", "about", "more", "than",
            "company", "business", "position", "department",
            "office", "location", "requirements", "requirement",
            "qualifications", "qualification", "knowledge",
            "environment", "opportunity", "provide", "support",
            "ensure", "responsible", "excellent"
        }

        for word in jd_words:
            if (
                word not in generic_words
                and word not in experience_keywords
            ):
                experience_keywords.append(word)

    experience_text = clean_text(
        experience_section
    )

    resume_experience_keywords = [
        keyword
        for keyword in experience_keywords
        if keyword in experience_text
    ]

    matched_job_keywords = list(
        dict.fromkeys(
            resume_experience_keywords
        )
    )

    job_experience_keywords = list(
        dict.fromkeys(
            experience_keywords
        )
    )

    if job_experience_keywords:
        relevance_score = round(
            (
                len(matched_job_keywords)
                / len(job_experience_keywords)
            ) * 100
        )
    else:
        relevance_score = 100

    # -----------------------------------------------------
    # Experience score
    # -----------------------------------------------------

    score = 0

    if experience_section:
        score += 25

    if entries:
        score += 25

    if dates:
        score += 20

    if bullets:
        score += 25

    if action_verbs:
        score += 20

    
    if (
        job_description
        and relevance_score >= 70
    ):
        score += 25

    score = min(
        score,
        100
    )

    # -----------------------------------------------------
    # Strengths
    # -----------------------------------------------------

    strengths = []
    weaknesses = []
    recommendations = []

    if entries:

        strengths.append(
            "Relevant job or internship roles were detected."
        )

    if dates:

        strengths.append(
            "Experience dates or duration information was detected."
        )

    if bullets:

        strengths.append(
            "Experience responsibilities are presented using bullet points."
        )

    if action_verbs:

        strengths.append(
            "Action verbs were detected in the experience section."
        )

    if metrics:

        strengths.append(
            "Measurable achievements or numerical results were detected."
        )

    # -----------------------------------------------------
    # Weaknesses
    # -----------------------------------------------------

    if not dates:

        weaknesses.append(
            "Experience dates or duration are not clearly shown."
        )

    if not bullets:

        weaknesses.append(
            "Experience responsibilities are not clearly formatted as bullet points."
        )

    if not action_verbs:

        weaknesses.append(
            "Strong action verbs were not detected in experience details."
        )

    if not metrics:

        weaknesses.append(
            "Few or no measurable achievements were detected."
        )

    # -----------------------------------------------------
    # Job description relevance
    # -----------------------------------------------------

    if job_description:

        if relevance_score >= 70:

            strengths.append(
                "Experience has a strong match with the target job."
            )

        elif relevance_score >= 50:

            weaknesses.append(
                "Experience has a moderate match with the target job."
            )

        else:

            weaknesses.append(
                "Experience has a low match with the target job."
            )

    # -----------------------------------------------------
    # Recommendations
    # -----------------------------------------------------

    if not dates:

        recommendations.append(
            "Add clear start and end dates for each experience or internship."
        )

    if not bullets:

        recommendations.append(
            "Use concise bullet points to describe responsibilities and achievements."
        )

    if not metrics:

        recommendations.append(
            "Add measurable results such as percentages, users, revenue, or time saved."
        )

    if not action_verbs:

        recommendations.append(
            "Start experience bullets with strong action verbs such as Developed, Built, Implemented, or Optimized."
        )

    if (
        job_description
        and relevance_score < 70
    ):

        recommendations.append(
            "Tailor experience bullets to the skills and responsibilities mentioned in the target job description."
        )

    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    return {

        "has_experience": True,

        "experience_score": score,

        "experience_level": experience_level,

        "experience_years": experience_years,

        "section_present": True,

        "internship_detected": internship_detected,

        "entries": entries,

        "dates_detected": dates,

        "metrics_detected": metrics,

        "bullet_count": len(bullets),

        "action_verbs_detected": action_verbs,

        "job_relevance_score": relevance_score,

        "matched_job_experience_keywords": matched_job_keywords,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations,
    }