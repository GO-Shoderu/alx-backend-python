#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from unittest.mock import patch
from utils import access_nested_map, get_json

class TestAccessNestedMap(unittest.TestCase):
        
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(context.exception.args[0], expected_key)

class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, mock_get, test_url, test_payload):
        mock_get.return_value.json.return_value = test_payload
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(get_json(test_url), test_payload)