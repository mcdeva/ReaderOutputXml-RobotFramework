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
- Read output xml to dictionary
```python
from ReaderOutputXmlRobotFramework.ReaderRobotFramework import ReaderRobotFramework

PATH_OUTPUT_XML: str = r'D:\RobotAll_Output.xml'

reader = ReaderRobotFramework(PATH_OUTPUT_XML, '/suite')
robot_result: dict = reader.read_output_xml_file_to_dict()
print(robot_result)
```
- Get testsuite name from output xml
```python
testsuite_name: str = reader.get_testsuite_name()
print(testsuite_name)
```
- Get source file from output xml
```python
source_file: str = reader.get_source_file()
print(source_file)
```

## Structure Json (output xml to dictionary)
- Support structure output xml (suite xpath <= 2 levels)

```json
{
  "ProjectName": "project_name",
  "SourceFile": "/path",
  "TestcaseDetail": [{
    "testcase_name": "str",
    "documentation": "str",
    "tags": "str",
    "step_keyword": "str",
    "test_result": "str",
    "keyword_fail": "str",
    "date_time": "datetime",
    "msg_error": "str"
  }]
}
```

## Uninstall package
```bash
pip uninstall ReadOutputXml-RobotFramework
```
