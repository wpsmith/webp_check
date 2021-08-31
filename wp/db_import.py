from wp.command import WPCommand


class DBImport(WPCommand):
    command = ['db', 'import']

    # File.
    file = ''  # Required

    # When using an SQL file, do not include speed optimization such as disabling auto-commit and key checks.
    skip_optimization = bool

    # Extra arguments to pass to mysqldump. Refer to mysqldump docs.
    fields = []

    # Loads the environment’s MySQL option files.
    # Default behavior is to skip loading them to avoid failures due to misconfiguration.
    defaults = []

    def __init__(self, file, **args):
        super().__init__(**args)
        self.file = file

        self.skip_optimization = self.get_arg_value(key="skip_optimization", default_value=self.skip_optimization)
        self.fields = self.get_arg_value(key="fields", default_value=self.fields)
        self.defaults = self.get_arg_value(key="defaults", default_value=self.defaults)

    def params(self):
        return [
            self.file
        ]

    def get_excluded_attrs(self):
        return [
            "file"
        ]

