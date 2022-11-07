from celery import Celery
from config import celery_config
from utils.logger import logger


app = Celery("celery_tasks")
app.config_from_object(celery_config)


@app.task(name="celery_tasks.get_test_info")
def get_test_info(content):
    logger.info(f"celery task form : {content}")
    return {"res": content}


if __name__ == '__main__':
    app.start(argv=['celery', '-A', 'celery_tasks', 'worker', '--loglevel', 'info'])
    # app.start(argv=['celery', '-A', 'celery_tasks', 'worker', '--loglevel', 'info', '--logfile', 'logs/info.log'])
