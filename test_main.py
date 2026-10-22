"""Unit-тесты синтаксиса и поиска MAC-адресов."""

import unittest

from main import find_macs, is_mac, read_url


class MacTests(unittest.TestCase):
    def test_valid_formats(self):
        self.assertTrue(is_mac("AA:bb:01:23:CD:ef"))
        self.assertTrue(is_mac("aa-bb-01-23-cd-ef"))

    def test_length(self):
        self.assertFalse(is_mac("AA:BB:CC:DD:EE"))
        self.assertFalse(is_mac("AA:BB:CC:DD:EE:FF:00"))

    def test_hex_digits(self):
        self.assertFalse(is_mac("GG:BB:CC:DD:EE:FF"))

    def test_same_separator(self):
        self.assertFalse(is_mac("AA:BB-CC:DD:EE:FF"))

    def test_search_boundaries(self):
        text = "xAA:BB:CC:DD:EE:FF AA:BB:CC:DD:EE:FF:00"
        self.assertEqual(find_macs(text), [])

    def test_search_removes_duplicates(self):
        text = "aa-bb-cc-dd-ee-ff и AA:BB:CC:DD:EE:FF; 01:23:45:67:89:ab"
        self.assertEqual(find_macs(text), ["AA:BB:CC:DD:EE:FF", "01:23:45:67:89:AB"])

    def test_url_scheme(self):
        with self.assertRaises(ValueError):
            read_url("file:///example.txt")


if __name__ == "__main__":
    unittest.main()
