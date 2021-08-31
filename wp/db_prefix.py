from wp.command import WPCommand


class DBPrefix(WPCommand):
    command = ['db', 'prefix']

    def __init__(self, **args):
        super().__init__(**args)

    def params(self):
        return []
