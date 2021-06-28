import xml.etree.ElementTree as ET
import re
from datetime import datetime
from typing import TypedDict

KEYWORD_REGEX_IGNORE: list = []


class TestcaseDetailDict(TypedDict):
    testcase_name: str
    documentation: str
    tags: str
    step_keyword: str
    test_result: str
    keyword_fail: str
    date_time: str
    msg_error: str


class ReaderRobotFramework:
    def __init__(self, xml_file, main_suite_xpath):
        self.xml_file: str = f'{xml_file}'
        self.main_suite_xpath: str = main_suite_xpath
        self.keyword_ignore: list = KEYWORD_REGEX_IGNORE
        self.robot_output: dict = self.convert_xml_file_to_dict()

    def set_keyword_ignore_error(self, keyword_regex_ignore: list):
        self.keyword_ignore = keyword_regex_ignore

    def convert_xml_file_to_dict(self) -> dict:
        project_dict: dict = {}
        root = ET.parse(self.xml_file).getroot()

        for testsuite in root.findall(self.main_suite_xpath):
            testsuite_name = testsuite.get('name')
            detail_project: dict = {}
            source_file = testsuite.get('source')
            detail_project['SourceFile'] = source_file

            # check tag testsuite has attribute name only
            if testsuite_name:
                suite_testcase = []
                for testcase in testsuite.findall('./test'):
                    # check tag test has value only
                    if testcase:
                        # binding testcase detail
                        testcase_detail = self.get_element_testcase(testcase, self.keyword_ignore)
                        suite_testcase.append(testcase_detail)

                detail_project['TestcaseDetail'] = suite_testcase
            project_dict[testsuite_name] = detail_project
        return project_dict

    @staticmethod
    def get_element_testcase(element_testcase, keyword_regex_ignore: list) -> dict:
        testcase_name = element_testcase.get('name')
        doc: str = ''
        tags: str = ''
        multi_tag: list = []
        test_steps: str = ''
        step: int = 1
        test_result: str = ''
        keyword_fail: str = ''
        date_time_format: str = ''
        msg_error: str = ''
        for detail in element_testcase:
            if detail.tag == 'kw':
                keyword = detail
                keyword_name = keyword.get('name')
                # check ignore keyword from keyword_regex_ignore variable (skip keyword in keyword_regex_ignore list)
                ignore_keyword: bool = False
                if keyword_regex_ignore is not None:
                    for keyword_ignore in keyword_regex_ignore:
                        keyword_match = re.search(keyword_ignore, keyword_name)
                        if keyword_match:
                            ignore_keyword = True
                if ignore_keyword:
                    continue

                for status in keyword.findall('./status'):
                    status_keyword = status.get('status')
                    if status_keyword == 'FAIL' and keyword_fail == '':
                        keyword_fail = keyword_name

                # set new line for concat string
                if test_steps:
                    test_steps += '\n'
                test_steps += f'{step}. {keyword_name}'
                step += 1

            if detail.tag == 'doc':
                doc = detail.text

            # set tag into multi_tag
            if detail.tag == 'tag':
                multi_tag.append(detail.text)

            if detail.tag == 'status':
                status = detail
                test_result = status.get('status')
                date_time = datetime.strptime(status.get('starttime'), '%Y%m%d %H:%M:%S.%f')
                date_time_format = f'{date_time:%Y%m%d %X.%f}'
                date_time_format = date_time_format[:-3]
                if status.text:
                    msg_error = status.text

        # concat ', ' between each tag
        tags = ', '.join(multi_tag)

        # bind data to testcase_detail_dict for return dictionary
        testcase_detail_dict: TestcaseDetailDict = \
            TestcaseDetailDict(testcase_name=testcase_name,
                               documentation=doc,
                               tags=tags,
                               step_keyword=test_steps,
                               test_result=test_result,
                               keyword_fail=keyword_fail,
                               date_time=date_time_format,
                               msg_error=msg_error)
        return testcase_detail_dict

    def read_output_xml_file_to_dict(self):
        return self.robot_output

    def get_testsuite_name(self):
        return self.robot_output['ProjectName']

    def get_source_file(self):
        return self.robot_output['SourceFile']
