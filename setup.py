# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DingTalkBot",
    version="0.0.1",
    author="maida",
    author_email="maida6244@gmail.com",
    description="钉钉群聊天机器人",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LZC6244/DingTalkBot",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
