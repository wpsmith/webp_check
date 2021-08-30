from subprocess import check_output, CalledProcessError, STDOUT
from loggr import logger


class WPCommand(object):
    # Holder for the args.
    _args = {}

    # User running command.
    cmd_user = "www-data"

    # Whether to run as sudo.
    as_sudo = False
    _as_sudo = ["sudo", "-u", cmd_user]
    _as_sudo_param = ["--allow-root"]

    # What should come before the WP Command.
    cmd_prefix = []

    # WordPress command binary
    cmd_base = 'wp'

    # What should follow the WP Command.
    cmd_suffix = []

    # The WP Command.
    command = ''

    # GLOBAL PARAMETERS.

    # Path to the WordPress files.
    path = ''

    # Perform operation against a remote server over SSH.
    ssh = ''

    # Perform operation against a remote WordPress install over HTTP.
    http = ''

    # Pretend request came from given URL. In multisite, this argument is how the target site is specified.
    url = ''

    # Set the WordPress user. Options: id,email,login
    user = ''

    # Skip loading all or some plugins. Note: mu-plugins are still loaded.
    skip_plugins = ''

    # Skip loading all or some themes.
    skip_themes = ''

    # Skip loading all installed packages.
    skip_packages = []

    # Whether to colorize the output.
    color = ''

    # Show all PHP errors; add verbosity to WP-CLI bootstrap.
    # Not implemented
    debug = bool

    # Suppress informational messages.
    # Not implemented.
    quiet = False

    # List of Apache Modules that are to be reported as loaded.
    apache_modules = []

    # List of PHP files to require before running.
    require = []

    # PHP to execute
    exec = ''

    # Whether to prompt
    prompt = False

    # Environment Variables.
    #  TODO Make this do something.
    envs = {
        # WP_CLI_CACHE_DIR – Directory to store the WP-CLI file cache.
        # Default is ~/.wp-cli/cache/.
        "WP_CLI_CACHE_DIR": '~/.wp-cli/cache/',

        # WP_CLI_CONFIG_PATH – Path to the global config.yml file.
        # Default is ~/.wp-cli/config.yml.
        "WP_CLI_CONFIG_PATH": '~/.wp-cli/config.yml',

        # WP_CLI_CUSTOM_SHELL – Allows the user to override the default /bin/bash shell used.
        "WP_CLI_CUSTOM_SHELL": '',

        # WP_CLI_DISABLE_AUTO_CHECK_UPDATE – Disable WP-CLI automatic checks for updates.
        "WP_CLI_DISABLE_AUTO_CHECK_UPDATE": '',

        # WP_CLI_PACKAGES_DIR – Directory to store packages installed through WP-CLI’s package management.
        # Default is ~/.wp-cli/packages/.
        "WP_CLI_PACKAGES_DIR": '~/.wp-cli/packages/',

        # WP_CLI_PHP – PHP binary path to use when overriding the system default (only works for non-Phar installation).
        "WP_CLI_PHP": '',

        # WP_CLI_PHP_ARGS – Arguments to pass to the PHP binary when invoking WP-CLI (only works for non-Phar installation).
        "WP_CLI_PHP_ARGS": '',

        # WP_CLI_SSH_PRE_CMD – When using --ssh:<ssh>, perform a command before WP-CLI calls WP-CLI on the remote server.
        "WP_CLI_SSH_PRE_CMD": '',

        # WP_CLI_STRICT_ARGS_MODE – Avoid ambiguity by telling WP-CLI to treat any arguments before the command as global,
        # and after the command as local.
        "WP_CLI_STRICT_ARGS_MODE": '',

        # WP_CLI_SUPPRESS_GLOBAL_PARAMS – Set to true to skip showing the global parameters at the end of the help screen.
        # This saves screen estate for advanced users.
        "WP_CLI_SUPPRESS_GLOBAL_PARAMS": '',
    }

    # def __setattr__(key, value):
    #     super().__setattr__(key, value)

    def __init__(self, **args):
        if self._args is None:
            self._args = args
        self.cmd_prefix = self.get_arg_value(key="cmd_prefix", default_value=self.cmd_prefix)
        self.as_sudo = self.get_arg_value(key="as_sudo", default_value=self.as_sudo)

        # Global parameters.
        self.path = self.get_arg_value(key="path", default_value=self.path)
        self.ssh = self.get_arg_value(key="ssh", default_value=self.ssh)
        self.http = self.get_arg_value(key="http", default_value=self.http)
        self.url = self.get_arg_value(key="url", default_value=self.url)
        self.user = self.get_arg_value(key="user", default_value=self.user)
        self.skip_plugins = self.get_arg_value(key="skip_plugins", default_value=self.skip_plugins)
        self.skip_themes = self.get_arg_value(key="skip_themes", default_value=self.skip_themes)
        self.skip_packages = self.get_arg_value(key="skip_packages", default_value=self.skip_packages)
        self.color = self.get_arg_value(key="color", default_value=self.color)
        self.debug = self.get_arg_value(key="debug", default_value=self.debug)
        self.quiet = self.get_arg_value(key="quiet", default_value=self.quiet)
        self.apache_modules = self.get_arg_value(key="apache_modules", default_value=self.apache_modules)

    # self.cmd_prefix = self.get_arg_value(key="cmd_prefix", default_value=self.cmd_prefix, args=args)
    # self.as_sudo = self.get_arg_value(key="as_sudo", default_value=self.as_sudo, args=args)
    # # self.cmd_user = self.get_arg_value(key="cmd_user", default_value=self.cmd_user, args=args)
    #
    # # Global parameters.
    # self.path = self.get_arg_value(key="path", default_value=self.path, args=args)
    # self.ssh = self.get_arg_value(key="ssh", default_value=self.ssh, args=args)
    # self.http = self.get_arg_value(key="http", default_value=self.http, args=args)
    # self.url = self.get_arg_value(key="url", default_value=self.url, args=args)
    # self.user = self.get_arg_value(key="user", default_value=self.user, args=args)
    # self.skip_plugins = self.get_arg_value(key="skip_plugins", default_value=self.skip_plugins, args=args)
    # self.skip_themes = self.get_arg_value(key="skip_themes", default_value=self.skip_themes, args=args)
    # self.skip_packages = self.get_arg_value(key="skip_packages", default_value=self.skip_packages, args=args)
    # self.color = self.get_arg_value(key="color", default_value=self.color, args=args)
    # self.debug = self.get_arg_value(key="debug", default_value=self.debug, args=args)
    # self.quiet = self.get_arg_value(key="quiet", default_value=self.quiet, args=args)
    # self.apache_modules = self.get_arg_value(key="apache_modules", default_value=self.apache_modules, args=args)

    def __getitem__(self, item):
        return super().__getattribute__(item)

    # def get_arg_value(self, key, default_value, **args):
    def get_arg_value(self, key, default_value):
        value = self._args.get(key)
        if value is None:
            return default_value

        return value

    # Gets everything for the command.
    def cmd(self):
        return self._prefix() + \
               self._wp_cmd() + \
               self._cmd() + \
               self._params() + \
               self._suffix()
        # return self._prefix() + \
        #        self._wp_cmd() + \
        #        # self._global_params() + \
        #        self._cmd() + \
        #        self._params() + \
        #        self._suffix()

    # Runs the command.
    def run(self):
        c = self.cmd()
        logger.info(f"running " + " ".join(c))
        print(f"running: " + " ".join(c))
        output = check_output(c, stderr=STDOUT)
        logger.info(output)

        # try:
        #     output = check_output(c, stderr=STDOUT)
        #     # if "This does not seem to be a WordPress installation"
        #     logger.info(output)
        # except CalledProcessError as e:
        #     o = e.output.decode("utf-8")
        #     print(o)
        #     return o


    # Returns the parameters.
    def params(self):
        return []

    # Params that should not have underscores (_) replaced with dashes (-).
    # Should be overridden.
    def get_raw_params(self):
        return [
            "apache_modules",
        ]

    # Gets excluded attributes.
    # Should be overridden.
    def get_excluded_attrs(self):
        return [
            "_args",
            "as_sudo",
            "_as_sudo",
            "_as_sudo_param",
            "cmd_user",
            "cmd_prefix",
            "cmd_base",
            "cmd_suffix",
            "command",
            "envs",
        ]

    # PRIVATE
    # Returns the prefix.
    def _prefix(self):
        return self.cmd_prefix

    # Returns the user running the command and the command base (`wp`).
    def _wp_cmd(self):
        if self.as_sudo:
            return self._as_sudo + [
                self.cmd_base
            ]
        return [
            self.cmd_base
        ]

    # Returns the WP CLI command.
    def _cmd(self):
        return [
            self.command
        ]

    # def _global_params(self):
    #     return self._get_params_by_attrs(self._get_global_attrs(), [])

    # def _get_params_by_attrs(self, attrs, p):
    #     # p = self.params()
    #     for attr in attrs:
    #         key = attr
    #         val = self[attr]
    #
    #         # Replace underscores with dashes except for those which are RAW.
    #         if attr not in self.get_raw_params():
    #             key = key.replace('_', '-')
    #
    #         # Prepare output
    #         t = type(self[attr])
    #         if bool == t:
    #             false_attrs = self._get_false_attrs()
    #             if key in false_attrs:
    #                 p.append(false_attrs[key])
    #             elif self[attr]:
    #                 p.append(f"--{key}")
    #         elif list == t:
    #             if 0 != len(val):
    #                 val_str = ",".join(val)
    #                 p.append(f"--{key}=\"{val_str}\"")
    #         elif str == t:
    #             if '' != val:
    #                 p.append(f"--{key}=\"{val}\"")
    #         else:
    #             p.append(f"--{key}=\"{val}\"")
    #
    #     # Prepare sudo.
    #     if self.as_sudo:
    #         p += self._as_sudo_param
    #
    #     return p

    # Returns the parameters.
    def _params(self):
        # return self._get_params_by_attrs(self._get_attrs(), self.params())
        p = self.params()
        for attr in self._get_attrs():
            key = attr
            val = self[attr]
            if attr not in self.get_raw_params():
                key = key.replace('_', '-')

            t = type(self[attr])
            if bool == t:
                p.append(f"--{key}")
            elif list == t:
                if 0 != len(val):
                    val_str = ",".join(val)
                    p.append(f"--{key}=\"{val_str}\"")
            elif str == t:
                if '' != val:
                    p.append(f"--{key}=\"{val}\"")
            else:
                p.append(f"--{key}=\"{val}\"")

        if self.as_sudo:
            p += self._as_sudo_param

        return p

    # Gets all attributes from class that are command parameters
    def _get_attrs(self):
        # print(dir(self))
        return [a for a in dir(self)
                if not a.startswith('__') and not callable(getattr(self, a)) and a not in self._get_excluded_attrs()]

    # Gets global attributes
    # @classmethod
    # def _get_global_attrs(cls):
    #     return [
    #         "path",
    #         "url",
    #         "ssh",
    #         "http",
    #         "user",
    #         "skip_plugins",
    #         "skip_themes",
    #         "skip_packages",
    #         "require",
    #         "exec",
    #         "color",
    #         "debug",
    #         "prompt", # Not implemented
    #         "quiet", # Not implemented
    #     ]

    # Gets the false attrs.
    def _get_false_attrs(self):
        return {
            "color": "--no-color",
            "debug": "--debug=false",
        }

    # Gets excluded attributes.
    def _get_excluded_attrs(self):
        return [
                   'command',
                   "prompt",
                   "quiet",
               ] + self.get_excluded_attrs()
        # return ['command'] + self.get_excluded_attrs() + WPCommand._get_global_attrs()

    def _suffix(self):
        return self.cmd_suffix
