from DBcm import UseDatabase
from Saver import Saver
from Proxy_manager import ProxyManager
import config as cfg
from tastemade_com_food import Tastemade_com_food

my_get = {'table_name': 'food_recipe', 'title': 'Васильев'}

if __name__ == '__main__':
    with UseDatabase(cfg.dbconfig) as cursor:
        saver = Saver(cursor)
        proxy_manager = ProxyManager()
        current_parser = Tastemade_com_food('https://www.tastemade.com/food', saver, proxy_manager)
        saver.add_item_content_to_sql(current_parser.parse_item_page('https://www.tastemade.com/videos/spring-rolls-with-sakura-petals'))
