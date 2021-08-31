from wp.command import WPCommand


class DBQuery(WPCommand):
    command = ['db', 'query']

    # SQL.
    sql = ''  # Required

    # Skips outputting column names.
    skip_column_names = bool

    def __init__(self, sql, **args):
        super().__init__(**args)
        self.sql = sql

        self.skip_column_names = self.get_arg_value(key="skip_column_names", default_value=self.skip_column_names)

    def params(self):
        return [
            self.sql
            # f"\"{self.sql}\""
        ]

    def get_excluded_attrs(self):
        return [
            "sql"
        ]

    @staticmethod
    def escape(str):
        return str.translate(
            str.maketrans({
                "\0": "\\0",
                "\r": "\\r",
                "\x08": "\\b",
                "\x09": "\\t",
                "\x1a": "\\z",
                "\n": "\\n",
                "\r": "\\r",
                "\"": "\\\"",
                "'": "\\'",
                "\\": "\\\\",
                "%": "\\%"
            }))
