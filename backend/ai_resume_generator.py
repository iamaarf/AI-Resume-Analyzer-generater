import os
import re
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


# ============================================================
# DEMO MODE
# ============================================================

# True = testing/demo ke liye short information ko
# AI-generated illustrative detail se expand karega.
#
# IMPORTANT:
# Is mode ke generated details ko real job application
# mein factual experience ke roop mein use nahi karna.
#
# False = factual mode.
DEMO_EXPANSION_MODE = True


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(
    api_key=api_key
)


# ============================================================
# STRUCTURED OUTPUT SCHEMA
# ============================================================
def clean_list_items(items):
    """
    Ensures AI-generated skills and technologies
    are returned as separate readable list items.
    """

    if not items:
        return []

    cleaned = []

    known_terms = [
        "Component-Based Architecture",
        "Cross-Browser Compatibility",
        "Performance Optimization",
        "Responsive Web Design",
        "Data Cleaning & Preprocessing",
        "Microsoft Excel",
        "Data Visualization",
        "Data Modeling",
        "Data Analysis",
        "Business Intelligence",
        "Statistical Analysis",
        "Database Management",
        "Relational Databases",
        "Machine Learning",
        "Problem Solving",
        "UI Development",
        "REST APIs",
        "REST API",
        "Power Query",
        "Power BI",
        "Tailwind CSS",
        "React.js",
        "JavaScript",
        "HTML5",
        "CSS3",
        "Bootstrap",
        "GitHub",
        "Debugging",
        "SQL",
        "DAX",
        "Python",
        "Tableau",
        "Excel",
        "Git",
        "CSS",
        "HTML",
        "APIs",
        "ETL",
        "BI",
    ]

    # Longer terms must be checked first.
    known_terms = sorted(
        known_terms,
        key=len,
        reverse=True
    )

    for item in items:

        if not isinstance(item, str):
            continue

        text = item.strip()

        if not text:
            continue

        # First handle normal separators.
        text = re.sub(
            r"\s*[,;|]\s*",
            "|||",
            text
        )

        parts = text.split("|||")

        for part in parts:

            part = part.strip()

            if not part:
                continue

            # Split only when a complete known term
            # is joined to another known term.
            found_parts = []
            remaining = part

            while remaining:

                matched = False

                for term in known_terms:

                    if remaining == term:
                        found_parts.append(term)
                        remaining = ""
                        matched = True
                        break

                    if remaining.startswith(term):
                        found_parts.append(term)
                        remaining = remaining[len(term):].strip()
                        matched = True
                        break

                if matched:
                    continue

                # If the remaining text starts with a known
                # term after some other text, find that boundary.
                boundary_found = False

                for term in known_terms:

                    position = remaining.find(term)

                    if position > 0:

                        before = remaining[:position].strip()

                        if before:
                            found_parts.append(before)

                        found_parts.append(term)

                        remaining = (
                            remaining[
                                position + len(term):
                            ].strip()
                        )

                        boundary_found = True
                        break

                if boundary_found:
                    continue

                # Nothing else to split.
                found_parts.append(remaining)
                remaining = ""

            for value in found_parts:

                value = value.strip()

                if value and value not in cleaned:
                    cleaned.append(value)

    return cleaned
class WorkExperienceItem(BaseModel):

    title: str = Field(
        description="Job title."
    )

    company: str = Field(
        description="Company name."
    )

    dates: str = Field(
        description="Employment dates."
    )

    responsibilities: list[str] = Field(
        description=(
            "Professional, detailed, ATS-friendly and "
            "achievement-oriented work experience bullets."
        )
    )


class EducationItem(BaseModel):

    degree: str = Field(
        description="Degree."
    )

    specialization: str = Field(
        description="Field or specialization."
    )

    institution: str = Field(
        description="University or college."
    )

    year: str = Field(
        description="Education year."
    )


