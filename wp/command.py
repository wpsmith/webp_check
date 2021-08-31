import os

from loggr import logger
import subprocess


class WPCommand(object):
    # Holder for the args.
    _args = {}

    # User running command.
    cmd_user = "www-data"

    # Whether to run as sudo.
    as_sudo = False
    __as_sudo = ["sudo", "-u", cmd_user]
    __as_sudo_param = ["--allow-root"]

    # What should come before the WP Command.
    cmd_prefix = []

    # WordPress command binary
    cmd_base = 'wp'

    # What should follow the WP Command.
    cmd_suffix = []

    # The WP Command.
    command = []

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

    # STDOUT result of run().
    output = ''

    # STDERR result of run().
    error = ''

    # def __setattr__(key, value):
    #     super().__setattr__(key, value)

    def __init__(self, **args):
        super().__init__()
        if self._args is not None:
            self._args = args

        self.cmd_prefix = self.get_arg_value(key="cmd_prefix", default_value=self.cmd_prefix)
        self.as_sudo = self.get_arg_value(key="as_sudo", default_value=self.as_sudo)
        self.cmd_user = self.get_arg_value(key="cmd_user", default_value=self.cmd_user)

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
        # self.quiet = self.get_arg_value(key="quiet", default_value=self.quiet)
        self.apache_modules = self.get_arg_value(key="apache_modules", default_value=self.apache_modules)

    def __getitem__(self, item):
        return super().__getattribute__(item)

    def __str__(self):
        return " ".join([str(elem) for elem in self.cmd()])

    # PUBLIC API.
    def get_arg_value(self, key, default_value):
        value = self._args.get(key)
        if value is None:
            return default_value

        return value

    # Gets everything for the command.
    def cmd(self):
        return self.__cmd()

    def __cmd(self):
        return self.__prefix() + \
               self.__wp_cmd() + \
               self.command + \
               self.__params() + \
               self.__suffix()

    # Runs the command as sudo or as root.
    def run_as_sudo(self):
        self.as_sudo = True
        return self.run()

    # Runs the command.
    def run(self):
        c = self.cmd()
        logger.info(f"running " + " ".join([str(elem) for elem in c]))
        # print(f"running: " + " ".join([str(elem) for elem in c]))

        output, error = subprocess.Popen(
            c, universal_newlines=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        self.output = output.strip("\n")
        self.error = error.strip("\n")

        # print(output)
        # print(error)
        logger.info("Output: {0}".format(self.output))
        logger.info("Errors: {0}".format(self.error))
        return self.output, self.error

        # output = subprocess.check_output(c)
        # output = subprocess.check_output(c, stderr=subprocess.STDOUT)
        # print(output.decode('utf-8'))

        # try:
        #     output = check_output(c, stderr=STDOUT)
        #     # if "This does not seem to be a WordPress installation"
        #     logger.info(output)
        # except CalledProcessError as e:
        #     o = e.output.decode("utf-8")
        #     print(o)
        #     return o

    # Abstract Method. Returns the parameters.
    def params(self):
        raise NotImplementedError("Please implement params")

    # Abstract Method. Returns the parsed output or by default, just the output.
    def get_result(self):
        return self.output

    # Params that should not have underscores (_) replaced with dashes (-).
    # Should be overridden.
    def get_raw_params(self):
        return []

    # Gets excluded attributes. These class/instance attributes will never be outputted.
    # Should be overridden.
    def get_excluded_attrs(self):
        return []

    # Gets the bool attributes. Key should be the raw attribute.
    def get_custom_bool_attrs(self):
        return {}

    # Returns a custom string output for specific attribute.
    def get_attr_custom_param_output(self, attr):
        return ''

    # PRIVATE API.

    # Params that should not have underscores (_) replaced with dashes (-).
    # Should be overridden.
    def __get_raw_params(self):
        return self.get_raw_params() + [
            "apache_modules",
        ]

    # Gets the custom bool attrs. Key should be the raw attribute.
    def __get_custom_bool_attrs(self):
        global_attrs = {
            "color-false": "--no-color",
            "debug-false": "--debug=false",
        }

        attrs = self.get_custom_bool_attrs()
        attrs.update(global_attrs)
        return attrs

    # Gets the custom string attrs.
    def __get_attr_custom_param_output(self, attr):
        if 'format' == attr and hasattr(self, 'format') and '' != self.format:
            return '--format=' + self.format

        return self.get_attr_custom_param_output(attr)

    # Gets excluded attributes.
    def __get_excluded_attrs(self):
        return self.get_excluded_attrs() + [
            "_args",
            "as_sudo",
            "cmd_user",
            "cmd_prefix",
            "cmd_base",
            "cmd_suffix",
            "command",
            "envs",
            "error",
            "output",
            "prompt",
            "quiet",
        ]

    def __filter_atts(self, attr):
        # res = (
        #         not attr.startswith('__')
        #         and not attr.startswith('_' + self.__class__.__name__ + '__')
        #         and not attr.startswith('_WPCommand__')
        #         and not callable(getattr(self, attr))
        #         and attr not in self.__get_excluded_attrs()
        # )
        return (
                not attr.startswith('__')
                and not attr.startswith('_' + self.__class__.__name__ + '__')
                and not attr.startswith('_WPCommand__')
                and not callable(getattr(self, attr))
                and attr not in self.__get_excluded_attrs()
        )

    # Gets all attributes from class that are command parameters
    def __get_attrs(self):
        # print(dir(self))
        orig_attrs = dir(self)
        # attrs = list(filter(self.__filter_atts, dir(self)))
        attrs = [a for a in dir(self) if self.__filter_atts(a)]
        return attrs

    # Returns the prefix.
    def __prefix(self):
        return self.cmd_prefix

    # Returns the user running the command and the command base (`wp`).
    def __wp_cmd(self):
        if self.as_sudo:
            return self.__as_sudo + [
                self.cmd_base
            ]
        return [
            self.cmd_base
        ]

    # Returns the parameters.
    def __params(self):
        # return self._get_params_by_attrs(self._get_attrs(), self.params())
        p = self.params()
        attrs = self.__get_attrs()
        for attr in attrs:
            key = attr
            val = self[attr]
            if attr not in self.__get_raw_params():
                key = key.replace('_', '-')

            custom_out_attr = self.__get_attr_custom_param_output(attr)
            if '' != custom_out_attr:
                p.append(custom_out_attr)
                continue

            t = type(self[attr])
            if bool == t:
                custom_bool_attrs = self.__get_custom_bool_attrs()
                if f"{attr}-{str(val).lower()}" in custom_bool_attrs.keys():
                    p.append(custom_bool_attrs[f"{attr}-{str(val).lower()}"])
                elif self[attr]:
                    p.append(f"--{key}")
            elif list == t:
                if 0 != len(val):
                    val_str = ",".join(val)
                    p.append(f"--{key}=\"{val_str}\"")
            elif str == t:
                if '' != val:
                    # p.append(f"--{key}={val}")
                    p.append(f"--{key}=\"{val}\"")
            else:
                p.append(f"--{key}=\"{val}\"")

        if self.as_sudo and ('root' == self.cmd_user or os.geteuid() == 0):
            p += self.__as_sudo_param

        return p

    def __suffix(self):
        return self.cmd_suffix
