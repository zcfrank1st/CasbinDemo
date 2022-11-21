from apscheduler.schedulers.background import BackgroundScheduler

class SyncPolicy:
    def __init__(self, fun, seconds=5) -> None:
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(fun, trigger='interval', seconds=seconds)
    
    def start(self):
        self.scheduler.start()
    