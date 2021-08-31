from wp.command import WPCommand


class CacheFlush(WPCommand):
    command = ['cache', 'flush']

    def __init__(self, **args):
        super().__init__(**args)

    def params(self):
        return []

