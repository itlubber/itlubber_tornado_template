from apscheduler.schedulers.tornado import TornadoScheduler
from models.features_extraction import test_func


scheduler = TornadoScheduler()


scheduler.add_job(test_func, "interval", seconds=60, id="test")