from wp.command import WPCommand


class DBCheck(WPCommand):
    command = ['db', 'check']

    # Extra arguments to pass to mysqldump. Refer to mysqldump docs.
    fields = []

    # Loads the environment’s MySQL option files.
    # Default behavior is to skip loading them to avoid failures due to misconfiguration.
    defaults = []

    def __init__(self, **args):
        super().__init__(**args)

        self.fields = self.get_arg_value(key="fields", default_value=self.fields)
        self.defaults = self.get_arg_value(key="defaults", default_value=self.defaults)

    def params(self):
        return []
