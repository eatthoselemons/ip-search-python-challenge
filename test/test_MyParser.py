from unittest import TestCase
from MyParser import MyParser


class TestMyParser(TestCase):
    def test_parse_input_file_ipv4(self):
        my_parser = MyParser()
        ip_list: list[str] = my_parser.parse_input_file(f'./test_MyParser/test_parser_file.txt')
        assert_list: list[str] = ['1.29.45.88', '10.0.0.1', '192.168.1.1']
        self.assertEqual(assert_list, ip_list)

    def test_parse_config(self):
        my_parser = MyParser()
        test_dict: dict[str, str] = my_parser.parse_config(input_file='test_MyParser/test_parser_config.cfg')
        assert_dict: dict[str, str] = {'geoIPUsername': 'user',
                                       'geoIPApiKey': 'key',
                                       'localDatabasePassword': '1234'}
        self.assertEqual(assert_dict, test_dict)

    def test_parse_ip_file_ipv4(self):
        my_parser = MyParser()
        test_ip_list: list[str] = my_parser.parse_ip_file('./test_MyParser/test_parser_ip_list.txt')
        assert_list: list[str] = ['10.0.0.1', '1.2.3.4', '8.8.8.8']
        self.assertEqual(assert_list, test_ip_list)
