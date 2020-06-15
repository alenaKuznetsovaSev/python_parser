import re
import Log
import csv


class Saver:
    """сохраняет результаты в SQL"""

    def __init__(self, cursor):
        self.logger = Log.get_logger(__name__)
        self.logger.debug('Saver was created')
        self.cursor = cursor

    def add_item_content_to_sql(self, content):
        _SQL = "SELECT table_name FROM information_schema.tables WHERE table_name = '" + content['table_name']\
               + "' AND table_schema = database();"

        self.cursor.execute(_SQL)
        table_exist = self.cursor.fetchone()

        if table_exist:
            # self.logger.debug("table %s exist " % content['table_name'])
            _SQL = "INSERT INTO "+content['table_name']+" ("
            for k, v in content.items():
                if k != 'table_name':
                    _SQL += k + ", "
            _SQL = _SQL[0: -2] + ") VALUES ("

            for k, v in content.items():
                if k != 'table_name':
                    if type(v) == type(''):
                        _SQL += "'" + v + "', "
                    else:
                        _SQL += str(v) + ", "
            _SQL = _SQL[0: -2] + """);"""
            _SQL = re.sub(r'[^\w\s!?.,;:@#$%^&*№><~`\'\"\[\]()]', "", _SQL)
            try:
                self.cursor.execute(_SQL)
            except Exception as e:
                self.logger.warn("we couldn`t insert into %s this SQL - %s, have this error : %s " % (content['table_name'], _SQL, e))
                # self.logger.error('error msg', e)
                return False, e
        else:
            self.logger.warn("table %s does not exist " % content['table_name'])
            return False
        return True

    def add_list_of_links_to_sql(self, home_site_page, list_of_links) -> 'SQL execute':
        """generate SQL request for saving list of links items"""
        _SQL = """INSERT INTO links4parse (home_site_page, curr_link) VALUES """
        for i in range(len(list_of_links) - 1):
            _SQL += """("%s", "%s"), """ % (home_site_page, list_of_links[i])
        i = + 1
        _SQL += """("%s", "%s")""" % (home_site_page, list_of_links[i])
        try:
            self.cursor.execute(_SQL)
        except Exception as e:
            self.logger.error("we couldn`t insert into links4parse this SQL - %s " % _SQL)
            self.logger.error('error msg', e)

    def write_row_in_file(self, file_name="database.csv", data=""):
        """функция для дописывания строки в файл"""
        with open(file_name, "a") as file:
            row = ""
            for i in data:
                row += "%s, " % i
            file.write(row[:-2] + "\n")
            file.close()

    def read_file(self, file_name="random_text.csv"):
        """функция для чтения из файла
        file_name - имя файла
        возвращает массив строк"""
        text = []
        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                text += row
        return text

    # % (invoke_attributes.__class__.__name__, invoke_attributes.__dir__()[1], status)

# with UseDatabase(cfg.dbconfig) as cursor:
#     _sql = """show tables"""
#     cursor.execute(_sql)
#     data = cursor.fetchall()
#     main_logger.debug(data)

# main_logger.debug(type(my_get))
# s = Saver()
# s.add_item_content_to_sql(my_get)
