import re


class Saver:
    """сохраняет результаты в SQL"""

    def __init__(self, cursor):
        self.cursor = cursor

    def add_item_content_to_sql(self, content):
        _SQL = "SELECT table_name FROM information_schema.tables WHERE table_name = '" + content['table_name']\
               + "' AND table_schema = database();"

        self.cursor.execute(_SQL)
        table_exist = self.cursor.fetchone()
        print(table_exist, _SQL)
        if table_exist:
            _SQL = "INSERT INTO "+content['table_name']+" ("
            for k, v in content.items():
                if k != 'table_name':
                    _SQL += k + ", "
            _SQL = _SQL[0: -2] + ") VALUES ("

            for k, v in content.items():
                if k != 'table_name':
                    _SQL += "'" + v + "', "
            _SQL = _SQL[0: -2] + """);"""
            _SQL = re.sub(r'[^\w\s!?.,;:@#$%^&*№><~`\'\"\[\]()]', "", _SQL)
            print(_SQL)
            try:
                self.cursor.execute(_SQL)
            except Exception as e:
                self.add_log(self, 'False')
                return False, e
        else:

            self.add_log(self, 'table %s is not exist' % content['table_name'])
            return False
        return True

    def add_list_of_links_to_sql(self, home_site_page, list_of_links) -> 'SQL execute':
        """generate SQL request for saving list of links items"""
        _SQL = """INSERT INTO links4parse (home_site_page, curr_link) VALUES """
        for i in range(len(list_of_links) - 1):
            _SQL += """("%s", "%s"), """ % (home_site_page, list_of_links[i])
        i = + 1
        _SQL += """("%s", "%s")""" % (home_site_page, list_of_links[i])
        self.cursor.execute(_SQL)

    def add_log(self,  invoke_attributes, status):
        # time_stump, invoke_class, invoke_method, status
        print(status)
        _SQL = "INSERT INTO tracker (invoke_class, invoke_method, status) VALUES('%s', '%s', '%s')" \
               % (invoke_attributes.__class__.__name__, invoke_attributes.__dir__()[1], status)
        print(invoke_attributes.__dir__())
        self.cursor.execute(_SQL)

# with UseDatabase(cfg.dbconfig) as cursor:
#     _sql = """show tables"""
#     cursor.execute(_sql)
#     data = cursor.fetchall()
#     print(data)

# print(type(my_get))
# s = Saver()
# s.add_item_content_to_sql(my_get)
