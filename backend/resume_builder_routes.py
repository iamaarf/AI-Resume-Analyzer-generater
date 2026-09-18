from fastapi import APIRouter, HTTPException

from resume_builder_engine import build_resume


router = APIRouter()


@router.post("/build-resume")
async def build_resume_endpoint(
    resume_data: dict
):

    try:

        if not isinstance(
            resume_data,
            dict
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid resume data."
            )

        result = build_resume(
            resume_data
        )

        return {
            "success": True,
            "message": "Resume generated successfully.",
            "resume": result
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            "Resume Builder Error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to generate resume."
        )