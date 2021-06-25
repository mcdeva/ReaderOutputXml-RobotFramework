# ReaderOutputXml-RobotFramework

This library is a reader output xml from robotframework.
- convert xml to dictionary (by structure robotframework output)

###### I have made this for publishing a package to PyPI only!

## Usage
Install package by using pip:
```bash
pip install ReadOutputXml-RobotFramework
```

## Example
- Read output xml to dictionary.
```python
from ReaderOutputXmlRobotFramework.ReaderRobotFramework import ReaderRobotFramework

PATH_OUTPUT_XML: str = r'D:\Robot\All_Output.xml'

reader = ReaderRobotFramework(PATH_OUTPUT_XML, '/suite')
robot_result: dict = reader.read_output_xml_file_to_dict()
print(robot_result)
```
- Get testsuite name from output xml.
```python
testsuite_name: str = reader.get_testsuite_name()
print(testsuite_name)
```
- Get source file from output xml.
```python
source_file: str = reader.get_source_file()
print(source_file)
```

## Structure Json (output xml to dictionary)
- Support structure output xml. (suite xpath <= 2 levels)
```output.xml
<?xml version="1.0" encoding="UTF-8"?>
<robot generator="Rebot 4.0 (Python 3.8.3 on darwin)" generated="20210625 16:19:04.596" rpa="false" schemaversion="2">
<suite id="s1" name="Automate Test">
<suite id="s1-s1" name="Example Project1" source="/documents/path/robot/file.robot">...</suite>
<suite id="s1-s2" name="Example Project2" source="/documents/path/robot/file2.robot">...</suite>
...
</robot>
```
- define _main_suite_xpath_ for set level xpath to get name project.
```python
reader = ReaderRobotFramework(PATH_OUTPUT_XML, './suite/suite')
```
### Example Json Result
```json
{
  "Example Project1": {
    "SourceFile": "/documents/path/robot/file1.robot",
    "TestcaseDetail": [{
      "testcase_name": "name test1",
      "documentation": "documentation",
      "tags": "tag1, tag2",
      "step_keyword": "1. keyword1\n2. keyword2",
      "test_result": "PASS",
      "keyword_fail": "",
      "date_time": object_datetime,
      "msg_error": ""
    }]
  },
  "Example Project2": {
    "SourceFile": "/documents/path/robot/file2.robot",
    "TestcaseDetail": [{
      "testcase_name": "name test2",
      "documentation": "documentation",
      "tags": "tag1",
      "step_keyword": "1. keyword1",
      "test_result": "FAIL",
      "keyword_fail": "keyword2",
      "date_time": object_datetime,
      "msg_error": "cannot execute keyword2"
    }]
  }
}
```

## Uninstall package
```bash
pip uninstall ReadOutputXml-RobotFramework
```
