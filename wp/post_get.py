from wp.command import WPCommand


class PostGet(WPCommand):
    command = ['post', 'get']

    # Post ID.
    id = int

    # Instead of returning the whole post, returns the value of a single field.
    field = ''

    # Limit the output to specific fields. Defaults to all fields.
    fields = ''

    # Render output in a particular format.
    # default: table
    # options: table, csv, json, yaml
    format = ''

    def __init__(self, id, **args):
        super().__init__(**args)
        self.id = id

        self.format = self.get_arg_value(key="format", default_value=self.format)
        self.field = self.get_arg_value(key="field", default_value=self.field)
        self.fields = self.get_arg_value(key="fields", default_value=self.fields)

    def params(self):
        return [
            str(self.id)
        ]

    def get_excluded_attrs(self):
        return [
            "id"
        ]

    # Gets the custom string attrs.
    def get_attr_custom_param_output(self, attr):
        if 'fields' == attr and hasattr(self, 'fields') and '' != self.fields:
            return '--fields=' + self.fields

        return ''
