from analytics_database import (
    AnalyticsEvent,
    engine,
    create_database,
    get_analytics_summary
)

from analytics_trends import (
    get_daily_analytics,
    get_monthly_analytics,
    get_yearly_analytics
)

from sqlmodel import Session


def record_resume_analysis(
    ats_score: int | None,
    has_job_description: bool
):
    create_database()

    with Session(engine) as session:
        event = AnalyticsEvent(
            event_type="resume_analyzed",
            ats_score=ats_score,
            has_job_description=has_job_description
        )

        session.add(event)
        session.commit()
        session.refresh(event)

        return event.id


def get_admin_analytics():
    return get_analytics_summary()


def get_admin_daily_analytics():
    return get_daily_analytics()
def get_admin_daily_analytics():
    return get_daily_analytics()
def get_admin_monthly_analytics():
    return get_monthly_analytics()


def get_admin_yearly_analytics():
    return get_yearly_analytics()