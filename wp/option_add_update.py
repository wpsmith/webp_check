from wp.command import WPCommand


class OptionAddUpdate(WPCommand):
    command = ['option', 'upsert']

    # Option key.
    key = ''

    # Option value.
    value = ''

    # Autoload: either yes/no.
    autoload = bool

    # Render output in a particular format.
    # default: plaintext
    # options: plaintext, json
    format = ''

    def __init__(self, key, value='', **args):
        super().__init__(**args)
        self.key = key
        self.value = value

        self.format = self.get_arg_value(key="format", default_value=self.format)

    def params(self):
        return [
            self.key,
            self.value,
        ]

    def get_excluded_attrs(self):
        return [
            "key",
            "value",
        ]
