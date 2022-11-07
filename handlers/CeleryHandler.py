from handlers.BaseHandler import *
from celery.result import AsyncResult
from celery_tasks import get_test_info


class CeleryTasksTest(BaseHandler):

    def post(self):
        content = self.json_args.get("content", "")
        response = get_test_info.delay(content)
        self.write(dict(code=RET.OK, msg="OK", data={"task_id": response.id}))

    def get(self, task_id):
        response = AsyncResult(task_id)
        if response.ready():
            self.write(dict(code=RET.OK, msg=RESPONSEMAP.get(RET.OK, "UNKNOWN"),
                            data={"task_id": task_id, "response": response.get()}))
        else:
            self.write(dict(code=RET.RUNING, msg=RESPONSEMAP.get(RET.RUNING, "UNKNOWN"),
                            data={"task_id": task_id, "response": None}))