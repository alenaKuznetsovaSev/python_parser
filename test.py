import config as cfg
from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
import Log

logger = Log.get_logger('test')
sql = "INSERT INTO proxies (proxy, type, replace_ip, speed, check_count, success_checks, alive) VALUES ('216.45.60.108:58780', 'SOCKS5', 1, 14, 29, 10, 1);"
with UseDatabase(cfg.dbconfig) as cursor:
    try:
        cursor.execute(sql)
    except Exception as ex:
        logger.warn("%s" % ex)
