from handlers.BaseHandler import *


class EventImportanceHandler(BaseHandler):

    def post(self):
        content = self.json_args.get("content")
        if content is None:
            return self.write({"code": RET.NODATA, "msg": f"错误类型 : {RESPONSEMAP.get(RET.NODATA)}, 错误详情 : 传入的 content 字段为空"})
        if not isinstance(content, str):
            return self.write({"code": RET.PARAMERR, "msg": f"错误类型 : {RESPONSEMAP.get(RET.PARAMERR)}, 错误详情 : 传入的 content 字段必须为字符串"})

        # todo: specific program execution
        res = {"res": "xxxxx", "content": content}

        self.write(dict(code=RET.OK, msg=RESPONSEMAP.get(RET.OK), data=res))