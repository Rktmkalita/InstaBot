from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pytz
import random
import datetime
import json
from bot import run_bot


class BotScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.job = None
        self.logs = []
        self.load_config()

    def log(self, message):
        timestamp = datetime.datetime.now().isoformat()
        self.logs.append(f"[{timestamp}] {message}")
        self.logs = self.logs[-100:]  # Keep last 100 logs

    def load_config(self):
        try:
            with open("config.json") as f:
                self.config = json.load(f)
        except:
            self.config = {
                "category": "animememes",
                "max_posts": 10,
                "timezone": "Asia/Kolkata",
                "sleep_hours": ["01:00", "09:00"],
                "upload_interval": [30, 120]
            }

    def reload_config(self, new_config):
        self.config = new_config
        self.stop()
        self.start()

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()

        if not self.job:
            self.schedule_next_run()
            self.log("Scheduler started")

    def stop(self):
        if self.job:
            self.job.remove()
            self.job = None
            self.log("Scheduler stopped")

    def run_now(self):
        self.run_task()

    def run_task(self):
        tz = pytz.timezone(self.config.get("timezone", "Asia/Kolkata"))
        now = datetime.datetime.now(tz).time()
        sleep_start = datetime.datetime.strptime(self.config["sleep_hours"][0], "%H:%M").time()
        sleep_end = datetime.datetime.strptime(self.config["sleep_hours"][1], "%H:%M").time()

        if sleep_start < sleep_end:
            in_sleep = sleep_start <= now <= sleep_end
        else:  # cross-midnight case
            in_sleep = now >= sleep_start or now <= sleep_end

        if not in_sleep:
            try:
                self.log("Running bot task")
                run_bot(self.config)
            except Exception as e:
                self.log(f"Error during bot task: {e}")
        else:
            self.log("Skipped run due to sleep window")

        self.schedule_next_run()

    def schedule_next_run(self):
        delay_minutes = random.randint(*self.config.get("upload_interval", [30, 120]))
        if self.job:
            self.job.remove()

        self.job = self.scheduler.add_job(self.run_task, trigger=IntervalTrigger(minutes=delay_minutes))
        self.log(f"Next run scheduled in {delay_minutes} minutes")

    def get_status(self):
        return {
            "running": self.scheduler.running,
            "next_run_time": str(self.job.next_run_time) if self.job else "Not scheduled"
        }

    def get_logs(self):
        return self.logs

bot_scheduler = BotScheduler()
