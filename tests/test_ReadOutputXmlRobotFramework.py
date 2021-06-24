from unittest import TestCase
from datetime import datetime
from .. import ReadOutputXmlRobotFramework as ReaderXml

functional_test_xml_file_test: str = 'D:\\MySpace\\Code\\ScriptTools\\TDDPython\\' \
                                     'FunctionalTest20210205.xml'
functional_test_xml_no_testcase_name_test: str = 'D:\\MySpace\\Code\\ScriptTools\\TDDPython\\' \
                                                 'FunctionalTest20210205_no_testcase_name.xml'
iot_sacf_xml_file_test: str = 'D:\\MySpace\\Code\\ScriptTools\\TDDPython\\' \
                              'IOT_SACF20210211.xml'
merge_all_output_xml_file_test: str = 'D:\\MySpace\\Code\\ScriptTools\\TDDPython\\All_Output20210210.xml'
smoke_test_output_xml_file_test: str = 'D:\\MySpace\\Code\\ScriptTools\\TDDPython\\' \
                                       'All_Output_Smoke_Test20210303.xml'
status_code_exit_program: int = 1


class TestReadOutputXml(TestCase):
    def setUp(self):
        self.reader_xml = ReaderXml.ReadOutputXmlRobotFramework(functional_test_xml_file_test)

    def test_get_testsuite_name_on_one_level(self):
        expect_suite_name = 'ADMD V3.2 Functional Test'
        suite_name = self.reader_xml.get_testsuite_name_from_output_xml_file('./suite')
        self.assertEqual(expect_suite_name, suite_name)

    def test_get_testsuite_name_without_suite_xpath(self):
        expect_suite_name = ''
        suite_name = self.reader_xml.get_testsuite_name_from_output_xml_file('')
        self.assertEqual(expect_suite_name, suite_name)

    def test_get_testsuite_name_on_two_level(self):
        expect_suite_name = ''
        suite_name = self.reader_xml.get_testsuite_name_from_output_xml_file('./suite/suite')
        self.assertEqual(expect_suite_name, suite_name)

    def test_get_testsuite_name_with_file_not_exist(self):
        self.reader_xml.xml_file = ''
        with self.assertRaises(SystemExit) as system_read_file:
            self.reader_xml.get_testsuite_name_from_output_xml_file('./suite')
        self.assertEqual(status_code_exit_program, system_read_file.exception.code)

    def test_get_source_file_from_output_xml_file(self):
        expect_project_with_source = {
            'ADMD V1 B2B Relay42': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/andromeda/Relay42/TestSuites/ADMD_V1_B2B_Relay42.robot',
            'ADMD V3.1 LearnDi': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/LearnDi/TestSuites/ADMD_V3.1_LearnDi.robot',
            'ADMD V3.1 Singularity': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/Singularity/TestSuites/ADMD_V3.1_Singularity.robot',
            'ADMD V3.2 CloudGame': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/CloudGame/TestSuites/ADMD_V3.2_CloudGame.robot',
            'ADMD V3.2 LGUPlus': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/LGUPlus/TestSuites/ADMD_V3.2_LGUPlus.robot',
            'ADMD V3.2 Functional Test Iot': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/andromeda/AndromedaV3.2 FunctionalTest/TestSuites/ADMD_V3.2_Functional_Test.robot',
            'ADMD V3 B2B SiamPiwat': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/siampiwat_API/TestSuites/ADMD_V3_B2B_SiamPiwat.robot',
            'ADMD V3 B2C PICO': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/andromeda/PICO/TestSuites/ADMD_V3_B2C_PICO.robot',
            'ADMD V3 B2C SiamPiwat': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/siampiwat_API/TestSuites/ADMD_V3_B2C_SiamPiwat.robot',
            'Apollo': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/Apollo/TestSuites/Apollo.robot',
            'IOT SACF': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/SACF/TestSuites/IOT_SACF.robot',
            'SPW MobileBE ReEn': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/SiamPiwat_MobileBE-Re-En/TestSuites/SPW_MobileBE_ReEn.robot',
            'Triangular PCWebCrossPCWeb': '/Users/atcharakanlueang/Documents/IOT_AUTOMATED_SMOKE_TEST/triangular/Triangulum_Web/Triangular_PCWebCrossPCWeb.robot'
        }
        self.reader_xml.xml_file = smoke_test_output_xml_file_test
        project_with_source = self.reader_xml.get_source_file_from_output_xml_file('./suite/suite')
        self.assertEqual(expect_project_with_source, project_with_source)

    def test_get_source_file_from_output_xml_file_with_suite_xpath_1_level(self):
        expect_project_with_source = {'iot-Automated': None}
        self.reader_xml.xml_file = smoke_test_output_xml_file_test
        project_with_source = self.reader_xml.get_source_file_from_output_xml_file('./suite')
        self.assertEqual(expect_project_with_source, project_with_source)

    def test_get_testcase_detail_with_suite_to_dict(self):
        """
        insert ด้วยไฟล์ output xml (test ด้วย FunctionalTest20210205.xml)
        :return: เป็น dictionary (key = ชื่อ project, value = list ของ value -> value เป็น dict แต่ละตัวจะเท่ากับ แต่ละ testcase
        """
        expect_project_dict = {
            'ADMD V3.2 Functional Test': [{
                'testcase_id': 'TST_F10_1_1_006',
                'testcase_name': 'verify validate success - login msisdn by grant type = password',
                'document': '',
                'tags': 'Validate token',
                'step_keyword': '1. Send Request To Request OTP',
                'test_result': 'FAIL',
                'keyword_fail': 'Send Request To Request OTP',
                'date_time': datetime(2021, 2, 4, 14, 27, 54, 867000),
                'msg_error': "ReadTimeout: HTTPSConnectionPool(host='iot-apivr.ais.co.th', port=443): "
                             "Read timed out. (read timeout=20.0)"}]}
        self.reader_xml.xml_file = functional_test_xml_file_test
        project_dict = self.reader_xml.get_testcase_detail_with_suite_to_dict('./suite')
        self.assertEqual(expect_project_dict, project_dict)

    def test_get_testcase_detail_with_suite_to_dict_ignore_keyword_match(self):
        """
        insert ด้วยไฟล์ output xml (test ด้วย FunctionalTest20210205.xml)
        :return: เป็น dictionary (key = ชื่อ project, value = list ของ value -> value เป็น dict แต่ละตัวจะเท่ากับ แต่ละ testcase
        """
        expect_project_dict = {
            'ADMD V3.2 Functional Test': [{
                'testcase_id': 'TST_F10_1_1_006',
                'testcase_name': 'verify validate success - login msisdn by grant type = password',
                'document': '',
                'tags': 'Validate token',
                'step_keyword': '',
                'test_result': 'FAIL',
                'keyword_fail': '',
                'date_time': datetime(2021, 2, 4, 14, 27, 54, 867000),
                'msg_error': "ReadTimeout: HTTPSConnectionPool(host='iot-apivr.ais.co.th', port=443): "
                             "Read timed out. (read timeout=20.0)"}]}
        self.reader_xml.xml_file = functional_test_xml_file_test
        keyword_regex_ignore_list: list = ['.*Send Request To Request OTP.*']
        project_dict = self.reader_xml.get_testcase_detail_with_suite_to_dict('./suite', keyword_regex_ignore_list)
        self.assertEqual(expect_project_dict, project_dict)

    def test_get_testcase_detail_with_suite_to_dict_ignore_keyword_no_match(self):
        """
        insert ด้วยไฟล์ output xml (test ด้วย FunctionalTest20210205.xml)
        :return: เป็น dictionary (key = ชื่อ project, value = list ของ value -> value เป็น dict แต่ละตัวจะเท่ากับ แต่ละ testcase
        """
        expect_project_dict = {
            'ADMD V3.2 Functional Test': [{
                'testcase_id': 'TST_F10_1_1_006',
                'testcase_name': 'verify validate success - login msisdn by grant type = password',
                'document': '',
                'tags': 'Validate token',
                'step_keyword': '1. Send Request To Request OTP',
                'test_result': 'FAIL',
                'keyword_fail': 'Send Request To Request OTP',
                'date_time': datetime(2021, 2, 4, 14, 27, 54, 867000),
                'msg_error': "ReadTimeout: HTTPSConnectionPool(host='iot-apivr.ais.co.th', port=443): "
                             "Read timed out. (read timeout=20.0)"}]}
        self.reader_xml.xml_file = functional_test_xml_file_test
        keyword_regex_ignore_list: list = ['.*Run Keyword And Ignore Error.*']
        project_dict = self.reader_xml.get_testcase_detail_with_suite_to_dict('./suite', keyword_regex_ignore_list)
        self.assertEqual(expect_project_dict, project_dict)

    def test_get_testcase_detail_with_suite_to_dict_without_testcase_name(self):
        """
        insert ด้วยไฟล์ output xml (test ด้วย FunctionalTest20210205_no_testcase_name.xml)
        :return: เป็น dictionary (key = ชื่อ project, value = list ของ value -> value เป็น dict แต่ละตัวจะเท่ากับ แต่ละ testcase
        """
        expect_project_dict = {
            'ADMD V3.2 Functional Test': [{
                'testcase_id': 'TST_F10_1_1_006',
                'testcase_name': '',
                'document': 'Test document',
                'tags': 'Validate token',
                'step_keyword': '1. Send Request To Request OTP',
                'test_result': 'FAIL',
                'keyword_fail': 'Send Request To Request OTP',
                'date_time': datetime(2021, 2, 4, 14, 27, 54, 867000),
                'msg_error': "ReadTimeout: HTTPSConnectionPool(host='iot-apivr.ais.co.th', port=443): "
                             "Read timed out. (read timeout=20.0)"}]}
        self.reader_xml.xml_file = functional_test_xml_no_testcase_name_test
        project_dict = self.reader_xml.get_testcase_detail_with_suite_to_dict('./suite')
        self.assertEqual(expect_project_dict, project_dict)

    def test_get_testcase_detail_with_suite_to_dict_without_document(self):
        """
        insert ด้วยไฟล์ output xml (test ด้วย FunctionalTest20210205.xml)
        :return: เป็น dictionary (key = ชื่อ project, value = list ของ value -> value เป็น dict แต่ละตัวจะเท่ากับ แต่ละ testcase
        """
        expect_project_dict = {
            'ADMD V3.2 Functional Test': [{
                'testcase_id': 'TST_F10_1_1_006',
                'testcase_name': 'verify validate success - login msisdn by grant type = password',
                'document': '',
                'tags': 'Validate token',
                'step_keyword': '1. Send Request To Request OTP',
                'test_result': 'FAIL',
                'keyword_fail': 'Send Request To Request OTP',
                'date_time': datetime(2021, 2, 4, 14, 27, 54, 867000),
                'msg_error': "ReadTimeout: HTTPSConnectionPool(host='iot-apivr.ais.co.th', port=443): "
                             "Read timed out. (read timeout=20.0)"}]}
        self.reader_xml.xml_file = functional_test_xml_file_test
        project_dict = self.reader_xml.get_testcase_detail_with_suite_to_dict('./suite')
        self.assertEqual(expect_project_dict, project_dict)

    def test_get_testcase_detail_with_suite_to_dict_without_msg_error(self):
        """
        insert ด้วยไฟล์ output xml (test ด้วย IOT_SACF20210211.xml)
        :return: เป็น dictionary (key = ชื่อ project, value = list ของ value -> value เป็น dict แต่ละตัวจะเท่ากับ แต่ละ testcase
        """
        expect_project_dict = {
            'IOT SACF': [{
                'testcase_id': 'TST_F1_1_1_001',
                'testcase_name': 'authen loginByB2B cmd (loginByB2Bjson) port 15400',
                'document': 'Post Request: https://apipg.ais.co.th:15400/v1/loginByB2B.json\n'
                            'Request Headers: {"x-appEnvironmentType": "partner_iot", '
                            '"Content-Type": "application/json"}\n'
                            'Request Body: {"clientId": '
                            '"K5dwgpOrFkmBUD8IOxYZRO0HNSI7VuX/AAYnJh7hpWk=", "timeStamp": '
                            '"1613032711000", "serverId": "NBADL1711009", "signature": '
                            '"code_signature"}',
                'tags': 'Login, SmokeTest',
                'step_keyword': '1. Generate SACF Signature\n'
                                '2. Login B2B By URL\n'
                                '3. Run Keyword And Ignore Error',
                'test_result': 'PASS',
                'keyword_fail': '',
                'date_time': datetime(2021, 2, 11, 15, 37, 31, 222000),
                'msg_error': ''}]}
        self.reader_xml.xml_file = iot_sacf_xml_file_test
        project_dict = self.reader_xml.get_testcase_detail_with_suite_to_dict('./suite')
        self.assertEqual(expect_project_dict, project_dict)

    def test_get_testcase_detail_with_suite_to_dict_from_smoke_test_output_xml(self):
        """
        insert ด้วยไฟล์ output xml (test ด้วย All_Output_Smoke_Test20210303.xml)
        :return: เป็น dictionary (key = ชื่อ project, value = list ของ value -> value เป็น dict แต่ละตัวจะเท่ากับ แต่ละ testcase
        """
        expect_project_dict = {
            'ADMD V1 B2B Relay42': [
                {'testcase_id': 'TST_F1_1_1_001', 'testcase_name': 'User login to send SMS success', 'document': '',
                 'tags': 'ADMD V1 B2B Relay42: User login to send SMS success, SmokeTest',
                 'step_keyword': '1. Login on Relay42\n2. Send SMS on Relay42\n3. Check Get and Export SSH Log from Relay42',
                 'test_result': 'PASS', 'keyword_fail': '', 'date_time': datetime(2021, 3, 2, 15, 59, 6, 590000), 'msg_error': ''}],
            'ADMD V3.1 LearnDi': [{'testcase_id': 'TST_F1_1_1_003',
                                   'testcase_name': 'To verify LearnDi partner (30172) registers with email SMTP Server of CSLoxinfo, Register to get access token',
                                   'document': 'API: {"publicId": "ldi:jennifercrawford@gmail.com", "deleteAllAlias": "yes"}\n\nBody: {"publicId": "ldi:jennifercrawford@gmail.com", "deleteAllAlias": "yes"}',
                                   'tags': 'Register, SmokeTest',
                                   'step_keyword': '1. Open Learn Di Website and Register\n2. Connect to ADMD-SRFP and Activate URL\n3. Send Request to Get Token by URL\n4. Verify Register Success From API Search Sub\n5. Delete Sub Register\n6. Run Keyword And Ignore Error',
                                   'test_result': 'PASS', 'keyword_fail': '', 'date_time': datetime(2021, 3, 2, 15, 59, 6, 799000),
                                   'msg_error': ''}],
            'ADMD V3.1 Singularity': [{'testcase_id': 'TST_F1_1_1_001',
                                       'testcase_name': 'Verify Partnermanagement (30122) used identity Credential Level 2 & IDP Group = pnm to register',
                                       'document': 'Authorization: https://iot-apiv3.ais.co.th/auth/v3.1/oauth/authorize?response_type=code&client_id=TxjbTTY7JQhJjrzxG8z0h%2FnDt1qEU%2FxXSyXOwzJeHBCcNEc%2BSp%2Bjeg%3D%3D&scope=profile&redirect_uri=https://www.ais.co.th/\n First Name: Matthew\n last Name: Weber\n Email: jeremy73@gmail.com\n Password: passWord@1234\n',
                                       'tags': 'Register, SmokeTest',
                                       'step_keyword': '1. Open Singularity Website\n2. Register an New Account with Email AIS Partner Management\n3. Create an Username and Password AIS Partner Management\n4. Confirm the Registration by Activation Link\n5. Run Keyword And Ignore Error',
                                       'test_result': 'FAIL', 'keyword_fail': 'Confirm the Registration by Activation Link', 'date_time': datetime(2021, 3, 2, 15, 59, 26, 670000),
                                       'msg_error': "No match found for '$' in 3 seconds\nOutput:\nLast login: Tue Mar  2 14:36:06 2021 from 10.239.89.123\n\nThis computer system is property of Advanced Info Service Public Company Limited (AIS) and\nmust be accessed only by authorized users. Any unauthorized use of this system is strictly prohibited\nand deemed as violation to AIS'\xads regulation on Information Technology and Computer System\nSecurity of Telecommunication and Wireless Business (Regulation). The unauthorized user or any\nperson who breaches AIS'\xads Regulation, policy, criteria and/or memorandums regarding IT Security\nwill be punished by AIS and may be subject to criminal prosecution.\nAll data contained within the systems is owned by AIS. The data may be monitored, intercepted,\nrecorded, read, copied, or captured and disclosed in any manner by authorized personnel for\nprosecutions and other purposes according to AIS's Regulation.\nAny communication on or information stored within the system, including information stored locally\non the hard drive or other media in use with this unit (e.g., floppy disks, PDAs and other hand-held\nperipherals, Handy drives, CD-ROMs, etc.), is also owned by AIS. AIS have all rights to manage such\ninformation.\nPlease contact IT Support if you encounter any computer problem.\n."}],
            'ADMD V3.2 CloudGame': [{'testcase_id': 'TST_F1_1_1_001', 'testcase_name': 'Login B2B Client Credential',
                                     'document': '\nLoginB2B POST Request: https://iot-apivr.ais.co.th/auth/v3.1/oauth/token \nRequest Headers: {"Content-Type": "application/x-www-form-urlencoded"} \nRequest Body: {"client_id": "skZHmM4IPAGBUD8IOxYZRO0HNSI7VuX/aVThDpTFLbI=", "grant_type": "client_credentials", "client_secret": "004798a82375640fc2f4f8356828c13e"}',
                                     'tags': 'Authentication, SmokeTest',
                                     'step_keyword': '1. Set Library Search Order\n2. Login Authentication Cloud Game B2B',
                                     'test_result': 'PASS', 'keyword_fail': '', 'date_time': datetime(2021, 3, 2, 15, 59, 26, 603000),
                                     'msg_error': ''}],
            'ADMD V3.2 LGUPlus': [
                {'testcase_id': 'TST_F1_1_1_001', 'testcase_name': 'Login AR with OTP', 'document': '',
                 'tags': 'Login OTP, SmokeTest',
                 'step_keyword': '1. Open ARUPLUS website\n2. Fill Mobile No to Request OTP\n3. Input OTP and Login\n4. Close All Browsers',
                 'test_result': 'FAIL', 'keyword_fail': 'Input OTP and Login', 'date_time': datetime(2021, 3, 2, 15, 59, 25, 372000),
                 'msg_error': 'OTP not found in /Singularity/5G/logs/admd-v3-2/detail/\nNonce: LGUPlus20210302155925'}],
            'ADMD V3.2 Functional Test Iot': [{'testcase_id': 'TST_F12_1_1_001',
                                               'testcase_name': 'Generate ClientId PartnerId 5 digit snackcase format',
                                               'document': '-app_name:fivedigit\n-partner_id:01234',
                                               'tags': 'GenerateClientId, SmokeTest, snackcase',
                                               'step_keyword': '1. Send Request to Generate ClientId\n2. Run Keyword And Ignore Error',
                                               'test_result': 'PASS', 'keyword_fail': '',
                                               'date_time': datetime(2021, 3, 2, 15, 59, 7, 657000), 'msg_error': ''}],
            'ADMD V3 B2B SiamPiwat': [
                {'testcase_id': 'TST_F1_1_1_001', 'testcase_name': 'Verify First Get Request', 'document': '',
                 'tags': 'SmokeTest', 'step_keyword': '1. Send Request to First Get Request and Verify Success',
                 'test_result': 'PASS', 'keyword_fail': '', 'date_time': datetime(2021, 3, 2, 15, 58, 6, 492000), 'msg_error': ''}],
            'ADMD V3 B2C PICO': [
                {'testcase_id': 'TST_F1_1_1_001', 'testcase_name': 'User auto login to purchase app and charge success',
                 'document': 'Phone number was provided in this testcase:\nAuto Login with 66932019875 phone number \nGET Request: https://iot-apivr.ais.co.th/auth/v3.2/oauth/authorize?response_type=code&client_id=2h2VPdd6lB%2BkQ3xTqRQTMiltoB3sv9Ia7oTPgwM7oUU%3D&scope=profile&redirect_uri=https%3A%2F%2Fwww.ais.co.th%2F&state=poc0000003&nonce=ROBOT-API-T110630 \nRequest Headers: {"x-msisdn": "66932019875"} \nGET Request: https://iot-apivr.ais.co.th/auth/v3.2/oauth/token?client_id=2h2VPdd6lB%2BkQ3xTqRQTMiltoB3sv9Ia7oTPgwM7oUU%3D&client_secret=clientSecret&grant_type=authorization_code&redirect_uri=https%3A%2F%2Fwww.ais.co.th%2F&code=W23Uv2uCBW7q3fxda226XmtaUKqa1LiP46X9hs3X2H9P',
                 'tags': 'ADMD V3 B2C PICO: Auto login to purchase app and charge success, SmokeTest',
                 'step_keyword': '1. Login Auto\n2. Check Get and Export SSH Log from PICO Login\n3. Send Request Send One Time Password\n4. Send Request Confirm One Time Password\n5. Send Reserve And Charge Request\n6. Check Get and Export SSH Log from PICO',
                 'test_result': 'PASS', 'keyword_fail': '', 'date_time': datetime(2021, 3, 2, 15, 59, 7, 191000), 'msg_error': ''}],
            'ADMD V3 B2C SiamPiwat': [
                {'testcase_id': 'TST_F1_1_1_001', 'testcase_name': 'Verify Login Facebook Success', 'document': '',
                 'tags': 'Login_Social, SmokeTest', 'step_keyword': '1. Open SiamPiwat Web\n2. Login with Facebook',
                 'test_result': 'PASS', 'keyword_fail': '', 'date_time': datetime(2021, 3, 2, 15, 58, 8, 411000), 'msg_error': ''}],
            'Apollo': [{'testcase_id': 'TST_F1_1_1_001', 'testcase_name': 'Verify GET Enterprise',
                        'document': 'GET Request: https://10.137.30.22:32323/api/v1/apollo/enterprises/\n Request Headers: {"X-Tid": "1201307enterprise1670873"}\n',
                        'tags': 'Enterprise, SmokeTest',
                        'step_keyword': '1. Get Request For Apollo Enterprise\n2. Check If Result Code And Developer Message Is Return As Expected\n3. Run Keyword And Ignore Error',
                        'test_result': 'PASS', 'keyword_fail': '', 'date_time': datetime(2021, 3, 2, 15, 59, 25, 341000), 'msg_error': ''}],
            'IOT SACF': [
                {'testcase_id': 'TST_F1_1_1_001', 'testcase_name': 'authen loginByB2B cmd (loginByB2Bjson) port 15400',
                 'document': '\nPost Request: https://apipg.ais.co.th:15400/v1/loginByB2B.json \nRequest Headers: {"x-appEnvironmentType": "partner_iot", "Content-Type": "application/json"} \nRequest Body: {"clientId": "K5dwgpOrFkmBUD8IOxYZRO0HNSI7VuX/AAYnJh7hpWk=", "timeStamp": "1614675625000", "serverId": "NBADL1711009", "signature": "sHmhd+tF0CBhhIyZEMCyMSkP2+K/jqahiVVnvTQDz8cvmM6zxyybS+nz4Inw3aqVnkkmDq768ZwJUlwU83JyBqMJ+T5LbBEp0AORLUKspBUzuty8TAfTJZ4kKP0pAG+6ax1C+TPDS/Wk3zF6xGsia2f+Aa66Dt8hCrUIR4WW4FkyrbKj4AbmLtul/oEO5OyWf4Lj0/7laAOJrNN0769fILZkykXNVKAWJHsEJPQe5v0depEfyDxZvgwLZ4ZRblxHnmjZrqAJUFhYbcDsB7U4eAn4cO5eU17fOQdeSGXrKPyKJwKNH3lSUlxuHL6Pnl9obtTLZ/lKHENyw1/zyNmiRA=="}',
                 'tags': 'Login, SmokeTest',
                 'step_keyword': '1. Generate SACF Signature\n2. Login B2B By URL\n3. Run Keyword And Ignore Error',
                 'test_result': 'PASS', 'keyword_fail': '', 'date_time': datetime(2021, 3, 2, 15, 59, 25, 373000), 'msg_error': ''}],
            'SPW MobileBE ReEn': [
                {'testcase_id': 'TST_F1_1_1_001', 'testcase_name': 'Verify API Get Privilege Dynamic Success',
                 'document': '', 'tags': 'Privilege, SmokeTest',
                 'step_keyword': '1. Send Request to Get Privilege Dynamic and Verify Success\n2. Check Get and Export SSH Log from Siam Piwat API',
                 'test_result': 'PASS', 'keyword_fail': '', 'date_time': datetime(2021, 3, 2, 15, 58, 8, 536000), 'msg_error': ''}],
            'Triangular PCWebCrossPCWeb': [
                {'testcase_id': 'TST_F2_1_1_001', 'testcase_name': 'verify A voice call to B but A press hang up',
                 'document': 'Accounts were provided in this test case:\n1. User A: Email: testtriangular4@gmail.com\nPassword: 1234\n2. User B: Email: testtriangular5@gmail.com\nPassword: 1234',
                 'tags': 'SmokeTest, Triangular PCWebCrossPCWeb: [PC] A: Firefox Call B: Firefox',
                 'step_keyword': '1. Open Firefox With Device Camera and Mic\n2. A User Login On Triangulum Web\n3. Run Keyword And Ignore Error',
                 'test_result': 'FAIL', 'keyword_fail': 'A User Login On Triangulum Web', 'date_time': datetime(2021, 3, 2, 15, 56, 14, 49000),
                 'msg_error': "Element with locator 'id=swal2-title' not found."}]
        }
        self.reader_xml.xml_file = smoke_test_output_xml_file_test
        project_dict = self.reader_xml.get_testcase_detail_with_suite_to_dict('./suite/suite')
        self.assertEqual(expect_project_dict, project_dict)

    def test_get_testcase_detail_with_suite_to_dict_with_suite_xpath_1_level(self):
        """
        insert ด้วยไฟล์ output xml (test ด้วย All_Output20210210.xml)
        :return: เป็น dictionary (key = ชื่อ project, value = list ของ value -> value เป็น dict แต่ละตัวจะเท่ากับ แต่ละ testcase
        """
        expect_project_dict = {'iot-Automated': []}
        self.reader_xml.xml_file = merge_all_output_xml_file_test
        project_dict = self.reader_xml.get_testcase_detail_with_suite_to_dict('./suite')
        self.assertEqual(expect_project_dict, project_dict)
