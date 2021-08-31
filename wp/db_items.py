from wp import DBTables


class DBItem(object):
    # From Search
    table = ''
    column = ''
    id = int
    value = ''

    # Column of the ID.
    id_column = ''

    @staticmethod
    def new_from_db_table_entry(table, entry):
        item = DBItem()
        item.entry = entry
        item.table = table

        return item

    @staticmethod
    def new_from_db_search_line(line):
        return DBItem.new_from_db_search_item(line.split(":", 3))

    @staticmethod
    def new_from_db_search_item(parts):
        item = DBItem()
        if type(parts) == list and len(parts) == 4:
            item.table = parts[0]
            item.column = parts[1]
            item.id = int(parts[2])
            item.value = parts[3]

        return item


class DBItems(list):
    __all_tables = []
    lines = []
    items = []
    tables = []

    def __init__(self):
        super().__init__()
        self.set_all_tables()

    @staticmethod
    def new_from_search_output(search_output_str):
        items = DBItems()

        items.lines = search_output_str.splitlines()
        for index, line in enumerate(items.lines):
            if line.startswith(tuple(items.__all_tables)):
                item = DBItem.new_from_db_search_line(line)
                items.items.append(item)
            else:
                items.items[-1].value = "\n".join([items.items[-1].value, line])

        return items

    def get_all_items_from_table(self, table):
        return [a for a in self.items if table == a.table]

    def set_all_tables(self):
        if 0 != len(self.__all_tables):
            return self.__all_tables

        tables = DBTables(all_tables=True)
        out, err = tables.run()
        self.__all_tables = tables.tables.get_tables()
