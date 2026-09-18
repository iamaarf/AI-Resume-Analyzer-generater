import re


def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^\w\s%+.#/-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def find_project_section(text):
    if not text:
        return ""

    lines = text.splitlines()

    start_headings = [
        "projects",
        "project",
        "personal projects",
        "academic projects",
        "academic project",
        "key projects",
        "project experience",
        "project work",
        "projects experience",
    ]

    stop_headings = [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "education",
        "academic background",
        "academic qualifications",
        "skills",
        "technical skills",
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

    # -----------------------------------------
    # 1. NORMAL LINE-BY-LINE HEADING DETECTION
    # -----------------------------------------

    start_index = None

    for i, line in enumerate(lines):
        heading = clean_text(line)

        if heading in start_headings:
            start_index = i + 1
            break

    if start_index is not None:

        section_lines = []

        for line in lines[start_index:]:
            heading = clean_text(line)

            if heading in stop_headings:
                break

            section_lines.append(line)

        section = "\n".join(section_lines).strip()

        if section:
            return section

    # -----------------------------------------
    # 2. FALLBACK FOR PDF TEXT EXTRACTION
    # -----------------------------------------
    # Sometimes PDF extraction does not preserve
    # headings as separate lines.

    normalized_text = clean_text(text)

    project_heading_patterns = [
        "academic projects",
        "personal projects",
        "project experience",
        "project work",
        "key projects",
        "projects",
    ]

    start_position = -1
    matched_heading = ""

    for heading in project_heading_patterns:
        position = normalized_text.find(heading)

        if position != -1:
            if start_position == -1 or position < start_position:
                start_position = position
                matched_heading = heading

    if start_position == -1:
        return ""

    project_text = normalized_text[
        start_position + len(matched_heading):
    ].strip()

    # -----------------------------------------
    # 3. STOP BEFORE NEXT MAJOR RESUME SECTION
    # -----------------------------------------

    stop_patterns = [
        "work experience",
        "professional experience",
        "employment history",
        "education",
        "technical skills",
        "skills",
        "certifications",
        "achievements",
        "awards",
        "languages",
    ]

    stop_position = len(project_text)

    for stop_heading in stop_patterns:
        position = project_text.find(stop_heading)

        if position != -1 and position < stop_position:
            stop_position = position

    project_text = project_text[:stop_position].strip()

    return project_text
def detect_project_entries(section_text):
    if not section_text:
        return []

    lines = [
        line.strip()
        for line in section_text.splitlines()
        if line.strip()
    ]

    entries = []

    for line in lines:
        clean_line = clean_text(line)

        if not clean_line:
            continue

        # Detect only actual project title lines
        if re.match(r"^[●•*-]?\s*project\s*\d+", clean_line):
            entries.append(line)

    return list(dict.fromkeys(entries))
def detect_project_bullets(section_text):
    if not section_text:
        return []

    lines = [
        line.strip()
        for line in section_text.splitlines()
        if line.strip()
    ]

    bullets = []
    inside_project = False

    for line in lines:
        clean_line = clean_text(line)

        # Start of a project
        if re.match(r"^[●•*-]?\s*project\s*\d+", clean_line):
            inside_project = True
            bullets.append(
                re.sub(r"^[●•*-]\s*", "", line).strip()
            )
            continue

        # Everything after the project section that looks like
        # personal skills/languages should not be treated as project content.
        if inside_project:
            stop_patterns = [
                "fluent in",
                "strong analytical",
                "quick learner",
                "team management",
                "english",
                "hindi",
                "languages",
                "skills",
                "technical skills",
                "certifications",
                "achievements",
                "awards",
                "experience",
                "education",
            ]

            if any(pattern in clean_line for pattern in stop_patterns):
                continue

            # Keep project technology and description lines
            if (
                "technologies used" in clean_line
                or "technology used" in clean_line
                or "description" in clean_line
            ):
                content = re.sub(r"^[●•*-]\s*", "", line).strip()

                if content:
                    bullets.append(content)

    return list(dict.fromkeys(bullets))

def detect_project_technologies(section_text):
    text = clean_text(section_text)

    technologies = [
        "python",
        "java",
        "javascript",
        "typescript",
        "c++",
        "c#",
        "html",
        "css",
        "react",
        "react.js",
        "node.js",
        "express",
        "fastapi",
        "django",
        "flask",
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "firebase",
        "aws",
        "azure",
        "docker",
        "kubernetes",
        "git",
        "github",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "pandas",
        "numpy",
        "power bi",
        "tableau",
        "excel",
        "machine learning",
        "deep learning",
        "nlp",
        "computer vision",
    ]

    detected = [
        technology
        for technology in technologies
        if technology in text
    ]

    return list(dict.fromkeys(detected))


def detect_action_verbs(section_text):
    text = clean_text(section_text)

    action_verbs = [
        "developed",
        "created",
        "built",
        "designed",
        "implemented",
        "analyzed",
        "analysed",
        "trained",
        "deployed",
        "managed",
        "automated",
        "optimized",
        "integrated",
        "configured",
        "led",
        "coordinated",
        "tested",
        "improved",
        "launched",
        "researched",
        "engineered",
        "programmed",
        "constructed",
    ]

    return [
        verb
        for verb in action_verbs
        if re.search(r"\b" + re.escape(verb) + r"\b", text)
    ]


def detect_metrics(section_text):
    if not section_text:
        return []

    patterns = [
        r"\b\d+%",
        r"\b\d+\+",
        r"\b\d+\s+(?:users|clients|customers|records|projects|items|products)\b",
        r"\b(?:reduced|increased|improved|saved|grew)\s+\w+\s+by\s+\d+%",
    ]

    metrics = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            section_text,
            flags=re.IGNORECASE
        )

        metrics.extend(matches)

    return list(dict.fromkeys(metrics))


