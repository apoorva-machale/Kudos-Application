from apscheduler.schedulers.background import BackgroundScheduler
from database import get_db
from crud.crud import reset_kudos_weekly


def start_scheduler():
    # Create a background scheduler instance
    scheduler = BackgroundScheduler()
    # Define a scheduled job to run weekly at Monday midnight (00:00)
    @scheduler.scheduled_job("cron", day_of_week="mon", hour=0)
    def weekly_reset():
        # Get a database session and call the kudos reset function
        with next(get_db()) as session:
            reset_kudos_weekly(session)
    # Start the scheduler in the background
    scheduler.start()
