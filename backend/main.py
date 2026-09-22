from fastapi import (
    FastAPI,
    UploadFile,
    HTTPException,
    Form,
    Depends
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from pypdf import PdfReader
from docx import Document
from io import BytesIO
import fitz
import pytesseract
from PIL import Image

from ats_analyzer import analyze_resume
from job_matcher import match_job_description
from experience_analyzer import analyze_experience
from education_analyzer import analyze_education
from project_analyzer import analyze_projects

from error_handler import (
    unsupported_file_error,
    empty_file_error,
    unreadable_file_error,
    empty_resume_error,
    server_error,
)

from analytics_routes import (
    record_resume_analysis,
    get_admin_analytics,
    get_admin_daily_analytics,
    get_admin_monthly_analytics,
    get_admin_yearly_analytics,
)

from admin_auth import (
    login_admin,
    get_current_admin,
)
from resume_builder_routes import router as resume_builder_router

app = FastAPI()
app.include_router(
    resume_builder_router
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://ai-resume-analyzer-generater-1.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer Backend is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.post("/analyze-resume")
async def analyze_resume_endpoint(
    file: UploadFile,
    job_description: str = Form("")
):

    if not file.filename:
        raise empty_file_error()

    filename = file.filename.lower()

    if not filename.endswith((".pdf", ".docx")):
        raise unsupported_file_error()

    file_data = await file.read()

    if not file_data:
        raise empty_file_error()

    extracted_text = ""
    if filename.endswith(".pdf"):
        try:
            pdf_document = fitz.open(
                stream=file_data,
                filetype="pdf"
            )

            for page in pdf_document:
                text = page.get_text()

                if text and text.strip():
                    extracted_text += text + "\n"

            pdf_document.close()

        except Exception:
            raise unreadable_file_error()

    elif filename.endswith(".docx"):
        try:
            document = Document(
                BytesIO(file_data)
            )

            for paragraph in document.paragraphs:
                if paragraph.text.strip():
                    extracted_text += (
                        paragraph.text + "\n"
                    )

        except Exception:
            raise unreadable_file_error()
            print("EXTRACTED TEXT LENGTH:", len(extracted_text))
    print("EXTRACTED TEXT PREVIEW:", repr(extracted_text[:500]))

    if not extracted_text.strip():
        raise empty_resume_error()

    ats_result = analyze_resume(
        extracted_text,
        job_description
    )

    job_match_result = match_job_description(
        extracted_text,
        job_description
    )

    experience_result = analyze_experience(
        extracted_text,
        job_description
    )

    education_result = analyze_education(
        extracted_text,
        job_description
    )

    project_analysis = analyze_projects(
        extracted_text,
        job_description
    )

    print(
        "ANALYTICS: reached analytics section"
    )

    record_resume_analysis(
        ats_score=ats_result.get("ats_score"),
        has_job_description=bool(
            job_description.strip()
        )
    )

    return {
        "filename": file.filename,
        "message": "Resume analyzed successfully",
        "text": extracted_text,
        "characters": len(extracted_text),
        "ats_analysis": ats_result,
        "job_match": job_match_result,
        "experience_analysis": experience_result,
        "education_analysis": education_result,
        "project_analysis": project_analysis
    }


@app.post("/admin/login")
async def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    return login_admin(
        form_data.username,
        form_data.password
    )


@app.get("/admin/analytics")
async def admin_analytics(
    current_admin=Depends(get_current_admin)
):

    return get_admin_analytics()


@app.get("/admin/analytics/daily")
async def admin_daily_analytics(
    current_admin=Depends(get_current_admin)
):

    return get_admin_daily_analytics()


@app.get("/admin/analytics/monthly")
async def admin_monthly_analytics(
    current_admin=Depends(get_current_admin)
):

    return get_admin_monthly_analytics()


@app.get("/admin/analytics/yearly")
async def admin_yearly_analytics(
    current_admin=Depends(get_current_admin)
):

    return get_admin_yearly_analytics()