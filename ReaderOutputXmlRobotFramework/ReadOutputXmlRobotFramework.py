import xml.etree.ElementTree as ET
from os import path
import re
from datetime import datetime
from typing import TypedDict


class TestcaseDetailDict(TypedDict):
    testcase_id: str
    testcase_name: str
    document: str
    tags: str
    step_keyword: str
    test_result: str
    keyword_fail: str
    date_time: datetime
    msg_error: str


class ReaderRobotFramework:
    def __init__(self, xml_file):
        self.xml_file: str = xml_file

    @staticmethod
    def check_exist_file_path(file):
        if not (path.exists(file)):
            print(f'[Error] File not found: \"{file}\"')
            exit(1)

    def get_testsuite_name_from_output_xml_file(self, suite_xpath: str) -> str:
        self.check_exist_file_path(self.xml_file)
        suite_name = ''
        root = ET.parse(self.xml_file).getroot()
        for testsuite in root.findall(suite_xpath):
            testsuite_name = testsuite.get('name')
            if testsuite_name:
                suite_name = testsuite_name
        return suite_name

    def get_robot_file_name_from_output_xml_file(self, suite_xpath: str) -> str:
        self.check_exist_file_path(self.xml_file)
        source_file_name = ''
        root = ET.parse(self.xml_file).getroot()
        for testsuite in root.findall(suite_xpath):
            suite_source = testsuite.get('source')
            if suite_source:
                source_file_name = suite_source

        filename = path.basename(source_file_name)
        robot_file_name = path.splitext(filename)[0]
        return robot_file_name

    def get_source_file_from_output_xml_file(self, suite_xpath: str) -> dict:
        project_with_source: dict = {}
        root = ET.parse(self.xml_file).getroot()
        for testsuite in root.findall(suite_xpath):
            testsuite_name = testsuite.get('name')
            suite_source = testsuite.get('source')
            if testsuite_name:
                project_with_source[testsuite_name] = suite_source
        return project_with_source

    def get_testcase_detail_with_suite_to_dict(self, main_suite_xpath: str, keyword_regex_ignore_list: list = None) -> dict:
        # ต้องการ output ออกมาเป็น dictionary project_dict (key = ชื่อโปรเจค, value = list ของ testcase)
        project_dict = {}
        root = ET.parse(self.xml_file).getroot()
        # กรณี file xml มี suite เดียว -> ใน 1 suite มี test case ทั้งหมด (path xml: root/suite/test)
        # ถ้ามี path มากกว่า 1 ชั้น -> ใน suite จะมี testcase (path xml: root/suite/suite/test)
        for testsuite in root.findall(main_suite_xpath):
            testsuite_name = testsuite.get('name')
            # check tag testsuite get ค่าเฉพาะตัวที่มี attribute name
            if testsuite_name:
                suite_testcase_list = []
                for testcase in testsuite.findall('./test'):
                    # check tag test เฉพาะที่มีค่าใน tag test
                    if testcase:
                        # binding ข้อมูลสำหรับ testcase detail
                        testcase_detail_dict = self.get_element_testcase(testcase, keyword_regex_ignore_list)
                        suite_testcase_list.append(testcase_detail_dict)
                project_dict[testsuite_name] = suite_testcase_list
        return project_dict

    @staticmethod
    def get_element_testcase(element_testcase, keyword_regex_ignore_list: list) -> dict:
        testcase_fullname = element_testcase.get('name')
        testcase_str = testcase_fullname.split(' ', 1)
        testcase_id: str = testcase_str[0]
        testcase_name: str = ''
        if len(testcase_str) == 2:
            testcase_name = testcase_str[1]
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
                if keyword_regex_ignore_list is not None:
                    for keyword_ignore in keyword_regex_ignore_list:
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
            if detail.tag == 'tags':
                tag_list: list = []
                for tag in detail:
                    tag_list.append(tag.text)
                tags = ', '.join(tag_list)

            if detail.tag == 'status':
                status = detail
                test_result = status.get('status')
                date_time = datetime.strptime(status.get('starttime'), '%Y%m%d %H:%M:%S.%f')
                if status.text:
                    msg_error = status.text

        # bind data เข้าไปใน testcase_detail_dict เตรียม return
        testcase_detail_dict: TestcaseDetailDict = \
            TestcaseDetailDict(testcase_id=testcase_id,
                               testcase_name=testcase_name,
                               document=doc,
                               tags=tags,
                               step_keyword=test_steps,
                               test_result=test_result,
                               keyword_fail=keyword_fail,
                               date_time=date_time,
                               msg_error=msg_error)
        return testcase_detail_dict
