import json
from wp.command import WPCommand


class Column(object):
    field = ''
    type = ''
    null = bool
    key = ''
    default = ''
    extra = ''

    @staticmethod
    def new_from_dict(d):
        if type(d) != dict:
            raise TypeError("column needs to be a dictionary")

        column = Column()
        column.field = d['Field']
        column.type = d['Type']
        column.null = bool(d['Null'].lower())
        column.key = d['Key']
        column.default = d['Default']
        column.extra = d['Extra']

        return column

    @staticmethod
    def new_from_list(l):
        if type(l) != list and 6 > len(l):
            raise TypeError("column needs to be a list of 6 elements")

        column = Column()
        column.field = l[0]
        column.type = l[1]
        column.null = bool(l[2].lower())
        column.key = l[3]
        column.default = l[4]
        column.extra = l[5]

        return column


class Columns(object):
    columns = {}

    def __init__(self, cmd_output, format="plain"):
        if '' != cmd_output and cmd_output is not None:
            if "json" == format:
                columns = json.loads(cmd_output)
                for column in columns:
                    self.columns[column['Field']] = Column.new_from_dict(column)
            else:
                rows = cmd_output.split("\n")

                # Remove header row
                if rows[0].startswith("Field"):
                    rows.pop(0)

                for row in rows:
                    data = row.split("\t")
                    self.columns[data[0]] = Column.new_from_list(data)
                print(cmd_output)
        else:
            raise TypeError("cmd_output should not be an empty string or None.")

    def __getitem__(self, item):
        return self.columns[item]

    def __len__(self):
        return len(self.columns)

    def get_columns(self):
        return self.columns


class DBColumns(WPCommand):
    command = ['db', 'columns']

    # Render output in a particular format.
    # default: var_export
    # options: var_export, json, yaml
    format = ''

    columns = Columns

    def __init__(self, table, **args):
        super().__init__(**args)
        self.table = table

        self.format = self.get_arg_value(key="format", default_value=self.format)

    def params(self):
        return [
            self.table
        ]

    def get_excluded_attrs(self):
        return [
            "table",
            "columns",
        ]

    def run(self):
        out, err = super().run()
        if "" != out:
            self.columns = Columns(out)
        return out, err
