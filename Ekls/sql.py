import sqlite3

class database:
    def __init__(self, name):
        self.conn = sqlite3.connect(name+".db")
        self.curs = self.conn.cursor()

    def create_table(self, table_name):
        self.curs.execute("CREATE TABLE {}( 'ID' INTEGER PRIMARY KEY AUTOINCREMENT);".format(table_name))

        self.conn.commit()  # 提交事务


    def insert_field(self, table_name, field_name, datatpye, keys=False, auto_increment=False, unique=False, default=False):
        instruction = 'ALTER TABLE {} ADD COLUMN {} {}'.format(table_name, field_name, datatpye)
        if auto_increment:
            instruction += " PRIMARY KEY AUTOINCREMENT"
        elif keys:
            instruction += " PRIMARY KEY"
        if unique:
            instruction += " UNIQUE"
        if default:
            instruction += " DEFAULT {};".format(default)
        self.curs.execute(instruction)
        self.conn.commit()


    def insert_into(self, table_name, **info):
        instruction = "INSERT INTO {}".format(table_name)
        keys, value = [], []
        for i in info:
            keys.append(i)
            value.append(info[i])
        instruction +=  "{} VALUES {};".format(tuple(keys), tuple(value))
        self.curs.execute(instruction)
        self.conn.commit()


    def select(self, table_name, output_field='*', condition=False):
        if condition:
            instruction = 'SELECT {} FROM {} WHERE {};'.format(", ".join(output_field), table_name, condition)
        else:
            instruction = 'SELECT {} FROM {};'.format(", ".join(output_field), table_name)
        outinfo = self.curs.execute(instruction)
        self.conn.commit()
        return outinfo


    def updata(self, table_name, condition, **info):
        instruction = "UPDATE {} SET".format(table_name)
        for i in info:
            instruction +=  " {} = {}".format(i, info[i])
        instruction += " WHERE {};".format(condition)
        print(instruction)
        self.curs.execute(instruction)
        self.conn.commit()


    def close_database(self):
        self.conn.close()  # 关闭连接