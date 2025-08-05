from apscheduler.schedulers.background import BackgroundScheduler
from ..database import get_db
from ..crud.crud import reset_kudos_weekly


def start_scheduler():
    scheduler = BackgroundScheduler()
    @scheduler.scheduled_job("cron", day_of_week="mon", hour=0)
    def weekly_reset():
        with next(get_db()) as session:
            reset_kudos_weekly(session)

    scheduler.start()
