import re


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_keywords(text):
    text = clean_text(text)

    keywords = [
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "react.js",
        "node.js",
        "node",
        "html",
        "css",
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "c++",
        "c#",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",
        "data analysis",
        "natural language processing",
        "nlp",
        "computer vision",
        "pandas",
        "numpy",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "power bi",
        "tableau",
        "excel",
        "aws",
        "azure",
        "google cloud",
        "docker",
        "kubernetes",
        "git",
        "github",
        "rest api",
        "api",
        "fastapi",
        "django",
        "flask",
        "communication",
        "leadership",
        "teamwork",
        "problem solving",
        "project management",
        "agile",
        "scrum",
    ]

    found = []

    for keyword in keywords:
        if keyword in text:
            found.append(keyword)

    return found

def extract_requirement_signals(job_description):
    text = clean_text(job_description)

    required_signals = [
        "required",
        "must have",
        "must-have",
        "minimum",
        "mandatory",
        "required skills",
        "requirements",
        "qualifications",
        "you must",
        "should have",
    ]

    preferred_signals = [
        "preferred",
        "nice to have",
        "nice-to-have",
        "plus",
        "bonus",
        "preferred skills",
        "good to have",
    ]

    return {
        "required_signals": required_signals,
        "preferred_signals": preferred_signals,
    }





def extract_requirement_keywords(job_description):
    text = clean_text(job_description)

    all_keywords = extract_keywords(text)

    signals = extract_requirement_signals(text)

    required_keywords = []
    preferred_keywords = []

    required_signals = signals["required_signals"]
    preferred_signals = signals["preferred_signals"]

    for keyword in all_keywords:
        position = text.find(keyword)

        if position == -1:
            continue

        nearby_text = text[max(0, position - 150):position]

        if any(signal in nearby_text for signal in required_signals):
            required_keywords.append(keyword)

        elif any(signal in nearby_text for signal in preferred_signals):
            preferred_keywords.append(keyword)

    return {
        "required_keywords": list(dict.fromkeys(required_keywords)),
        "preferred_keywords": list(dict.fromkeys(preferred_keywords)),
    }
