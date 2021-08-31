from wp.option_add_update import OptionAddUpdate


class OptionAdd(OptionAddUpdate):
    command = ['option', 'add']

    def __init__(self, key, value='', **args):
        super().__init__(key, value, **args)

    def params(self):
        return super().params()

    def get_excluded_attrs(self):
        return super().get_excluded_attrs()
