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
    date_time: datetime
    msg_error: str


class ReaderRobotFramework:
    def __init__(self, xml_file, main_suite_xpath):
        self.xml_file: str = xml_file
        self.main_suite_xpath: str = main_suite_xpath
        self.keyword_ignore: list = KEYWORD_REGEX_IGNORE
        self.robot_output: dict = self.convert_xml_file_to_dict()

    def set_keyword_ignore_error(self, keyword_regex_ignore: list):
        self.keyword_ignore = keyword_regex_ignore

    def convert_xml_file_to_dict(self) -> dict:
        project_dict = {}
        root = ET.parse(self.xml_file).getroot()

        for testsuite in root.findall(self.main_suite_xpath):
            testsuite_name = testsuite.get('name')
            project_dict['ProjectName'] = testsuite_name
            source_file = testsuite.get('source')
            project_dict['SourceFile'] = source_file

            # check tag testsuite has attribute name only
            if testsuite_name:
                suite_testcase = []
                for testcase in testsuite.findall('./test'):
                    # check tag test has value only
                    if testcase:
                        # binding testcase detail
                        testcase_detail = self.get_element_testcase(testcase, self.keyword_ignore)
                        suite_testcase.append(testcase_detail)
                project_dict['TestcaseDetail'] = suite_testcase
        return project_dict

    @staticmethod
    def get_element_testcase(element_testcase, keyword_regex_ignore: list) -> dict:
        testcase_name = element_testcase.get('name')
        doc: str = ''
        tags: str = ''
        test_steps: str = ''
        step: int = 1
        test_result: str = ''
        keyword_fail: str = ''
        date_time = ''
        msg_error: str = ''
        for detail in element_testcase:
            if detail.tag == 'kw':
                keyword = detail
                keyword_name = keyword.get('name')
                # ถ้ามีค่า ignore keyword และ ชื่อ keyword อยู่ใน list ให้ข้าม keyword นั้น ๆ
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

                # กรณีมีข้อมูลแล้ว ให้ใส่ \n เพื่อขึ้นบรรทัดใหม่
                if test_steps:
                    test_steps += '\n'
                test_steps += f'{step}. {keyword_name}'
                step += 1

            if detail.tag == 'doc':
                doc = detail.text

            # กรณีมี tag หลายตัว จะต่อข้อมูลด้วย ", "
            # if detail.tag == 'tags':
            #     tag_list: list = []
            #     for tag in detail:
            #         tag_list.append(tag.text)
            #     tags = ', '.join(tag_list)

            if detail.tag == 'tag':
                tags = detail.text

            if detail.tag == 'status':
                status = detail
                test_result = status.get('status')
                date_time = datetime.strptime(status.get('starttime'), '%Y%m%d %H:%M:%S.%f')
                if status.text:
                    msg_error = status.text

        # bind data เข้าไปใน testcase_detail_dict เตรียม return
        testcase_detail_dict: TestcaseDetailDict = \
            TestcaseDetailDict(testcase_name=testcase_name,
                               documentation=doc,
                               tags=tags,
                               step_keyword=test_steps,
                               test_result=test_result,
                               keyword_fail=keyword_fail,
                               date_time=date_time,
                               msg_error=msg_error)
        return testcase_detail_dict

    def read_output_xml_file_to_dict(self):
        return self.robot_output

    def get_testsuite_name(self):
        return self.robot_output['ProjectName']

    def get_source_file(self):
        return self.robot_output['SourceFile']
