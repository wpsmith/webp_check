from wp.command import WPCommand


class Eval(WPCommand):
    command = ['eval']

    # <php-code>
    # The code to execute, as a string.

    # [--skip-wordpress]
    # Execute code without loading WordPress.
    skip_wordpress = bool

    def __init__(self, code, **args):
        super().__init__(**args)

        self.code = code
        self.skip_wordpress = self.get_arg_value(key="skip_wordpress", default_value=self.skip_wordpress)

    def params(self):
        return [
            self.code
        ]

    def get_excluded_attrs(self):
        return [
            "code"
        ]
