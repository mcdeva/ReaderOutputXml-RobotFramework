import os
from datetime import datetime, timedelta
from typing import TypedDict
from ReaderRobotFramework import ReaderRobotFramework

PATH_OUTPUT_XML: str = r'C:\Users\mcdev\Downloads\All_Output.xml'


class TestCaseDetailLog(TypedDict):
    testcase_name: str
    test_result: str
    msg_error: str
    full_msg_error_robot: str
    script_robot_rerun: str


class AnalyzeErrorLog:
    def read_output_xml(self, path_output_xml, main_suite_xpath):
        reader = ReaderRobotFramework(path_output_xml, main_suite_xpath)
        reader.read_output_xml_file_to_dict()
        reader.get_testsuite_name()
        reader.get_source_file()


def main():
    analyzer = AnalyzeErrorLog()
    analyzer.read_output_xml(PATH_OUTPUT_XML, './suite')


if __name__ == '__main__':
    main()
