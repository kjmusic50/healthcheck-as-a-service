import unittest
import urllib
import mock

from healthcheck.plugin import (add_url, add_watcher, new, post,
                                command, main, CommandNotFound)


class PluginTest(unittest.TestCase):

    @mock.patch("healthcheck.plugin.post")
    def test_add_url(self, post_mock):
        add_url("name", "url")
        expected_data = {
            "name": "name",
            "url": "url",
        }
        post_mock.assert_called_with("/url", expected_data)

    @mock.patch("healthcheck.plugin.post")
    def test_new(self, post_mock):
        new("name")
        expected_data = {
            "name": "name",
        }
        post_mock.assert_called_with("/", expected_data)

    @mock.patch("healthcheck.plugin.post")
    def test_add_watcher(self, post_mock):
        add_watcher("name", "watcher@watcher.com")
        expected_data = {
            "name": "name",
            "watcher": "watcher@watcher.com",
        }
        post_mock.assert_called_with("/watcher", expected_data)

    @mock.patch("urllib2.Request")
    @mock.patch("urllib2.urlopen")
    def test_post(self, urlopen_mock, request_mock):
        url = "url"
        data = {"name": "name"}
        req_mock = request_mock.return_value
        post(url, data)
        request_mock.assert_called_with(url, urllib.urlencode(data))
        urlopen_mock.assert_called_with(req_mock)

    def test_commands(self):
        expected_commands = {
            "add-url": add_url,
            "new": new,
            "add-watcher": add_watcher,
        }
        for key, cmd in expected_commands.items():
            self.assertEqual(command(key), cmd)

    def test_commands_not_found(self):
        with self.assertRaises(CommandNotFound):
            command('notfound')

    @mock.patch("healthcheck.plugin.add_url")
    def test_main(self, add_url_mock):
        main("add-url", "myhc", "http://tsuru.io")
        add_url_mock.assert_called_with("myhc", "http://tsuru.io")