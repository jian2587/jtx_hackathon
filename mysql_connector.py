import MySQLdb  # install via pip package, MySQL-python


# Simple helper class to connect to MYSQL in python
class SqlManager:

    def __init__(self, hostname, user_name, pwd, db_name):
        self.db = MySQLdb.connect(host=hostname, user=user_name, passwd=pwd, db=db_name)
        self.cursor = self.db.cursor()

    # preps the database if neceessary
    def prepare_db_table_for_insertion(self, table_name):
        q = """CREATE TABLE IF NOT EXISTS %s (
             log_entry TEXT
         )""" % table_name

        self.cursor.execute(q)

    # insert a blob of string into the db
    def insert_text(self, table_name, col_name, text_blob):
        q = """
        INSERT INTO %s (%s) VALUES("%s");
        """ % (table_name, col_name, text_blob)
        self.cursor.execute(q)
        self.db.commit()

    # use this to output queries results
    def query(self, q):
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        while row is not None:
            print ", ".join([str(c) for c in row])
            row = self.cursor.fetchone()

if __name__ == '__main__':
    print 'Connecting to MYSQL test DB'
    table = 'logger1'
    m = SqlManager('localhost', 'root', '', 'test')
    m.prepare_db_table_for_insertion(table)
    m.insert_text(table, 'log_entry', 'xiaowei test')
    m.query('SELECT * FROM logger1')










