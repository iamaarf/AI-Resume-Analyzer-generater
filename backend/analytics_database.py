from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import datetime
from typing import Optional


class AnalyticsEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    event_type: str
    ats_score: Optional[int] = None
    has_job_description: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


sqlite_file_name = "resume_analytics.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(
    sqlite_url,
    echo=False
)


def create_database():
    SQLModel.metadata.create_all(engine)


def test_analytics_event():
    with Session(engine) as session:
        event = AnalyticsEvent(
            event_type="test_event",
            ats_score=75,
            has_job_description=True
        )

        session.add(event)
        session.commit()
        session.refresh(event)

        print("Test event saved successfully!")
        print("Event ID:", event.id)


def read_analytics_events():
    with Session(engine) as session:
        events = session.exec(
            select(AnalyticsEvent)
        ).all()

        for event in events:
            print(
                "ID:",
                event.id,
                "| Event:",
                event.event_type,
                "| ATS:",
                event.ats_score,
                "| JD:",
                event.has_job_description
            )


def get_analytics_summary():
    with Session(engine) as session:
        events = session.exec(
            select(AnalyticsEvent)
        ).all()

        resume_events = [
            event
            for event in events
            if event.event_type == "resume_analyzed"
        ]

        total_analyses = len(resume_events)

        ats_scores = [
            event.ats_score
            for event in resume_events
            if event.ats_score is not None
        ]

        if ats_scores:
            average_ats_score = round(
                sum(ats_scores) / len(ats_scores)
            )
        else:
            average_ats_score = 0

        jd_used = sum(
            1
            for event in resume_events
            if event.has_job_description
        )

        return {
            "total_analyses": total_analyses,
            "average_ats_score": average_ats_score,
            "job_description_used": jd_used,
            "job_description_not_used": total_analyses - jd_used
        }


if __name__ == "__main__":
    create_database()
    test_analytics_event()