def extract_job_titles(job_description):
    text = clean_text(job_description)

    
    job_titles = [
    # =========================
    # TECHNOLOGY
    # =========================
    "software engineer",
    "software developer",
    "software development",
    "data analyst",
    "data scientist",
    "data engineer",
    "machine learning engineer",
    "ai engineer",
    "frontend developer",
    "backend developer",
    "full stack developer",
    "web developer",
    "python developer",
    "java developer",
    "react developer",
    "devops engineer",
    "cloud engineer",
    "cyber security analyst",
    "cybersecurity analyst",
    "network engineer",
    "database administrator",
    "system administrator",
    "qa engineer",
    "software tester",
    "test engineer",
    "technical support engineer",

    # =========================
    # SALES
    # =========================
    "sales executive",
    "sales associate",
    "sales representative",
    "sales officer",
    "sales consultant",
    "sales manager",
    "sales coordinator",
    "business development executive",
    "business development associate",
    "business development representative",
    "business development manager",
    "account executive",
    "account manager",
    "territory sales manager",
    "regional sales manager",
    "area sales manager",
    "retail sales executive",
    "inside sales executive",
    "field sales executive",
    "b2b sales executive",
    "sales trainee",

    # =========================
    # MARKETING
    # =========================
    "marketing executive",
    "marketing associate",
    "marketing analyst",
    "marketing manager",
    "digital marketing executive",
    "digital marketing specialist",
    "digital marketing manager",
    "social media executive",
    "social media specialist",
    "social media manager",
    "content marketing executive",
    "content marketing manager",
    "brand executive",
    "brand manager",
    "marketing coordinator",
    "marketing consultant",
    "market research analyst",
    "public relations executive",
    "public relations manager",
    "media planner",
    "media buyer",

    # =========================
    # HUMAN RESOURCES
    # =========================
    "hr executive",
    "hr associate",
    "hr assistant",
    "hr coordinator",
    "hr recruiter",
    "human resources executive",
    "human resources specialist",
    "human resources manager",
    "recruitment executive",
    "recruiter",
    "talent acquisition executive",
    "talent acquisition specialist",
    "talent acquisition manager",
    "hr generalist",
    "hr intern",
    "payroll executive",
    "training and development executive",

    # =========================
    # FINANCE & ACCOUNTING
    # =========================
    "accountant",
    "accounts executive",
    "accounts assistant",
    "accounts officer",
    "senior accountant",
    "finance executive",
    "finance analyst",
    "financial analyst",
    "finance manager",
    "financial advisor",
    "financial planner",
    "audit executive",
    "auditor",
    "internal auditor",
    "tax analyst",
    "tax consultant",
    "payroll specialist",
    "bookkeeper",
    "investment analyst",
    "credit analyst",
    "banking executive",
    "banking officer",
    "loan officer",

    # =========================
    # CUSTOMER SERVICE / BPO
    # =========================
    "customer service executive",
    "customer service representative",
    "customer support executive",
    "customer support representative",
    "customer care executive",
    "customer care representative",
    "client service executive",
    "client service representative",
    "customer relationship executive",
    "customer relationship manager",
    "relationship manager",
    "call center executive",
    "call centre executive",
    "call center representative",
    "call centre representative",
    "chat support executive",
    "email support executive",
    "technical support representative",
    "help desk executive",
    "support executive",
    "process associate",
    "process executive",
    "bpo executive",
    "bpo associate",

    # =========================
    # OPERATIONS
    # =========================
    "operations executive",
    "operations associate",
    "operations analyst",
    "operations coordinator",
    "operations manager",
    "business operations executive",
    "business operations analyst",
    "administrative assistant",
    "administrative executive",
    "administrative officer",
    "office administrator",
    "office executive",
    "office manager",
    "project coordinator",
    "project manager",
    "program coordinator",
    "program manager",
    "management trainee",
    "management analyst",

    # =========================
    # LOGISTICS / SUPPLY CHAIN
    # =========================
    "logistics executive",
    "logistics coordinator",
    "logistics manager",
    "supply chain executive",
    "supply chain analyst",
    "supply chain manager",
    "procurement executive",
    "procurement specialist",
    "procurement manager",
    "purchase executive",
    "purchase officer",
    "warehouse executive",
    "warehouse manager",
    "inventory executive",
    "inventory manager",
    "transportation coordinator",

    # =========================
    # HOSPITALITY
    # =========================
    "hotel manager",
    "hotel operations manager",
    "front office executive",
    "front office associate",
    "front desk executive",
    "front desk associate",
    "guest relations executive",
    "guest relations officer",
    "guest service executive",
    "guest service associate",
    "reservation executive",
    "reservations executive",
    "hotel sales executive",
    "food and beverage executive",
    "food and beverage manager",
    "restaurant manager",
    "restaurant supervisor",
    "housekeeping executive",
    "housekeeping supervisor",
    "event coordinator",
    "event manager",

    # =========================
    # RETAIL
    # =========================
    "retail executive",
    "retail associate",
    "retail sales associate",
    "store executive",
    "store manager",
    "store supervisor",
    "store incharge",
    "store in-charge",
    "retail manager",
    "retail operations executive",
    "merchandiser",
    "visual merchandiser",

    # =========================
    # EDUCATION
    # =========================
    "teacher",
    "school teacher",
    "primary teacher",
    "secondary teacher",
    "subject teacher",
    "lecturer",
    "assistant professor",
    "professor",
    "academic coordinator",
    "academic counselor",
    "education counselor",
    "career counselor",
    "student counselor",
    "admission counselor",
    "content educator",
    "trainer",
    "corporate trainer",

    # =========================
    # HEALTHCARE
    # =========================
    "hospital administrator",
    "hospital administration executive",
    "healthcare executive",
    "healthcare administrator",
    "medical representative",
    "medical sales executive",
    "clinical coordinator",
    "patient care executive",
    "patient coordinator",
    "pharmacy assistant",
    "lab technician",
    "medical receptionist",

    # =========================
    # REAL ESTATE
    # =========================
    "real estate executive",
    "real estate sales executive",
    "property consultant",
    "property advisor",
    "real estate consultant",
    "real estate manager",
    "property manager",
    "leasing executive",
    "real estate relationship manager",

    # =========================
    # CONTENT / CREATIVE
    # =========================
    "content writer",
    "content writer executive",
    "content creator",
    "copywriter",
    "copywriting executive",
    "technical writer",
    "editor",
    "proofreader",
    "graphic designer",
    "ui designer",
    "ux designer",
    "video editor",
    "social media content creator",

    # =========================
    # LEGAL / COMPLIANCE
    # =========================
    "legal executive",
    "legal assistant",
    "legal associate",
    "compliance executive",
    "compliance analyst",
    "compliance officer",
    "legal advisor",

    # =========================
    # FRESHER / ENTRY LEVEL
    # =========================
    "fresher",
    "graduate trainee",
    "trainee",
    "management trainee",
    "intern",
    "graduate intern",
    "sales intern",
    "marketing intern",
    "hr intern",
    "finance intern",
    "operations intern",
    "business development intern",
    "customer service intern",
]
    found = []

    for title in job_titles:
        if title in text:
            found.append(title)

    return found
