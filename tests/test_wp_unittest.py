import json
import unittest
from subprocess import CalledProcessError

import sqlparse as sqlparse
import config
import os
from wp import WPCLIConfig, SearchReplace, PostGet, DBItems, DBSearch, DBQuery, DBItem, DBColumns, DBExport, DBImport, \
    DBCheck, DBTables


class TestWPConfig(unittest.TestCase):
    def test_init(self):
        url = 'paideiasoutheast.test'
        wp_cli_cfg = WPCLIConfig(url=url, user='wpsmith')
        self.assertEqual(wp_cli_cfg.url, url, f"Should be {url}")

    def test_yml(self):
        cfg = config.get()
        yml_path = os.path.expandvars(cfg.get('WP_CLI_YML'))
        wp_cli_cfg = WPCLIConfig(yml_path=yml_path)

        self.assertEqual(wp_cli_cfg.yml_path, yml_path, f"Should be {yml_path}")

    # def test_command(self):
    #     cmd = wp.WPCommand()
    #     # self.assertEqual('EXPECTED', 'ACTUAL', "test: Should be []")
    #     self.assertEqual([], cmd.__prefix(), "prefix: Should be []")
    #     self.assertEqual([], cmd.__suffix(), "suffix: Should be []")
    #     self.assertEqual(['www-data', 'wp'], cmd.__wp_cmd(), "wp_cmd: Should be ['www-data', 'wp']")
    #     self.assertEqual([''], cmd._cmd(), "cmd: Should be ['search-replace']")

    def test_db_check(self):
        check = DBCheck()
        check.run()

    def test_db_import(self):
        db_import = DBImport(
            os.path.join(os.path.dirname(__file__), 'dump.sql'),
            skip_optimizations=True,
        )
        print(" ".join(db_import.cmd()))
        db_import.run()

    def test_db_export(self):
        export = DBExport(
            os.path.join(os.path.dirname(__file__), 'dump.sql'),
            # no_create_info=True,
            add_drop_table=True,
            # debug=True,
        )
        print(" ".join(export.cmd()))
        export.run()

    def test_db_tables(self):
        tables = DBTables(all_tables=True)
        out, err = tables.run()
        print(tables)
        print(out)
        print(err)

    def test_db_query_describe_table(self):
        db_query = DBQuery("DESCRIBE wp_posts")
        db_query_out, err = db_query.run()
        print(db_query_out)

    def test_db_columns(self):
        # columns = DBColumns("wp_posts", all_tables=True, format="json")
        # columns_out, err = columns.run()
        # print(columns_out)

        columns = DBColumns("wp_actionscheduler_actions", all_tables=True)
        columns_out, err = columns.run()
        print(columns_out)
        print(err)

        columns = DBColumns("wp_actionscheduler_actions", all_tables=True, format="json")
        columns_out, err = columns.run()
        print(columns_out)
        print(err)

        columns = DBColumns("wp_yoast_seo_links", all_tables=True, format="json")
        columns_out, err = columns.run()
        print(columns_out)
        print(err)

    def test_db_query(self):
        i = DBItem.new_from_db_search_item([
            'wp_posts',
            'post_content',
            3049,
            'ock-image size-large"><img src="https://paideiasoutheast.test/wp-content/uploads/2021/08/enriching-nature-journal-watercolor-1024x684.jpg" alt="enriching mama\'s soul with nature'
        ])
        db_query = DBQuery(
            f"SELECT * from {i.table} WHERE {i.column} LIKE \"%{i.value}%\""
                              # skip_column_names=True
        )
        db_query_out, err = db_query.run()
        print(db_query_out)

    def test_db_query_unknown_table(self):
        i = DBItem(['wp_yoast_seo_links', 'url', 950, 'https://paideiasoutheast.test/wp-content/uploads/2021/03/TwigyPosts-321-1024x684.jpg'])
        db_query = DBQuery(
            f"SELECT * from {i.table} WHERE {i.column} LIKE \"%{i.value}%\""
                              # skip_column_names=True
        )
        db_query_out, err = db_query.run()

        parts = {}
        rows = db_query_out.strip().split("\n")
        if 2 == len(rows):
            keys = rows[0].strip().split("\t")
            values = rows[1].strip().split("\t")

            parts = dict(zip(keys, values))
        # if 4 == len(parts):
        #     parts.append(re.sub(get_pattern(), "\\1\\2webp", parts[2]))
        return parts

    def test_db_query_escape(self):
        val1 = DBQuery.escape("testing \" quotes \"")
        val2 = DBQuery.escape_d("testing \" quotes \"")
        print(val1)
        print(val2)

    def test_db_search(self):
        s = DBSearch(
            # 'paideiasoutheast\.test\/.+(jpg|jpeg|png|gif)',
            'paideiasoutheast\.test[-a-zA-Z0-9()@:%_\+.~#?&\/=]+?([\w\d_-]+)\.(jpg|jpeg|png|gif)',
            regex=True,
            all_tables=True,
            table_column_once=True,
            one_line=True,
            # matches_only=True,
            color=False,
            quiet=True,
            debug=True,
        )
        print(s)
        out, err = s.run()

        items = DBItems.new_from_search_output(out)
        # for line in out.splitlines():
        #     parts = line.split(":", 4)
        #     print("||".join(parts))


        for item in items.items:
            if 'wp_posts' == item.table:
                post = PostGet(item.id, format="json").run()
                print(post)
                # post_dict = json.loads(post)
                # print(post_dict)
            print(item)

    def test_post_get(self):
        post = PostGet(3, format="json")
        print(post)
        out = post.run()
        # print(out)
        post_dict = json.loads(out)
        print(post_dict)

        # search for images



    def test_search_replace_yaml(self):
        sr = SearchReplace("paideiasoutheast.test", "paideiasoutheast.com",
                              table="wp_post*",
                              debug=True,
                              dry_run=True,
                              skip_themes=True,
                              skip_plugins=True,
                              color=False,
                              all_tables=True)
        sr.run()

    def test_search_replace(self):
        sr = SearchReplace("old-dne-str", "new-dne-str",
                              table="wp_post*",
                              dry_run=True,
                              all_tables_with_prefix=True,
                              path="/Users/travis.smith/Projects/WPS/paideiasoutheast.test",
                              url="domain.com")
        self.assertEqual(['search-replace'],
            sr._cmd(),
            "cmd: Should be ['search-replace']")

        expected_output = [
            "\"old-dne-str\"",
            "\"new-dne-str\"",
            "\"wp_post*\"",
            '--all-tables-with-prefix',
            '--dry-run',
            '--path="/Users/travis.smith/Projects/WPS/paideiasoutheast.test"',
            '--url="domain.com"'
        ]
        self.assertEqual(
            expected_output,
            sr.__params(),
            "_params: Should be [{0}]\n".format(",\n".join(expected_output)))

        expected_output = [
            'wp',
            'search-replace',
            "\"old-dne-str\"",
            "\"new-dne-str\"",
            "\"wp_post*\"",
            '--all-tables-with-prefix',
            '--dry-run',
            '--path="/Users/travis.smith/Projects/WPS/paideiasoutheast.test"',
            '--url="domain.com"'
        ]
        self.assertEqual(
            expected_output,
            sr.cmd(),
            self.assert_msg('cmd', expected_output))

        # Test invalid path.
        with self.assertRaises(CalledProcessError):
            sr.run()

    def assert_msg(self, cmd_name, value):
        return "{0}: Should be [{1}]\n".format(cmd_name, ",\n".join(value))


if __name__ == '__main__':
    unittest.main()
