from wp.command import WPCommand


class DBSearch(WPCommand):
    command = ['db', 'search']

    # SQL.
    search = ''  # Required

    # One or more tables to search through for the string.
    tables = ''

    # Search through all the tables registered to $wpdb in a multisite install.
    network = bool

    # Enable replacement on any tables that match the table prefix even if not registered on $wpdb.
    all_tables_with_prefix = bool

    # Enable replacement on ALL tables in the database, regardless of the prefix, and even if not registered on $wpdb.
    # Overrides –network and –all-tables-with-prefix.
    all_tables = bool

    # For logging, number of characters to display before the old match and the new replacement.
    # Default 40. Ignored if not logging.
    before_context = int

    # For logging, number of characters to display after the old match and the new replacement.
    # Default 40. Ignored if not logging.
    after_context = int

    # Runs the search as a regular expression (without delimiters). The search becomes case-sensitive
    # (i.e. no PCRE flags are added). Delimiters must be escaped if they occur in the expression.
    # Because the search is run on individual columns, you can use the ^ and $ tokens
    # to mark the start and end of a match, respectively.
    regex = bool

    # Pass PCRE modifiers to the regex search (e.g. ‘i’ for case-insensitivity).
    regex_flags = ''

    # The delimiter to use for the regex. It must be escaped if it appears in the search string.
    # The default value is the result of chr(1).
    regex_delimiter = ''

    # Output the ‘table:column’ line once before all matching row lines in the table column
    # rather than before each matching row.
    table_column_once = bool

    # Place the ‘table:column’ output on the same line as the row id and match (‘table:column:id:match’).
    # Overrides –table_column_once.
    one_line = bool

    # Only output the string matches (including context). No ‘table:column’s or row ids are outputted.
    matches_only = bool

    # Output stats on the number of matches found, time taken, tables/columns/rows searched, tables skipped.
    stats = bool

    # Percent color code to use for the ‘table:column’ output. For a list of available percent color codes, see below.
    # Default ‘%G’ (bright green).
    table_column_color = ''

    # Percent color code to use for the row id output. For a list of available percent color codes, see below.
    # Default ‘%Y’ (bright yellow).
    id_color = ''

    # Percent color code to use for the match (unless both before and after context are 0, when no color code is used).
    # For a list of available percent color codes, see below. Default ‘%3%k’ (black on a mustard background).
    match_color = ''

    def __init__(self, search, **args):
        super().__init__(**args)
        self.search = search

        self.all_tables_with_prefix = self.get_arg_value(key="all_tables_with_prefix",
                                                         default_value=self.all_tables_with_prefix)
        self.all_tables = self.get_arg_value(key="all_tables", default_value=self.all_tables)
        self.before_context = self.get_arg_value(key="before_context", default_value=self.before_context)
        self.after_context = self.get_arg_value(key="after_context", default_value=self.after_context)
        self.regex = self.get_arg_value(key="regex", default_value=self.regex)
        self.regex_flags = self.get_arg_value(key="regex_flags", default_value=self.regex_flags)
        self.regex_delimiter = self.get_arg_value(key="regex_delimiter", default_value=self.regex_delimiter)
        self.table_column_once = self.get_arg_value(key="table_column_once", default_value=self.table_column_once)
        self.one_line = self.get_arg_value(key="one_line", default_value=self.one_line)
        self.matches_only = self.get_arg_value(key="matches_only", default_value=self.matches_only)
        self.stats = self.get_arg_value(key="stats", default_value=self.stats)
        self.table_column_color = self.get_arg_value(key="table_column_color", default_value=self.table_column_color)
        self.id_color = self.get_arg_value(key="id_color", default_value=self.id_color)
        self.match_color = self.get_arg_value(key="match_color", default_value=self.match_color)

    def params(self):
        return [
            self.search
        ]

    def get_raw_params(self):
        return [
            "before_context",
            "after_context",
            "table_column_once",
            "one_line",
            "matches_only",
            "table_column_color",
            "id_color",
            "match_color",
        ]

    def get_excluded_attrs(self):
        return [
            "search"
        ]
