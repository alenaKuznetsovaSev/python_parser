import logging
import Log

toto_logger = logging.getLogger("toto")
assert toto_logger.level == logging.NOTSET # новый диспетчер имеет уровень NOTSET
assert toto_logger.getEffectiveLevel() == logging.WARN # и его эффективный уровень равен уровню корневого диспетчера, то есть WARN

# прикрепляем консольный обработчик к диспетчеру «toto»
console_handler = logging.StreamHandler()
toto_logger.addHandler(console_handler)
toto_logger.debug("debug") # ничего не выводится, т. к. уровень логов, DEBUG, ниже, чем эффективный уровень «toto»
toto_logger.setLevel(logging.DEBUG)
toto_logger.debug("debug message") # теперь вы можете увидеть на экране «debug message»

my_log = Log.get_logger('my_test_logger')
my_log.addHandler(Log.get_console_handler())
my_log.setLevel(logging.DEBUG)
my_log.info('test msg from my_log')