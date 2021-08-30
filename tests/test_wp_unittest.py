import unittest

import wp
import config
import os

class TestWPConfig(unittest.TestCase):
    def test_init(self):
        url = 'paideiasoutheast.test'
        wp_cli_cfg = wp.WPCLIConfig(url=url, user='wpsmith')
        self.assertEqual(wp_cli_cfg.url, url, f"Should be {url}")

    def test_yml(self):
        cfg = config.get()
        yml_path = os.path.expandvars(cfg.get('WP_CLI_YML'))
        wp_cli_cfg = wp.WPCLIConfig(yml_path=yml_path)
        print(yml_path)
        self.assertEqual(wp_cli_cfg.yml_path, yml_path, f"Should be {yml_path}")

    def test_command(self):
        cmd = wp.WPCommand()
        # self.assertEqual('EXPECTED', 'ACTUAL', "test: Should be []")
        self.assertEqual([], cmd._prefix(), "prefix: Should be []")
        self.assertEqual([], cmd._suffix(), "suffix: Should be []")
        self.assertEqual(['www-data', 'wp'], cmd._wp_cmd(), "wp_cmd: Should be ['www-data', 'wp']")
        self.assertEqual([''], cmd._cmd(), "cmd: Should be ['search-replace']")
        # self.assertEqual(cmd.cmd(), [
        #
        # ], "Should be something else")

    def test_search_replace(self):
        sr = wp.SearchReplace("old-dne-str", "new-dne-str",
                              table="wp_post*",
                              all_tables_with_prefix=True,
                              path="/Users/travis.smith/Projects/WPS/paideiasoutheast.test",
                              url="domain.com")
        # self.assertEqual(['search-replace'], sr._cmd(), "cmd: Should be ['search-replace']")
        # self.assertEqual(["'old-dne-str'", "'new-dne-str'", 'wp_post*', '--all-tables-with-prefix', '--url=domain.com'], sr._params(), "_params: Should be [\"'old-dne-str'\", \"'new-dne-str'\", 'wp_post*', '--all-tables-with-prefix', '--url=domain.com']")
        # self.assertEqual(['wp', 'search-replace', "'old-dne-str'", "'new-dne-str'", 'wp_post*', '--all-tables-with-prefix', '--url=domain.com'], sr.cmd(), "cmd: Should be ['wp', 'search-replace', 'old', 'new', 'wp_post*]")
        self.assertEqual([], sr.run(), "run: ")



if __name__ == '__main__':
    unittest.main()
