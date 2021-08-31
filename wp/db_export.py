from wp.command import WPCommand


class DBExport(WPCommand):
    command = ['db', 'export']

    # File.
    file = ''  # Required

    # add-drop-table
    add_drop_table = False

    # no-create-info
    no_create_info = False

    # Extra arguments to pass to mysqldump. Refer to mysqldump docs.
    fields = []

    # WHERE phrase
    where = ''

    # The comma separated list of specific tables to export.
    # Excluding this parameter will export all tables in the database.
    tables = ''

    # The comma separated list of specific tables that should be skipped from exporting.
    # Excluding this parameter will export all tables in the database.
    exclude_tables = ''

    # include-tablespaces: Skips adding the default –no-tablespaces option to mysqldump.
    include_tablespaces = ''

    # Output filename for the exported database.
    porcelain = ''

    # Loads the environment’s MySQL option files.
    # Default behavior is to skip loading them to avoid failures due to misconfiguration.
    defaults = []

    def __init__(self, file, **args):
        super().__init__(**args)
        self.file = file

        self.no_create_info = self.get_arg_value(key="no_create_info", default_value=self.no_create_info)
        self.add_drop_table = self.get_arg_value(key="add_drop_table", default_value=self.add_drop_table)
        self.where = self.get_arg_value(key="where", default_value=self.where)
        self.fields = self.get_arg_value(key="fields", default_value=self.fields)
        self.tables = self.get_arg_value(key="tables", default_value=self.tables)
        self.exclude_tables = self.get_arg_value(key="exclude_tables", default_value=self.exclude_tables)
        self.include_tablespaces = self.get_arg_value(key="include_tablespaces", default_value=self.include_tablespaces)
        self.porcelain = self.get_arg_value(key="porcelain", default_value=self.porcelain)
        self.defaults = self.get_arg_value(key="defaults", default_value=self.defaults)

        # Prevent stupidity.
        if self.add_drop_table:
            self.no_create_info = False

    def params(self):
        return [
            self.file
        ]

    def get_raw_params(self):
        return [
            "exclude_tables",
        ]

    def get_excluded_attrs(self):
        return [
            "file"
        ]

    # Gets the false attrs.
    def get_custom_bool_attrs(self):
        return {
            "no_create_info-true": "--no-create-info=true"
        }