class ProjectItem(BaseModel):

    name: str = Field(
        description="Project name."
    )

    technologies: list[str] = Field(
    description=(
        "Technologies used in the project. "
        "IMPORTANT: Every technology MUST be a separate "
        "item in the list. Never concatenate multiple "
        "technologies into one string. For example, return "
        "['Excel', 'Power BI', 'SQL'] instead of "
        "['ExcelPower BISQL']."
    )
)

    description: str = Field(
        description=(
            "Detailed professional project description "
            "relevant to the target job."
        )
    )

    responsibilities: list[str] = Field(
        description=(
            "Detailed, professional and target-role-relevant "
            "project bullets."
        )
    )


class CertificationItem(BaseModel):

    name: str = Field(
        description="Certification name."
    )

    organization: str = Field(
        description="Issuing organization."
    )

    date: str = Field(
        description="Certification date."
    )


class ResumeOutput(BaseModel):

    professional_summary: str = Field(
        description="Detailed professional resume summary."
    )

    skills: list[str] = Field(
    description=(
        "Professional and job-relevant skills list. "
        "IMPORTANT: Every skill MUST be a separate item "
        "in the list. Never combine multiple skills into one "
        "string. For example, return ['SQL', 'Power BI', "
        "'Microsoft Excel', 'Data Visualization'] instead of "
        "['SQLPower BIMicrosoft ExcelData Visualization']."
    )
)

    work_experience: list[WorkExperienceItem] = Field(
        description="Detailed and achievement-oriented work experience."
    )

    education: list[EducationItem] = Field(
        description="Education."
    )

    projects: list[ProjectItem] = Field(
        description="Detailed and target-role-relevant projects."
    )

    certifications: list[CertificationItem] = Field(
        description="Certifications."
    )

    languages: list[str] = Field(
        description="Languages."
    )

    matched_keywords: list[str] = Field(
        description=(
            "Important job-description keywords that are "
            "supported by the candidate information and "
            "naturally reflected in the generated resume."
        )
    )

    missing_requirements: list[str] = Field(
        description=(
            "Important job requirements that are not supported "
            "by the candidate information."
        )
    )

    # ========================================================
    # NEW ATS ENGINE OUTPUT
    # ========================================================

    ats_match_score: int = Field(
        description=(
            "Estimated ATS match score from 0 to 100 based on "
            "job title relevance, required skills, relevant "
            "experience, projects, education, certifications, "
            "keywords and overall job-description alignment. "
            "This is an internal estimate and not a guaranteed "
            "score from a real company's ATS."
        )
    )

    ats_matched_keywords: list[str] = Field(
        description=(
            "Important job-description keywords and phrases "
            "that are supported by the candidate's actual "
            "information and used naturally in the resume."
        )
    )

    ats_missing_keywords: list[str] = Field(
        description=(
            "Important job-description keywords, skills, tools "
            "or requirements that are not supported by the "
            "candidate information."
        )
    )

    ats_suggestions: list[str] = Field(
        description=(
            "Specific and actionable suggestions for improving "
            "ATS relevance and recruiter readability without "
            "inventing candidate facts."
        )
    )


# ============================================================
# AI RESUME GENERATOR
# ============================================================

