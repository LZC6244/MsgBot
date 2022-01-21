# -*- coding: utf-8 -*-

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='MsgBot',
    version='0.1.2',
    author='maida',
    author_email='maida6244@gmail.com',
    description='Python 实现的一个消息通知助手。可以使用钉钉群聊天机器人或者微信。',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/LZC6244/DingTalkBot',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
