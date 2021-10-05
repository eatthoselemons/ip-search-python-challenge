from unittest import TestCase
from MyWriter import MyWriter
import os


class TestMyWriter(TestCase):
    def setUp(self) -> None:
        os.makedirs("./test_MyWriter/", exist_ok=True)

    def test_write_ip_list(self):
        assert_list: list[str] = ['10.0.0.1', '192.234.54.72']
        test_list: list[str] = []
        my_writer = MyWriter()
        my_writer.write_ip_list(assert_list, './test_MyWriter/write_ip_list.txt')
        with open ('./test_MyWriter/write_ip_list.txt') as file:
            for line in file:
                test_list.append(line.rstrip('\n'))
        self.assertEqual(assert_list, test_list)
        os.remove("./test_MyWriter/write_ip_list.txt")

    def test_write_data_list(self):
        assert_data: dict[str, str] = {'10.0.0.1': "value1",
                                       '192.234.54.72': "value2"}
        output_data: list[str] = ["10.0.0.1: locate: value1",
                                  "192.234.54.72: locate: value2"]
        read_file: list[str] = []
        my_writer = MyWriter()
        my_writer.write_data_list(assert_data, './test_MyWriter/write_data_list.txt', 'locate')
        with open ('./test_MyWriter/write_data_list.txt') as file:
            for line in file:
                read_file.append(line.rstrip('\n'))
        self.assertEqual(output_data, read_file)
        os.remove("./test_MyWriter/write_data_list.txt")

#    def tearDown(self) -> None:

