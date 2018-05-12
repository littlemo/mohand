#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>
"""
此脚本用于更新基于Git的版本说明文件，需在 ``.git/hooks``
中添加相关钩子，并在其中执行本脚本。建议使用 ``post-commit`` 钩子
"""
import os
import sys
import subprocess


version_content = """{name} ({code})"""

# 获取版本名
cmd_version_name = 'git describe --tags --always'
out, err = subprocess.Popen(
    cmd_version_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    shell=True).communicate()
if len(err) != 0:
    print('获取<版本名>失败: {}'.format(err))
    sys.exit(1)
version_name = out.decode().strip()

# 获取版本号
cmd_version_name = "git rev-list HEAD | wc -l | awk '{print $1}'"
out, err = subprocess.Popen(
    cmd_version_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    shell=True).communicate()
if len(err) != 0:
    print('获取<版本号>失败: {}'.format(err))
    sys.exit(1)
version_code = out.decode().strip()

# 生成version文件
print('> Current Soft VersionName is [{name}], VersionCode is [{code}]'.format(
    name=version_name,
    code=version_code))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'mohand', 'VERSION'), 'w') as f:
    f.write(version_content.format(
        name=version_name,
        code=version_code))
    print('> Update VERSION ... finish!')
