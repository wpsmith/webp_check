from datetime import datetime

from wp.command import WPCommand


class PostUpdate(WPCommand):
    command = ['post', 'update']

    # Post ID.
    id = int

    # [--post_author=<post_author>]
    # The ID of the user who added the post. Default is the current user ID.
    post_author = int

    # [--post_date=<post_date>]
    # The date of the post. Default is the current time.
    post_date = datetime

    # [--post_date_gmt=<post_date_gmt>]
    # The date of the post in the GMT timezone. Default is the value of $post_date.
    post_date_gmt = datetime

    # [--post_content=<post_content>]
    # The post content. Default empty.
    post_content = ''

    # [--post_content_filtered=<post_content_filtered>]
    # The filtered post content. Default empty.
    post_content_filtered = ''

    # [--post_title=<post_title>]
    # The post title. Default empty.
    post_title = ''

    # [--post_excerpt=<post_excerpt>]
    # The post excerpt. Default empty.
    post_excerpt = ''

    # [--post_status=<post_status>]
    # The post status. Default ‘draft’.
    post_status = ''

    # [--post_type=<post_type>]
    # The post type. Default ‘post’.
    post_type = ''

    # [--comment_status=<comment_status>]
    # Whether the post can accept comments. Accepts ‘open’ or ‘closed’.
    # Default is the value of ‘default_comment_status’ option.
    comment_status = ''

    # [--ping_status=<ping_status>]
    # Whether the post can accept pings. Accepts ‘open’ or ‘closed’.
    # Default is the value of ‘default_ping_status’ option.
    ping_status = ''

    # [--post_password=<post_password>]
    # The password to access the post. Default empty.
    post_password = ''

    # [--post_name=<post_name>]
    # The post name. Default is the sanitized post title when creating a new post.
    post_name = ''

    # [--to_ping=<to_ping>]
    # Space or carriage return-separated list of URLs to ping. Default empty.
    to_ping = ''

    # [--pinged=<pinged>]
    # Space or carriage return-separated list of URLs that have been pinged. Default empty.
    pinged = ''

    # [--post_modified=<post_modified>]
    # The date when the post was last modified. Default is the current time.
    post_modified = datetime

    # [--post_modified_gmt=<post_modified_gmt>]
    # The date when the post was last modified in the GMT timezone. Default is the current time.
    post_modified_gmt = datetime

    # [--post_parent=<post_parent>]
    # Set this for the post it belongs to, if any. Default 0.
    post_parent = int

    # [--menu_order=<menu_order>]
    # The order the post should be displayed in. Default 0.
    menu_order = int

    # [--post_mime_type=<post_mime_type>]
    # The mime type of the post. Default empty.
    post_mime_type = ''

    # [--guid=<guid>]
    # Global Unique ID for referencing the post. Default empty.
    # GUID cannot be updated, so why even support it?
    # guid = ''

    # [--post_category=<post_category>]
    # Array of category names, slugs, or IDs. Defaults to value of the ‘default_category’ option.
    post_category = ''

    # [--tags_input=<tags_input>]
    # Array of tag names, slugs, or IDs. Default empty.
    tags_input = ''

    # [--tax_input=<tax_input>]
    # Array of taxonomy terms keyed by their taxonomy name. Default empty.
    tax_input = ''

    # [--meta_input=<meta_input>]
    # Array in JSON format of post meta values keyed by their post meta key. Default empty.
    meta_input = ''

    # [<file>]
    # Read post content from <file>. If this value is present, the
    # --post_content argument will be ignored.
    # Passing - as the filename will cause post content to
    # be read from STDIN.
    file = ''

    # --<field>=<value>
    # One or more fields to update. See wp_insert_post().
    field = ''

    # [--defer-term-counting]
    # Recalculate term count in batch, for a performance boost.
    # Instead of returning the whole post, returns the value of a single field.
    defer_term_counting = ''

    def __init__(self, id, **args):
        super().__init__(**args)
        self.id = id

        self.post_author = self.get_arg_value(key="post_author", default_value=self.post_author)
        self.post_date = self.get_arg_value(key="post_date", default_value=self.post_date)
        self.post_date_gmt = self.get_arg_value(key="post_date_gmt", default_value=self.post_date_gmt)
        self.post_content = self.get_arg_value(key="post_content", default_value=self.post_content)
        self.post_content_filtered = self.get_arg_value(key="post_content_filtered", default_value=self.post_content_filtered)
        self.post_title = self.get_arg_value(key="post_title", default_value=self.post_title)
        self.post_excerpt = self.get_arg_value(key="post_excerpt", default_value=self.post_excerpt)
        self.post_status = self.get_arg_value(key="post_status", default_value=self.post_status)
        self.post_type = self.get_arg_value(key="post_type", default_value=self.post_type)
        self.comment_status = self.get_arg_value(key="comment_status", default_value=self.comment_status)
        self.ping_status = self.get_arg_value(key="ping_status", default_value=self.ping_status)
        self.post_password = self.get_arg_value(key="post_password", default_value=self.post_password)
        self.post_name = self.get_arg_value(key="post_name", default_value=self.post_name)
        self.to_ping = self.get_arg_value(key="to_ping", default_value=self.to_ping)
        self.post_modified = self.get_arg_value(key="post_modified", default_value=self.post_modified)
        self.post_modified_gmt = self.get_arg_value(key="post_modified_gmt", default_value=self.post_modified_gmt)
        self.post_parent = self.get_arg_value(key="post_parent", default_value=self.post_parent)
        self.menu_order = self.get_arg_value(key="menu_order", default_value=self.menu_order)
        self.post_mime_type = self.get_arg_value(key="post_mime_type", default_value=self.post_mime_type)
        # self.guid = self.get_arg_value(key="guid", default_value=self.guid)
        self.post_category = self.get_arg_value(key="post_category", default_value=self.post_category)
        self.tags_input = self.get_arg_value(key="tags_input", default_value=self.tags_input)
        self.tax_input = self.get_arg_value(key="tax_input", default_value=self.tax_input)
        self.meta_input = self.get_arg_value(key="meta_input", default_value=self.meta_input)
        self.field = self.get_arg_value(key="field", default_value=self.field)
        self.defer_term_counting = self.get_arg_value(key="defer_term_counting", default_value=self.defer_term_counting)

    def params(self):
        return [
            str(self.id)
        ]

    def get_excluded_attrs(self):
        return [
            "id"
        ]

    def get_raw_params(self):
        return [
            'post_author',
            'post_date',
            'post_date_gmt',
            'post_content',
            'post_content_filtered',
            'post_title',
            'post_excerpt',
            'post_status',
            'post_type',
            'comment_status',
            'ping_status',
            'post_password',
            'post_name',
            'to_ping',
            'post_modified',
            'post_modified_gmt',
            'post_parent',
            'menu_order',
            'post_mime_type',
            'post_category',
            'tags_input',
            'tax_input',
            'meta_input',
        ]
