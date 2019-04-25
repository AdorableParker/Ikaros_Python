from plugins.tool.date_box import sql_rewrite, sql_read, sql_write


def string_cover(from_string, to_string):
    from_string = str(from_string)
    from_string = from_string.replace(from_string[2:-2], to_string*len(from_string[2:-2]))
    return from_string


async def change_everything(session, field):
    """
    # 功能            字段名
    #------------------------
    # 复读姬          repeat
    # 开火权限        fire
    # 火星时报        Sara_news
    # 标枪快讯        Javelin_news
    # 报时           Call_bell
    # 报时_舰C       Call_bell_AZ
    """
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        if stripped_arg.startswith("#"):
            intent = sql_read("User.db", "group_info", "id", stripped_arg.lstrip("#"), field = field, in_where = True)[0][0]
            sql_rewrite("User.db", "group_info", "id", stripped_arg.lstrip("#"), field, int(not intent))
            echo = sql_read("User.db", "group_info", "id", stripped_arg.lstrip("#"), field = field, in_where = True)[0][0]
            return not not intent, not not echo
        else:
            group_id = stripped_arg
    else:
        group_id = session.ctx["group_id"]
    intent = sql_read("User.db", "group_info", "group_id", group_id, field = field, in_where = True)[0][0]
    sql_rewrite("User.db", "group_info", "group_id", session.ctx["group_id"], field, int(not intent))
    echo = sql_read("User.db", "group_info", "group_id", group_id, field = field, in_where = True)[0][0]

    return not not intent, not not echo