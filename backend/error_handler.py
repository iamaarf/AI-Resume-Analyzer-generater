from fastapi import HTTPException


def file_error(message):
    return HTTPException(
        status_code=400,
        detail=message
    )


def server_error(message="Something went wrong while analyzing the resume."):
    return HTTPException(
        status_code=500,
        detail=message
    )


def unsupported_file_error():
    return file_error(
        "Only PDF and DOCX files are supported."
    )


def empty_file_error():
    return file_error(
        "The uploaded resume file is empty."
    )


def unreadable_file_error():
    return file_error(
        "The resume file could not be read. Please upload a valid PDF or DOCX file."
    )


def empty_resume_error():
    return file_error(
        "No readable text was found in the resume. Please upload a text-based PDF or DOCX file."
    )