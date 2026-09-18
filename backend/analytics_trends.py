from datetime import datetime, timedelta

from sqlmodel import Session, select

from analytics_database import AnalyticsEvent, engine


def get_daily_analytics(days: int = 7):
    with Session(engine) as session:
        events = session.exec(
            select(AnalyticsEvent)
        ).all()

    today = datetime.utcnow().date()

    daily_data = []

    for offset in range(days - 1, -1, -1):
        current_date = today - timedelta(days=offset)

        day_events = [
            event
            for event in events
            if event.event_type == "resume_analyzed"
            and event.created_at.date() == current_date
        ]

        daily_data.append({
            "date": current_date.isoformat(),
            "analyses": len(day_events)
        })

    return daily_data
def get_monthly_analytics():
    with Session(engine) as session:
        events = session.exec(
            select(AnalyticsEvent)
        ).all()

    monthly_data = {}

    for event in events:
        if event.event_type != "resume_analyzed":
            continue

        month_key = event.created_at.strftime("%Y-%m")

        if month_key not in monthly_data:
            monthly_data[month_key] = 0

        monthly_data[month_key] += 1

    return [
        {
            "month": month,
            "analyses": monthly_data[month]
        }
        for month in sorted(monthly_data)
    ]
def get_yearly_analytics():
    with Session(engine) as session:
        events = session.exec(
            select(AnalyticsEvent)
        ).all()

    yearly_data = {}

    for event in events:
        if event.event_type != "resume_analyzed":
            continue

        year_key = event.created_at.strftime("%Y")

        if year_key not in yearly_data:
            yearly_data[year_key] = 0

        yearly_data[year_key] += 1

    return [
        {
            "year": year,
            "analyses": yearly_data[year]
        }
        for year in sorted(yearly_data)
    ]