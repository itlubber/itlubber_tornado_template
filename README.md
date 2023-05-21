## ITLubber、酱的WEB应用初始化框架


本仓库集成tornado、celery、apscheduler、pymysql等框架，简单实用。

> 微信公众号: [`酱菜坛子鹿宝宝`](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI2ODUwOTc5Mw==&action=getalbum&album_id=2560621199173730305&subscene=231&scenenote=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI2ODUwOTc5Mw%3D%3D%26mid%3D2247484178%26idx%3D1%26sn%3D3d994200042d12ebaa96f7b7714b9927%26chksm%3Deaef341cdd98bd0ad5efb37bc35bae8119e7933c83befb730ffee660a04e668274960c2a9f91%26scene%3D231%26subscene%3D0%26sessionid%3D1667812106%26clicktime%3D1667812124%26enterid%3D1667812124%26ascene%3D3%26fasttmpl_type%3D0%26fasttmpl_fullversion%3D6408308-zh_CN-zip%26fasttmpl_flag%3D0%26realreporttime%3D1667812125005%26devicetype%3Dandroid-30%26version%3D28001c57%26nettype%3D3gnet%26abtest_cookie%3DAAACAA%253D%253D%26lang%3Dzh_CN%26session_us%3Dgh_6cc40b0dcccc%26exportkey%3Dn_ChQIAhIQ6ISiL79eOOx4bND9EPccjxLrAQIE97dBBAEAAAAAAGo5Iny5qioAAAAOpnltbLcz9gKNyK89dVj0%252FxTnz7J1PklnWGwNEEXlYJWOLuG5%252BGZeF69%252F8hQXae8%252FpsjtCi4aLuDCumUuIjXpatcTnFFh5UEMkpjjuWMR6XZ4eNyOg89smCL1RUo4pFBVxRpjM3FXje79QgTckDpRM%252BEw7pipsiRkKDUrJQIiJ%252BCX0j4sxKE%252FZkkqdkrdrHkubtRCdzpW7t71Ug4gruylm0lmPjS6fEA7Rr2S2FpD136NRrmYagcW2jzh4DX7BSKrvPhYf9gtoLb50ejyHMZuD2yNzk4%253D%26pass_ticket%3DZSvCswxA3Xit%252Bu1c329HeQRoYANYXU4AkEFCicXc9prWMx8pfb6%252FgEesHTfYGj6z%26wx_header%3D3&nolastread=1#wechat_redirect)
> 
> 个人博客: [`https://itlubber.art/`](https://itlubber.art/)

### 交流

<table style="text-align:center !important;border=0;">
    <tr>
        <td>
            <span>微信: itlubber</span>
        </td>
        <td>
            <span>微信公众号: itlubber_art</span>
        </td>
    </tr>
    <tr>
        <td>
            <img src="https://itlubber.art//upload/itlubber.png" alt="itlubber.png" width="50%" border=0/>
        </td>
        <td>
            <img src="https://itlubber.art//upload/itlubber_art.png" alt="itlubber_art.png" width="50%" border=0/>
        </td>
    </tr>
</table>


### 在线API文档管理


> 在线API文档 : https://www.apifox.cn/apidoc/shared-fe7aebf8-8c1b-4704-8a55-830afac0ce3e


### 项目结构


```bash
tree

.
├── LICENSE                                     # MIT LICENSE
├── README.md                                   # 使用说明文档
├── server.py                                   # 服务启动脚本
├── config.py                                   # 相关配置文件
├── celery_tasks.py                             # celery 异步任务启动脚本
├── crontab.py                                  # 定时任务配置文件
├── clear_cache.sh                              # 清除缓存文件脚本
├── dbutils                                     # 数据库连接池
│   ├── __init__.py
│   ├── hive_connect_pool.py                    # impala & hive 数据库连接池
│   ├── mysql_connect_pool.py                   # mysql 数据库连接池
│   ├── persistent_db.py
│   ├── pooled_db.py
│   └── steady_db.py
├── docker                                      # docker 部署相关文件
│   ├── Dockerfile                              # docker 构建文件
│   ├── build.sh                                # docker build 脚本
│   ├── install_packages.sh                     # 安装依赖包脚本
│   ├── packages                                # 依赖文件
│   │   └── tornado-celery-0.3.5.tar.gz
│   ├── requirements.txt                        # python 依赖
│   └── run.sh                                  # docker 启动脚本
├── handlers                                    # 接口具体逻辑
│   ├── BaseHandler.py                          # 接口的基类，所有接口类类继承该类
│   ├── CeleryHandler.py                        # 异步任务相关接口实现
│   ├── EventImportance.py                      # 普通任务相关接口实现
│   └── __init__.py
├── logs                                        # 日志文件
│   └── info.log
├── models                                      # 数据库相关操作和其他模型相关的脚本
│   ├── __init__.py
│   ├── conn_db.py                              # 数据库连接池实例化
│   └── features_extraction.py                  # 具体任务逻辑
├── static                                      # 静态文件，访问 / 时返回网页
│   ├── favicon.ico
│   ├── index.html
│   └── style.css
└── utils                                       # 公共方法
    ├── __init__.py
    ├── logger.py                               # 日志
    ├── methods.py                              # 公用方法
    ├── response_code.py                        # 返回状态码
    └── urls.py                                 # 路由配置

8 directories, 35 files
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


### python 离线裸机部署


```bash
# 原生方法
pip freeze > requirements.txt
# 优化方法
# 安装依赖
pip install pipreqs
# 在当前目录生成
pipreqs . --encoding=utf8 --force
# 在当前环境下安装依赖
 pip install -r requirements.txt
# 下载当前依赖环境的离线包
pip download -d python_lib/ -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
# 离线安装依赖包 python_lib 为离线包文件的位置
pip install --no-index --find-links=python_lib -r requirements.txt
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