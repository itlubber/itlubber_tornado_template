## 模型接口服务实现

> postman接口在线文档 : http://127.0.0.1

### 项目结构
```bash
tornado_template-main
├── readme.md                           项目说明文件
├── server.py                           服务启动入口文件
├── config.py                           项目配置文件
├── crontab.py                          定时任务配置文件
├── clear_cache.sh                      清理缓存文件 __pycache__ & ipynb_checkpoints
├── docker                              docker相关文件
│   ├── Dockerfile                          - 打包文件
│   ├── build.sh                            - 执行打包的脚本
│   ├── requirements.txt                    - python 相关依赖
│   ├── install_packages.sh                 - 安装 python 依赖环境的脚本
│   └── run.sh                              - docker启动脚本
├── handlers                            接口服务文件夹
│   ├── BaseHandler.py                      - 接口的基类，所有接口类类继承该类
│   └── EventImportance.py                  - api测试样例
├── models                              数据库相关文件存放位置
│   ├── conn_db.py                          - 数据库连接池实现
│   └── features_extraction.py              - 数据库相关操作
├── utils                               tornado相关的公共方法
│   ├── constants.py                        - 常量配置（过期时间等）
│   ├── logger.py                           - 全局日志模块
│   ├── methods.py                          - 公共方法（函数执行计时器）
│   ├── response_code.py                    - 统一定义好的异常状态码及错误类型
│   └── urls.py                             - 路由配置入口文件
└── static                              静态文件存储位置（主页）
    ├── favicon.ico
    ├── index.html
    └── style.css
```


### 相关命令
```bash
# docker 相关文件中注意修改文件夹位置
# ----------------------------------------------------------------------------------
# python 主程序的启动方式
python main.py
# 加载 docker image
docker load < itlubber.risk_warnings.tar
# 可以重新打包 docker image
docker build -t itlubber/risk_warnings:v1 .
# 运行 docker
./run.sh
# docker 内部程序调试方法
docker exec -it YOUR_DOCKER_CONTAINER_ID /bin/bash
# docker-compose 方式启动
docker-compose up  -d
# 查看 docker 日志信息
docker logs -f YOUR_DOCKER_CONTAINER_ID
```


### tornado log 自定义

```python
import logging
import tornado
from tornado.log import access_log, gen_log, app_log, LogFormatter
access_log.propagate = False
datefmt = '%Y-%m-%d %H:%M:%S'
fmt = '%(color)s[%(levelname) %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
formatter = LogFormatter(color=True, datefmt=datefmt, fmt=fmt)
logHandler = logging.StreamHandler()
access_log.addHandler(logHandler)
tornado.options.parse_command_line()
[i.setFormatter(formatter) for i in logging.getLogger().handlers]
```
> 原理：tornado.options.parse_command_line()会自动调用enable_pretty_logging方法，该方法默认会创建一个root logger，因为父子关系的存在，tornado所有其他logger事件都会触发root logger，所以修改root logger的格式就能修改tornado所有日志的格式。

> 原理：tornado本身有三种类型的日志流:access_log, gen_log, app_log。为这些logger添加自定义的handler即可，注意access_log.propagate = False这段代码必不可少，要不然会触发默认的根logger导致重复日志