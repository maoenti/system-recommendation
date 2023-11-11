from importlib.metadata import version

flask_major_version = int(version("flask")[0])

import MySQLdb
from MySQLdb import cursors
from flask import current_app

if flask_major_version >= 2:
    from flask import g

    ctx = g
else:
    from flask import _app_ctx_stack

    ctx = _app_ctx_stack.top


class MySQL:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the `app` for use with this
        :class:`~flask_mysqldb.MySQL` class.
        This is called automatically if `app` is passed to
        :meth:`~MySQL.__init__`.

        :param flask.Flask app: the application to configure for use with
            this :class:`~flask_mysqldb.MySQL` class.
        """

        app.config.setdefault("MYSQL_HOST", "localhost")
        app.config.setdefault("MYSQL_USER", "root")
        app.config.setdefault("MYSQL_PASSWORD", None)
        app.config.setdefault("MYSQL_DB", "test_flask")
        app.config.setdefault("MYSQL_PORT", 3306)

        # set socket to xampp
        # app.config.setdefault("MYSQL_HOST", "localhost")
        # app.config.setdefault('MYSQL_UNIX_SOCKET', '/opt/lampp/var/mysql/mysql.sock')

        # app.config.setdefault("MYSQL_UNIX_SOCKET", None)
        # app.config.setdefault("MYSQL_CONNECT_TIMEOUT", 10)
        # app.config.setdefault("MYSQL_READ_DEFAULT_FILE", None)
        # app.config.setdefault("MYSQL_USE_UNICODE", True)
        # app.config.setdefault("MYSQL_CHARSET", "utf8")
        # app.config.setdefault("MYSQL_SQL_MODE", None)
        # app.config.setdefault("MYSQL_CURSORCLASS", None)
        # app.config.setdefault("MYSQL_AUTOCOMMIT", False)
        # app.config.setdefault("MYSQL_CUSTOM_OPTIONS", None)

        if hasattr(app, "teardown_appcontext"):
            app.teardown_appcontext(self.teardown)

    @property
    def connect(self):
        kwargs = {}

        if current_app.config["MYSQL_HOST"]:
            kwargs["host"] = "localhost"

        if current_app.config["MYSQL_USER"]:
            kwargs["user"] = "root"

        if current_app.config["MYSQL_PASSWORD"]:
            kwargs["passwd"] = ""

        if current_app.config["MYSQL_DB"]:
            kwargs["db"] = "test_flask"

        if current_app.config["MYSQL_PORT"]:
            kwargs["port"] = 3306

        # if current_app.config["MYSQL_UNIX_SOCKET"]:
        #     kwargs["unix_socket"] = current_app.config["MYSQL_UNIX_SOCKET"]

        # if current_app.config["MYSQL_CONNECT_TIMEOUT"]:
        #     kwargs["connect_timeout"] = current_app.config["MYSQL_CONNECT_TIMEOUT"]

        # if current_app.config["MYSQL_READ_DEFAULT_FILE"]:
        #     kwargs["read_default_file"] = current_app.config["MYSQL_READ_DEFAULT_FILE"]

        # if current_app.config["MYSQL_USE_UNICODE"]:
        #     kwargs["use_unicode"] = current_app.config["MYSQL_USE_UNICODE"]

        # if current_app.config["MYSQL_CHARSET"]:
        #     kwargs["charset"] = current_app.config["MYSQL_CHARSET"]

        # if current_app.config["MYSQL_SQL_MODE"]:
        #     kwargs["sql_mode"] = current_app.config["MYSQL_SQL_MODE"]

        # if current_app.config["MYSQL_CURSORCLASS"]:
        #     kwargs["cursorclass"] = getattr(
        #         cursors, current_app.config["MYSQL_CURSORCLASS"]
        #     )

        # if current_app.config["MYSQL_AUTOCOMMIT"]:
        #     kwargs["autocommit"] = current_app.config["MYSQL_AUTOCOMMIT"]

        # if current_app.config["MYSQL_CUSTOM_OPTIONS"]:
        #     kwargs.update(current_app.config["MYSQL_CUSTOM_OPTIONS"])

        return MySQLdb.connect(**kwargs)

    @property
    def connection(self):
        """Attempts to connect to the MySQL server.

        :return: Bound MySQL connection object if successful or ``None`` if
            unsuccessful.
        """

        if ctx is not None:
            if not hasattr(ctx, "mysql_db"):
                ctx.mysql_db = self.connect
            return ctx.mysql_db

    def teardown(self, exception):
        if hasattr(ctx, "mysql_db"):
            ctx.mysql_db.close()