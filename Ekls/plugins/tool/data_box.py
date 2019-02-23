"""
# 用于数据库查询
"""
import sqlite3


def sql_read(library_name, table_name, field_name="",
             field_key="", field="*", link="=" , in_where=True):  # 读
    """"
    # 用于读取数据库
    # 参数(标*为必填参数)：
    # librar_name   库名*
    # table_name    表名*
    # field_name    条件字段名-限定条件(默认为空)
    # field_key     条件字段值-限定条件(默认为空)
    # field         需返回字段的字段名(默认为返回所有)
    # in_where      是否使用where语句(默认为True)
    # 返回:
    # 返回一个包含元组的列表
    """
    conn = sqlite3.connect(library_name)
    pointer = conn.cursor()
    out = []
    if in_where:  # 是否启用 where 语句

        cursor = pointer.execute("SELECT {} FROM {} WHERE {} {} '{}';".format(
                field, table_name, field_name, link, field_key))
    else:
        cursor = pointer.execute("SELECT {} FROM {} table_name ;"
                                 .format(field, table_name))
    for para in cursor:  # 逐个打包
        out.append(para)
    conn.commit()
    conn.close()
    return out  # 返回结果


def sql_rewrite(library_name, table_name, field_name, field_key, field_name_to,
                field_key_to):  # 改
    """
    # 数据库改写
    # 参数(标*为必填参数)：
    # librar_name     库名*
    # table_name      表名*
    # field_name      条件字段名-限定条件*
    # field_key       条件字段值-限定条件*
    # field_name_to   需修改的字段名*
    # field_key_to    需修改的字段值*
    # 返回:
    # 返回一个改写后的包含元组的列表
    """
    conn = sqlite3.connect(library_name)
    pointer = conn.cursor()

    pointer.execute('UPDATE {} SET {} = "{}" WHERE {} = "{}";'.format(
            table_name, field_name_to, field_key_to, field_name, field_key))
    conn.commit()
    conn.close()
    return sql_read(library_name, table_name, field_name, field_key)  # 返回修改后结果


if __name__ == '__main__':
    i = sql_read("User.db", "User", in_where=False)
    ii = sql_read("User.db", "User", "Name", "A,B=B,A+B", "admin")[0]
    text = "测试1"
    print(i, ii)