from wp.command import WPCommand


class OptionGet(WPCommand):
    command = ['option', 'get']

    # Option key.
    key = ''

    # Render output in a particular format.
    # default: var_export
    # options: var_export, json, yaml
    format = ''

    def __init__(self, key, **args):
        super().__init__(**args)
        self.key = key

        self.format = self.get_arg_value(key="format", default_value=self.format)

    def params(self):
        return [
            str(self.key)
        ]

    def get_excluded_attrs(self):
        return [
            "key"
        ]
