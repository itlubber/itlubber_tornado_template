import tornado.log
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import config
import logging
from utils.logger import logger
from utils.urls import urls
from tornado.options import options
from crontab import scheduler


tornado.options.define("port", default=config.port, type=int, help="run server on the given port")


def main():
    tornado.log.access_log.propagate = False
    tornado.options.options.log_file_prefix = config.log_file
    tornado.options.options.logging = config.log_level
    tornado.options.options.log_rotate_mode = "time"
    tornado.options.options.log_rotate_when = "D"
    tornado.options.options.log_rotate_interval = 30
    tornado.options.options.log_file_num_backups = 10
    tornado.options.options.log_to_stderr = True
    formatter = tornado.log.LogFormatter(fmt=config.log_format, datefmt=config.log_date_format, color=True)
    tornado.options.parse_command_line()
    [i.setFormatter(formatter) for i in logging.getLogger().handlers]

    app = tornado.web.Application(urls, **config.settings)

    logger.debug(f"tornado httpserver runing, interface address is http://127.0.0.1:{config.port}/")
    http_server = tornado.httpserver.HTTPServer(app)

    http_server.listen(options.port)

    # http_server.bind(options.port)
    # http_server.start(config.max_workers)

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    scheduler.start()
    main()