def extract_job_phrases(job_description):
    text = clean_text(job_description)

    phrases = [
        "bachelor",
        "master",
        "btech",
        "mtech",
        "computer science",
        "software engineer",
        "software developer",
        "data scientist",
        "data analyst",
        "machine learning engineer",
        "frontend developer",
        "backend developer",
        "full stack developer",
        "web developer",
        "internship",
        "intern",
        "experience",
        "years experience",
        "problem solving",
        "communication",
        "leadership",
        "teamwork",
        "analytical skills",
    ]

    found = []

    for phrase in phrases:
        if phrase in text:
            found.append(phrase)

    return found
def match_job_description(resume_text, job_description):
    resume_text_clean = clean_text(resume_text)
    job_text_clean = clean_text(job_description)

    if not job_text_clean:
        return {
            "job_match_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "job_keywords": [],
            "resume_keywords": [],
            "message": "Job description was not provided."
        }

    resume_keywords = extract_keywords(resume_text_clean)
    job_keywords = extract_keywords(job_text_clean)
    job_titles = extract_job_titles(job_text_clean)


    
    matched_job_titles = [
        title
        for title in job_titles
        if title in resume_text_clean
    ]

    if len(job_titles) > 0:
        title_match_score = round(
            (len(matched_job_titles) / len(job_titles)) * 100
        )
    else:
        title_match_score = 100

    requirement_data = extract_requirement_keywords(job_text_clean)

    required_keywords = requirement_data["required_keywords"]
    preferred_keywords = requirement_data["preferred_keywords"]

    matched_required_keywords = [
        keyword
        for keyword in required_keywords
        if keyword in resume_keywords
    ]

    missing_required_keywords = [
        keyword
        for keyword in required_keywords
        if keyword not in resume_keywords
    ]

    matched_preferred_keywords = [
        keyword
        for keyword in preferred_keywords
        if keyword in resume_keywords
    ]

    missing_preferred_keywords = [
        keyword
        for keyword in preferred_keywords
        if keyword not in resume_keywords
    ]

    matched_keywords = [
        keyword
        for keyword in job_keywords
        if keyword in resume_keywords
    ]

    missing_keywords = [
        keyword
        for keyword in job_keywords
        if keyword not in resume_keywords
    ]

    if len(required_keywords) > 0:
        required_match_score = round(
            (len(matched_required_keywords) / len(required_keywords)) * 100
        )
    else:
        required_match_score = 100

    if len(preferred_keywords) > 0:
        preferred_match_score = round(
            (len(matched_preferred_keywords) / len(preferred_keywords)) * 100
        )
    else:
        preferred_match_score = 100

    if len(job_keywords) > 0:
        keyword_match_score = round(
            (required_match_score * 0.70)
            + (preferred_match_score * 0.30)
        )
    else:
        keyword_match_score = 0

    job_phrases = extract_job_phrases(job_text_clean)

    matched_phrases = [
        phrase
        for phrase in job_phrases
        if phrase in resume_text_clean
    ]

    if len(job_phrases) > 0:
        phrase_match_score = round(
            (len(matched_phrases) / len(job_phrases)) * 100
        )
    else:
        phrase_match_score = 100

    job_match_score = round(
        (keyword_match_score * 0.75)
        + (phrase_match_score * 0.25)
    )

    return {
        "job_match_score": job_match_score,
        "keyword_match_score": keyword_match_score,
        "phrase_match_score": phrase_match_score,
                "title_match_score": title_match_score,
        "matched_job_titles": matched_job_titles,





        "job_keywords": job_keywords,
        "resume_keywords": resume_keywords,

        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,

        "job_titles": job_titles,

        "required_match_score": required_match_score,
        "preferred_match_score": preferred_match_score,

        "required_keywords": required_keywords,
        "preferred_keywords": preferred_keywords,

        "matched_required_keywords": matched_required_keywords,
        "missing_required_keywords": missing_required_keywords,

        "matched_preferred_keywords": matched_preferred_keywords,
        "missing_preferred_keywords": missing_preferred_keywords,

        "job_phrases": job_phrases,
        "matched_phrases": matched_phrases,
    }