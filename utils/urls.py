import os
from tornado.web import StaticFileHandler, url
from handlers.EventImportance import EventImportanceHandler
from handlers.CeleryHandler import CeleryTasksTest


urls = [
    url(r"/event_importance", EventImportanceHandler, name="event_importance"),
    url(r"/celery_tasks_test", CeleryTasksTest, name="celery_tasks_test"),
    url(r"/celery_tasks_test/(?P<task_id>.+)", CeleryTasksTest, name="celery_tasks_test_response"),

    (r"/(.*)", StaticFileHandler,
     dict(path=os.path.join(os.path.dirname(__file__), "static"), default_filename="index.html"))
]