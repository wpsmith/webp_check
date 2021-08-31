from wp.command import WPCommand


class SearchReplace(WPCommand):
    command = ['search-replace']

    # A string to search for within the database.
    old = ''  # Required

    # Replace instances of the first string with this new string.
    new = ''  # Required

    # List of database tables to restrict the replacement to. Wildcards are supported, e.g. 'wp_*options' or 'wp_post*'.
    table = ''  # Optional

    # Parameters
    # Run the entire search/replace operation and show report, but don’t save changes to the database.
    dry_run = bool

    # Search/replace through all the tables registered to $wpdb in a multisite install.
    network = bool

    # Enable replacement on any tables that match the table prefix even if not registered on $wpdb.
    all_tables_with_prefix = bool

    # Enable replacement on ALL tables in the database, regardless of the prefix, and even if not registered on $wpdb.
    # Overrides –network and –all-tables-with-prefix.
    all_tables = bool

    # Write transformed data as SQL file instead of saving replacements to the database.
    # If <file> is not supplied, will output to STDOUT.
    export = ''

    # Define number of rows in single INSERT statement when doing SQL export.
    # You might want to change this depending on your database configuration (e.g. if you need to do fewer queries).
    # Default: 50
    export_insert_size = int

    # Do not perform the replacement on specific tables. Use commas to specify multiple tables.
    # Wildcards are supported, e.g. 'wp_*options' or 'wp_post*'.
    skip_tables = ''

    # Do not perform the replacement on specific columns. Use commas to specify multiple columns.
    skip_columns = ''

    # Perform the replacement on specific columns. Use commas to specify multiple columns.
    include_columns = ''

    # Force the use of PHP (instead of SQL) which is more thorough, but slower.
    precise = bool

    # Enable recursing into objects to replace strings. Defaults to true; pass –no-recurse-objects to disable.
    recurse_objects = bool

    # Prints rows to the console as they’re updated.
    verbose = bool

    # Runs the search using a regular expression (without delimiters).
    # Warning: search-replace will take about 15-20x longer when using –regex.
    regex = bool

    # Pass PCRE modifiers to regex search-replace (e.g. ‘i’ for case-insensitivity).
    regex_flags = ''

    # The delimiter to use for the regex. It must be escaped if it appears in the search string.
    # The default value is the result of chr(1).
    regex_delimiter = ''

    # The maximum possible replacements for the regex per row (or per unserialized data bit per row).
    # Defaults to -1 (no limit).
    regex_limit = int

    # Render output in a particular format. Options: table, count
    format = ''

    # Produce report. Defaults to true.
    report = bool

    # Report changed fields only. Defaults to false, unless logging, when it defaults to true.
    report_changed_only = ''

    # Log the items changed. If <file> is not supplied or is “-“, will output to STDOUT.
    # Warning: causes a significant slow down, similar or worse to enabling –precise or –regex.
    log = ''

    # For logging, number of characters to display before the old match and the new replacement.
    # Default 40. Ignored if not logging.
    before_context = int

    # For logging, number of characters to display after the old match and the new replacement.
    # Default 40. Ignored if not logging.
    after_context = int

    def __init__(self, old, new, **args):
        super().__init__(**args)
        # super().__init__(self, self.command, **args)
        self.old = old
        self.new = new

        self.table = self.get_arg_value(key="table", default_value=self.table)
        self.dry_run = self.get_arg_value(key="dry_run", default_value=self.dry_run)
        self.network = self.get_arg_value(key="network", default_value=self.network)
        self.all_tables_with_prefix = self.get_arg_value(key="all_tables_with_prefix",
                                                         default_value=self.all_tables_with_prefix)
        self.all_tables = self.get_arg_value(key="all_tables", default_value=self.all_tables)
        self.export = self.get_arg_value(key="export", default_value=self.export)
        self.export_insert_size = self.get_arg_value(key="export_insert_size", default_value=self.export_insert_size)
        self.skip_tables = self.get_arg_value(key="skip_tables", default_value=self.skip_tables)
        self.skip_columns = self.get_arg_value(key="skip_columns", default_value=self.skip_columns)
        self.include_columns = self.get_arg_value(key="include_columns", default_value=self.include_columns)
        self.precise = self.get_arg_value(key="precise", default_value=self.precise)
        self.recurse_objects = self.get_arg_value(key="recurse_objects", default_value=self.recurse_objects)
        self.verbose = self.get_arg_value(key="verbose", default_value=self.verbose)
        self.regex = self.get_arg_value(key="regex", default_value=self.regex)
        self.regex_flags = self.get_arg_value(key="regex_flags", default_value=self.regex_flags)
        self.regex_delimiter = self.get_arg_value(key="regex_delimiter", default_value=self.regex_delimiter)
        self.regex_limit = self.get_arg_value(key="regex_limit", default_value=self.regex_limit)
        self.format = self.get_arg_value(key="format", default_value=self.format)
        self.report = self.get_arg_value(key="report", default_value=self.report)
        self.report_changed_only = self.get_arg_value(key="report_changed_only", default_value=self.report_changed_only)
        self.log = self.get_arg_value(key="log", default_value=self.log)
        self.before_context = self.get_arg_value(key="before_context", default_value=self.before_context)
        self.after_context = self.get_arg_value(key="after_context", default_value=self.after_context)

    def params(self):
        p = [
            self.old,
            self.new
        ]
        if "" != self.table:
            p.append(self.table)

        return p
        # return [
        #     self.old,
        #     self.new,
        #     self.table,
        #     # f"\"{self.old}\"",
        #     # f"\"{self.new}\"",
        #     # f"'{self.table}'"
        # ]

    def get_raw_params(self):
        return [
            "before_context",
            "after_context"
        ]

    def get_excluded_attrs(self):
        return [
            "old",
            "new",
            "table"
        ]

    def get_attr_custom_param_output(self, attr):
        if 'regex_flags' == attr and '' != self.regex_flags:
            return '--regex-flags=' + self.regex_flags
        if 'include_columns' == attr and '' != self.include_columns:
            return '--include-columns=' + self.include_columns

        return ''