def calculate_project_quality(
    project_entries,
    project_bullets,
    technologies,
    action_verbs,
    metrics
):
    if not project_entries:
        return 0

    score = 40

    if len(project_bullets) >= 2:
        score += 15

    if len(project_bullets) >= 4:
        score += 10

    if technologies:
        score += 15

    if action_verbs:
        score += 10

    if metrics:
        score += 3

    return min(score, 100)


def analyze_projects(resume_text, job_description=""):
    project_section = find_project_section(resume_text)

    if not project_section:
        return {
            "has_projects": False,
            "project_score": 0,
            "project_count": 0,
            "projects": [],
            "project_bullets": [],
            "technologies_detected": [],
            "action_verbs_detected": [],
            "metrics_detected": [],
            "job_relevance_score": 0,
            "matched_job_project_keywords": [],
            "missing_job_project_keywords": [],
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
        }

    project_entries = detect_project_entries(project_section)
    project_bullets = detect_project_bullets(project_section)
    technologies = detect_project_technologies(project_section)
    action_verbs = detect_action_verbs(project_section)
    metrics = detect_metrics(project_section)
    # -----------------------------------------
    # PROJECT JOB RELEVANCE
    # -----------------------------------------

    job_text = clean_text(job_description)

    project_relevant_keywords = []

    if job_text:
        jd_words = re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
            job_text
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
                and word not in project_relevant_keywords
            ):
                project_relevant_keywords.append(word)

    job_keywords = list(
        dict.fromkeys(project_relevant_keywords)
    )

    project_text = clean_text(project_section)

    matched_job_keywords = [
        keyword
        for keyword in job_keywords
        if keyword in project_text
    ]

    missing_job_keywords = [
        keyword
        for keyword in job_keywords
        if keyword not in project_text
    ]

    if job_keywords:
        job_relevance_score = round(
            (
                len(matched_job_keywords)
                / len(job_keywords)
            ) * 100
        )
    else:
        job_relevance_score = 100
    

    if not project_entries and not project_bullets:
        return {
            "has_projects": False,
            "project_score": 0,
            "project_count": 0,
            "projects": [],
            "project_bullets": [],
            "technologies_detected": [],
            "action_verbs_detected": [],
            "metrics_detected": [],
            "job_relevance_score": 0,
            "matched_job_project_keywords": [],
            "missing_job_project_keywords": [],
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
        }
   

    project_score = calculate_project_quality(
        project_entries,
        project_bullets,
        technologies,
        action_verbs,
        metrics
    )

    strengths = []
    weaknesses = []
    recommendations = []

    if technologies:
        strengths.append(
            "Project technologies or tools are clearly mentioned."
        )

    if action_verbs:
        strengths.append(
            "Project descriptions use action-oriented language."
        )

    if metrics:
        strengths.append(
            "Project includes measurable results or numbers."
        )

    if len(project_bullets) >= 2:
        strengths.append(
            "Project has supporting description points."
        )

    if not technologies:
        weaknesses.append(
            "Project technologies or tools are not clearly mentioned."
        )

        recommendations.append(
            "Mention the main technologies, tools or methods used in the project."
        )

    if not action_verbs:
        weaknesses.append(
            "Project description lacks strong action verbs."
        )

        recommendations.append(
            "Start project bullets with clear action verbs such as developed, designed, implemented or analyzed."
        )

    if not metrics:
        weaknesses.append(
            "Project does not show measurable results."
        )

        recommendations.append(
            "Add measurable outcomes where possible, such as users, accuracy, performance improvement, time saved or records processed."
        )

    if len(project_bullets) < 2:
        weaknesses.append(
            "Project description is too short."
        )

        recommendations.append(
            "Add 2-4 concise bullets explaining your role, work and outcome."
        )

    if job_keywords and job_relevance_score < 50:
        weaknesses.append(
            "Projects have limited alignment with the provided job description."
        )

        recommendations.append(
            "Highlight project work and skills that are directly relevant to the target job."
        )

    return {
        "has_projects": True,
        "project_score": project_score,
        "project_count": len(project_entries),
        "projects": project_entries,
        "project_bullets": project_bullets,
        "technologies_detected": technologies,
        "action_verbs_detected": action_verbs,
        "metrics_detected": metrics,
        "job_relevance_score": job_relevance_score,
        "matched_job_project_keywords": matched_job_keywords,
        "missing_job_project_keywords": missing_job_keywords,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
    }