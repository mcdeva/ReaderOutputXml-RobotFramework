'''
# Deploy library #
py -m build
twine check dist/*
twine upload dist/*
'''
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ReadOutputXml-RobotFramework",
    version="0.0.5.1",
    author="Rukpong",
    author_email="aisendbox@gmail.com",
    description="Reader the output xml from structure RobotFramework output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcdeva/ReaderOutputXml-RobotFramework.git",
    license="MIT",
    packages=find_packages(),
    package_dir={'client': 'Client'},
    install_requires=[
        'requests'
    ],
    tests_require=[
        'coverage', 'wheel', 'pytest', 'requests_mock'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha"
    ]
)