def generate_ai_resume(resume_data: dict) -> dict:

    # --------------------------------------------------------
    # CANDIDATE DATA
    # --------------------------------------------------------

    name = resume_data.get("name", "")
    email = resume_data.get("email", "")
    phone = resume_data.get("phone", "")
    location = resume_data.get("location", "")
    linkedin = resume_data.get("linkedin", "")

    target_role = resume_data.get("targetRole", "")
    job_description = resume_data.get("jobDescription", "")

    experiences = resume_data.get("experiences", [])
    projects = resume_data.get("projects", [])
    skills = resume_data.get("skills", "")
    education = resume_data.get("education", [])
    certifications = resume_data.get("certifications", [])


    # ========================================================
    # MODE INSTRUCTION
    # ========================================================

    if DEMO_EXPANSION_MODE:

        expansion_instruction = """
DEMO EXPANSION MODE IS ENABLED.

This is a controlled product-testing/demo environment.

The candidate may provide extremely short information.

When the candidate provides short information, you MAY
generate realistic, plausible, illustrative professional
details to demonstrate what the finished ResumeAI product
could look like.

For example, if the candidate says:

"Maintained employee records in Excel."

you may expand the experience into several realistic
professional resume bullets.

However, clearly avoid extreme claims.

DO NOT generate unrealistic achievements such as:

- Increased revenue by 75%
- Reduced costs by 60%
- Managed a team of 50 people
- Served 10,000 customers

unless those facts were actually provided.

Do not create dramatic achievements, fake awards,
fake companies, fake degrees, fake certifications,
or impossible claims.

The purpose of DEMO EXPANSION_MODE is to create a realistic
ILLUSTRATIVE resume for product testing.

For this demo mode:

SHORT INPUT -> EXPAND PROFESSIONALLY.

DETAILED INPUT -> PRESERVE THE DETAIL AND EXPAND/ORGANIZE IT.

Do not unnecessarily shorten detailed information.

Use the target role and job description to make the
generated resume professionally relevant.

The generated expanded details are DEMO CONTENT and must
not be treated as verified candidate facts.
"""

    else:

        expansion_instruction = """
FACTUAL MODE IS ENABLED.

The candidate information is the only source of truth.

Do not invent responsibilities, achievements, metrics,
skills, technologies, certifications, education,
customers, users, revenue, team sizes, or results.

You may only professionally rewrite and organize
information supplied by the candidate.

SHORT INPUT -> keep it accurate.

DETAILED INPUT -> preserve and professionally organize it.

If an achievement metric is not provided, do not invent
a number. Instead describe the contribution accurately
without a fabricated result.
"""


    # ========================================================
    # MASTER PROMPT
    # ========================================================

    prompt = f"""

You are an expert:

- Professional Resume Writer
- ATS Resume Optimization Specialist
- Recruiter-focused Resume Editor
- Job Description Matching Specialist
- Resume Quality Analyst

Your task is to transform the candidate's raw information
into a professional, detailed, ATS-friendly,
job-targeted resume.

============================================================
CURRENT MODE
============================================================

{expansion_instruction}

============================================================
1. CORE OBJECTIVE
============================================================

The final resume should NOT look artificially short.

The goal is:

Professional
Detailed
Readable
ATS-friendly
Job-targeted
HR-friendly
Evidence-based
Achievement-oriented

Use the available candidate information effectively.

If information is short and DEMO_EXPANSION_MODE is enabled,
expand it with realistic illustrative professional content.

If information is already detailed,
preserve the detail and organize it professionally.

Do not rewrite the candidate into a completely different
career profile.

============================================================
2. JD-BASED RESUME TAILORING
============================================================

The JOB DESCRIPTION is extremely important.

First analyze the job description before writing the resume.

Identify:

- target job title
- core responsibilities
- required skills
- preferred skills
- tools
- technologies
- qualifications
- domain terminology
- important action words
- important business terminology
- important ATS keywords
- important phrases

Then compare these requirements with the candidate's:

- experience
- projects
- skills
- education
- certifications

Use only relevant supported requirements.

Naturally tailor the resume toward the target job.

The generated resume should feel specifically written
for the supplied job description rather than being a
generic resume.

Do NOT keyword stuff.

Do NOT copy the job description.

Do NOT insert unsupported skills simply because they
appear in the job description.

============================================================
3. RESUME LENGTH
============================================================

Use the candidate's experience level and amount of information.

General target:

Fresher / Entry Level:
300–500 words when appropriate.

0–3 years:
400–600 words when appropriate.

3–7 years:
500–800 words when appropriate.

7–10+ years:
600–1000+ words when appropriate.

Senior / Executive:
800–1200+ words when enough information exists.

These are GUIDELINES, not hard requirements.

Do not add meaningless filler.

Do not artificially increase word count.

Use additional space only when it improves professional
quality, relevance, clarity or evidence.

============================================================
4. PROFESSIONAL SUMMARY
============================================================

Create a strong professional summary.

Target:

Fresher:
approximately 70–110 words.

Experienced:
approximately 80–130 words.

The summary should prioritize information that matters
for the target job.

Use relevant:

- experience
- target role
- skills
- technologies
- domain knowledge
- projects
- education
- certifications

Use job-description terminology naturally when supported.

Do not create unsupported achievements.

Do not make the summary repetitive.

Do not turn the summary into a keyword list.

============================================================
5. WORK EXPERIENCE
============================================================

For every experience:

Preserve:

- job title
- company
- dates

Then create a detailed professional experience section.

TARGET:

Short experience:
3–5 bullets.

Normal experience:
4–6 bullets.

Detailed experience:
5–8 bullets.

============================================================
EXPERIENCE BULLET QUALITY
============================================================

Do not make every bullet a generic responsibility.

Whenever supported by candidate information, structure
bullets around:

ACTION + WORK PERFORMED + TOOL/CONTEXT + RESULT/IMPACT

Examples:

Developed
Analyzed
Managed
Improved
Automated
Created
Implemented
Coordinated
Validated
Optimized
Monitored
Prepared
Supported
Reviewed

Prioritize meaningful contributions.

If the candidate supplied metrics or measurable results,
preserve them.

If the candidate did NOT supply a metric:

DO NOT invent a percentage, revenue figure, user count,
cost reduction, team size or other numerical achievement.

In DEMO_EXPANSION_MODE, you may expand responsibilities
realistically, but do not create unrealistic numerical
achievements.

============================================================
6. PROJECTS
============================================================

Projects should NOT be one-line entries when enough
information exists.

For each project provide:

- project name
- technologies
- detailed description
- 2–5 professional bullets

The project should explain:

- what problem or business need it addresses
- what was created
- what technologies were involved
- what analysis/development/work was performed
- important functionality
- relevant business or technical context
- how it relates to the target role

Projects should be tailored to the job description.

If SQL appears in the JD and the project genuinely uses
SQL, reflect that naturally.

If Power BI appears in the JD and the project genuinely
uses Power BI, reflect that naturally.

Do not add technologies that the candidate did not provide
unless DEMO_EXPANSION_MODE explicitly allows reasonable
illustrative expansion.

Do not make extreme project claims.

============================================================
7. SKILLS
============================================================

Organize skills professionally.

Keep skills relevant to the target role.

Prioritize skills that are:

1. explicitly provided by candidate
2. demonstrated in experience
3. demonstrated in projects
4. strongly relevant to the target JD

Do not create a huge random skill list.

============================================================
SKILL EVIDENCE RULE
============================================================

Whenever possible, important skills listed in the Skills
section should also have evidence somewhere in:

- Work Experience
- Projects
- Summary

Example:

If the candidate has:

SQL

then relevant SQL work should appear in experience/project
content when supported.

If the candidate has:

Power BI

then Power BI dashboard/reporting work should appear
when supported.

If a skill cannot reasonably be connected to any
candidate evidence, do not artificially force it into
experience.

This creates a strong:

SKILL -> EVIDENCE

relationship.

============================================================
8. JOB DESCRIPTION / ATS ANALYSIS
============================================================

Analyze the target job description deeply.

Identify:

- important keywords
- required skills
- preferred skills
- tools
- technologies
- qualifications
- responsibilities
- domain terminology
- important job-title terminology

Then map them against candidate evidence.

Use relevant supported keywords naturally in:

- summary
- skills
- work experience
- projects

Do not keyword stuff.

Avoid unnecessary repetition.

The resume should sound like a professional resume,
not like a copied job description.

============================================================
9. ATS MATCH SCORE
============================================================

Calculate an ESTIMATED ATS MATCH SCORE from 0 to 100.

This is an internal ResumeAI estimate.

It is NOT a guaranteed score from the employer's ATS.

Consider:

- target job title relevance
- required skill coverage
- preferred skill coverage
- relevant experience
- responsibility alignment
- project relevance
- keyword coverage
- education requirements
- certification relevance
- natural keyword placement
- evidence of important skills

Do not give a high score simply because many keywords
appear.

Evidence and relevance are more important than keyword count.

The score should reflect the supplied candidate data
and the supplied job description.

============================================================
10. MATCHED KEYWORDS
============================================================

Return important job-description keywords that:

- are supported by candidate information
- are relevant to the target role
- are naturally reflected in the generated resume

Keep the list meaningful.

Do not return every common word.

============================================================
11. MISSING KEYWORDS
============================================================

Return important job-description requirements that are
not supported by candidate information.

Examples:

- required technology not provided
- required certification not provided
- required experience area not provided
- required responsibility not demonstrated

Do NOT treat every unsupported phrase as missing.

Only include meaningful requirements.

============================================================
12. ATS SUGGESTIONS
============================================================

Return practical suggestions for improving the resume
against the supplied JD.

Suggestions can include:

- add missing skill if genuinely possessed
- add relevant project if genuinely completed
- provide measurable achievement if known
- clarify responsibility
- add relevant certification if actually held
- strengthen evidence for an important skill
- clarify experience with a required tool

IMPORTANT:

Suggestions must NOT tell the candidate to lie.

Never suggest inventing:

- experience
- metrics
- certifications
- companies
- education
- achievements
- technologies

============================================================
13. EDUCATION
============================================================

Keep education concise and professional.

Include:

Degree
Specialization
Institution
Year

Do not create unnecessary education bullets.

============================================================
14. CERTIFICATIONS
============================================================

Include:

Certification
Organization
Date

In DEMO_EXPANSION_MODE, do NOT invent random
certifications.

Only use certifications supplied by the candidate.

============================================================
15. LANGUAGES
============================================================

Use explicitly supplied languages.

Do not create a large language list.

============================================================
16. HR READABILITY
============================================================

The resume must be easy for a recruiter to scan.

Use:

- strong action verbs
- concise professional bullets
- clear section hierarchy
- relevant keywords
- specific terminology
- consistent wording
- readable spacing

Avoid:

- emojis
- decorative text
- excessive symbols
- huge paragraphs
- repetitive sentences
- keyword stuffing
- unnecessary jargon

============================================================
17. DEMO EXPANSION RULE
============================================================

DEMO_EXPANSION_MODE is being used because we are testing
the ResumeAI product.

Therefore:

If the candidate gives:

"Maintained employee records in Excel."

do NOT return only:

"Maintained employee records using Microsoft Excel."

Instead create a realistic professionally expanded
experience section.

However, do not invent dramatic achievements.

If the candidate provides:

"Created sales dashboard using Excel, Power BI and SQL."

do NOT return only one sentence.

Create a properly structured project with:

- professional description
- several relevant bullets
- technologies
- target-role relevance
- business analysis context where appropriate

If the candidate provides substantial details,
use those details instead of replacing them with
generic content.

============================================================
18. NO UNREALISTIC CLAIMS
============================================================

Even in DEMO mode, avoid absurd claims.

Do NOT randomly create:

- huge revenue numbers
- massive user counts
- famous clients
- unrealistic percentages
- executive responsibilities
- senior leadership claims
- prestigious awards
- fake certifications
- fake degrees

If a numerical achievement was not supplied,
do not manufacture one.

============================================================
19. CANDIDATE EVIDENCE PRIORITY
============================================================

When deciding what to include, prioritize:

1. Candidate-provided facts
2. Candidate-provided skills
3. Candidate-provided experience
4. Candidate-provided projects
5. Candidate-provided education
6. Candidate-provided certifications
7. Relevant JD terminology
8. Reasonable DEMO expansion only when DEMO mode is enabled

Never allow the job description to overwrite
candidate reality.

============================================================
20. FINAL QUALITY CHECK
============================================================

Before returning the result, check:

- Is the resume detailed enough?
- Is the summary strong?
- Is the resume specifically tailored to the JD?
- Are experience bullets meaningful?
- Are bullets achievement-oriented where evidence allows?
- Are projects sufficiently detailed?
- Are projects relevant to the target role?
- Are skills relevant?
- Does important skill have evidence?
- Are JD keywords naturally used?
- Are missing requirements correctly identified?
- Is the ATS score reasonable?
- Are ATS suggestions actionable?
- Is the content readable?
- Is the resume ATS-friendly?
- Is the resume unnecessarily short?
- If input was short, did DEMO mode expand it?
- If input was detailed, did the model preserve that detail?
- Did the model avoid fake numerical achievements?
- Did the model avoid fake certifications?
- Did the model avoid unsupported technologies?

============================================================
CANDIDATE DATA
============================================================

PERSONAL INFORMATION

Name:
{name}

Email:
{email}

Phone:
{phone}

Location:
{location}

LinkedIn:
{linkedin}


============================================================
TARGET ROLE
============================================================

{target_role}


============================================================
JOB DESCRIPTION
============================================================

{job_description}


============================================================
WORK EXPERIENCE
============================================================

{experiences}


============================================================
PROJECTS
============================================================

{projects}


============================================================
SKILLS
============================================================

{skills}


============================================================
EDUCATION
============================================================

{education}


============================================================
CERTIFICATIONS
============================================================

{certifications}


============================================================
FINAL OUTPUT
============================================================

Return ONLY the structured JSON object.

Do not return explanations outside the schema.

The ATS fields must be populated:

- ats_match_score
- ats_matched_keywords
- ats_missing_keywords
- ats_suggestions

The existing fields must also be populated:

- professional_summary
- skills
- work_experience
- education
- projects
- certifications
- languages
- matched_keywords
- missing_requirements

============================================================
FINAL INSTRUCTION
============================================================

Generate the best possible professional resume using
the candidate information and target job description.

Do not sacrifice factual accuracy for ATS keywords.

Do not sacrifice readability for keyword matching.

Do not sacrifice professional quality for word count.

The final result should look like a real,
job-targeted professional resume.
"""


    # ========================================================
    # GEMINI GENERATION
    # ========================================================

       # ========================================================
    # GEMINI GENERATION WITH RETRY + FALLBACK
    # ========================================================

    generation_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ResumeOutput,
        max_output_tokens=10000,
    )

    models_to_try = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.5-flash",
    ]

    response = None
    last_error = None

    for model_name in models_to_try:

        for attempt in range(3):

            try:
                print(
                    f"Resume generation: "
                    f"{model_name}, attempt {attempt + 1}/3"
                )

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=generation_config,
                )

                if response and response.text:
                    print(
                        f"Resume generation successful "
                        f"with {model_name}"
                    )
                    break

            except Exception as error:

                last_error = error

                print(
                    f"Resume generation failed: "
                    f"{model_name}, "
                    f"attempt {attempt + 1}/3: "
                    f"{error}"
                )

                # Wait before retrying.
                if attempt < 2:
                    wait_seconds = 2 ** attempt
                    time.sleep(wait_seconds)

        if response and response.text:
            break

    if not response or not response.text:
        print(
            "All Gemini resume generation attempts failed:",
            last_error
        )

        raise RuntimeError(
            "Unable to generate resume after multiple attempts."
        )


    # ========================================================
    # VALIDATE RESPONSE
    # ========================================================
    result = ResumeOutput.model_validate_json(
        response.text
    )

    # ========================================================
    # CLEAN SKILLS AND PROJECT TECHNOLOGIES
    # ========================================================

    result.skills = clean_list_items(
        result.skills
    )

    for project in result.projects:

        project.technologies = clean_list_items(
            project.technologies
        )

    return result.model_dump()