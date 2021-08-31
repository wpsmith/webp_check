from wp.command import WPCommand


class Tables(object):
    tables = []

    def __init__(self, cmd_output, format="list"):
        if "csv" == format:
            self.tables = cmd_output.split(",")
        else:
            self.tables = cmd_output.split("\n")

    def has_table(self, table):
        return table in self.tables

    def get_tables(self):
        return self.tables


class DBTables(WPCommand):
    command = ['db', 'tables']

    # List tables based on wildcard search, e.g. ‘wp_*_options’ or ‘wp_post?’.
    table = ''

    # Can be all, global, ms_global, blog, or old tables. Defaults to all.
    scope = ''
    __scope_enum = [
        'all',
        'global',
        'ms_global',
        'blog',
        'old',
    ]

    # List all the tables in a multisite install.
    network = bool

    # List all tables that match the table prefix even if not registered on $wpdb. Overrides –network.
    all_tables_with_prefix = bool

    # List all tables in the database, regardless of the prefix, and even if not registered on $wpdb.
    # Overrides –all-tables-with-prefix.
    all_tables = bool

    # Render output in a particular format.
    # default: list
    # options: list, csv
    format = ''

    # Tables from the command.
    tables = Tables

    def __init__(self, **args):
        super().__init__(**args)

        self.table = self.get_arg_value(key="table", default_value=self.table)
        self.scope = self.get_arg_value(key="scope", default_value=self.scope)
        self.network = self.get_arg_value(key="network", default_value=self.network)
        self.all_tables_with_prefix = self.get_arg_value(key="all_tables_with_prefix",
                                                         default_value=self.all_tables_with_prefix)
        self.all_tables = self.get_arg_value(key="all_tables", default_value=self.all_tables)
        self.format = self.get_arg_value(key="format", default_value=self.format)

    def params(self):
        return []

    def run(self):
        out, err = super().run()
        self.tables = Tables(out)
        return out, err
