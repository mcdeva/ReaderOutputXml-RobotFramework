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
```python
from ReaderOutputXmlRobotFramework.ReaderRobotFramework import ReaderRobotFramework

PATH_OUTPUT_XML: str = r'D:\RobotAll_Output.xml'

reader = ReaderRobotFramework(path_output_xml)
reader.check_exist_file_path(path_output_xml)
```

## Uninstall package
```bash
pip uninstall ReadOutputXml-RobotFramework
```