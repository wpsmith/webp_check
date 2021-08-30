import yaml
import re


class WPCLIBaseItem(object):
    url = ''
    path = ''
    disabled_commands = []
    require = []

    def __init__(self, **args):
        self.url = args.get('url')
        self.path = args.get('path')
        self.disabled_commands = args.get('disabled_commands')
        self.require = args.get('require')

    def __add__(self, other):
        item = self
        item.maybe_set("url", other.url)
        item.maybe_set("path", other.path)
        item.maybe_set("disabled_commands", other.disabled_commands)
        item.maybe_set("require", other.require)

        return item

    def maybe_set(self, key, value):
        if self.has_value(value):
            super().__setattr__(key, value)

    @staticmethod
    def has_value(val):
        return val is not None or val != ''


class WPCLISSHItem(WPCLIBaseItem):
    cmd = ''

    def __init__(self, **args):
        super().__init__(**args)
        self.cmd = args.get('cmd')

    def __add__(self, other):
        item = super().__add__(other)
        item.maybe_set("cmd", other.cmd)

        return item


class WPCLISSH(object):
    vagrant = WPCLISSHItem
    development = WPCLISSHItem
    staging = WPCLISSHItem
    production = WPCLISSHItem

    def __init__(self, **args):
        self.vagrant = args.get('vagrant')
        self.development = args.get('development')
        self.staging = args.get('staging')
        self.production = args.get('production')

    def __add__(self, other):
        item = super().__add__(other)

        item.maybe_set("development", other.development)
        item.maybe_set("staging", other.staging)
        item.maybe_set("production", other.production)

        return item


class WPCLIItem(WPCLIBaseItem):
    ssh = WPCLISSH
    http = ''
    user = ''
    color = ''

    def __init__(self, **args):
        super().__init__(**args)
        self.ssh = args.get('ssh')
        self.http = args.get('http')
        self.user = args.get('user')
        self.color = args.get('color')

    def __add__(self, other):
        item = super().__add__(other)
        item.maybe_set("ssh", other.ssh)
        item.maybe_set("http", other.http)
        item.maybe_set("user", other.user)
        item.maybe_set("color", other.color)

        return item


class WPCLIConfig(WPCLIItem):
    ssh = WPCLISSH

    # Environments
    both = []
    development = WPCLIItem
    staging = WPCLIItem
    production = WPCLIItem
    vagrant = WPCLIItem

    # Global Parameters
    skip_themes = False
    skip_plugins = False
    skip_packages = False
    debug = False

    # Private Parameters
    yml_path = ''
    yml_str = ''

    def __init__(self, **args):
        super().__init__(**args)

        self.debug = args.get('debug')
        self.skip_themes = args.get('skip_themes')
        self.skip_plugins = args.get('skip_plugins')
        self.skip_packages = args.get('skip_packages')

        self.yml_path = args.get('yml_path')
        if self.yml_path is not None:
            self.load()

    def __add__(self, other):
        item = super().__add__(other)

        item.maybe_set("ssh", other.ssh)
        item.maybe_set("debug", other.debug)
        item.maybe_set("skip_themes", other.skip_themes)
        item.maybe_set("skip_plugins", other.skip_plugins)
        item.maybe_set("skip_packages", other.skip_packages)
        item.maybe_set("both", other.both)
        item.maybe_set("development", other.development)
        item.maybe_set("production", other.production)
        item.maybe_set("staging", other.staging)
        item.maybe_set("vagrant", other.vagrant)

        return item

    def normalize_yml(self):
        str = self.yml_str

        # Replace all ` - @`
        str = re.sub(
            r"^(\s-\s?)@",
            "\\1",
            str,
            flags=re.MULTILINE
        )

        # Replace all `^@`
        str = re.sub(
            r"^@",
            "",
            str,
            flags=re.MULTILINE
        )

        return "!WPCLIConfig\n" + str

    def load(self, path=''):
        if '' == path:
            path = self.yml_path

        try:
            # Load the wp-cli.sample.yml file into a string.
            with open(path, "r") as f:
                self.yml_str = f.read()
                f.close()
            self.yml_str = self.normalize_yml()

            # Parse the YML file.
            loader = self.get_loader()
            self._data = yaml.load(self.yml_str, Loader=loader)

            # Merge everything.
            self = self + self._data

        except yaml.YAMLError as e:
            print(e)

    def get_loader(self):
        """Add constructors to PyYAML loader."""
        loader = yaml.SafeLoader
        loader.add_constructor("!WPCLIConfig", wpcli_conf_constructor)
        return loader


def wpcli_conf_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> WPCLIConfig:
    return WPCLIConfig(**loader.construct_mapping(node))
