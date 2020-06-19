from db_classes.database_connector import UseDatabase
from db_classes.saver import Saver
from proxy_manager import ProxyManager
import config as cfg
from parsers.tastemade_com import Tastemade_com_food
import log

if __name__ == '__main__':
    main_logger = log.get_logger(__name__)
    main_logger.info('program started')
    with UseDatabase(cfg.dbconfig) as cursor:
        saver = Saver(cursor)
        proxy_manager = ProxyManager()
        current_parser = Tastemade_com_food('https://www.tastemade.com/food')
        saver.add_item_content_to_sql(current_parser.parse_item_page('https://www.tastemade.com/videos/spring-rolls-with-sakura-petals'))
    main_logger.info('program finished')
