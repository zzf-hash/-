#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试访问 mynews 首页"""

import urllib.request
import time

time.sleep(2)
try:
    response = urllib.request.urlopen('http://127.0.0.1:5001')
    html = response.read().decode('utf-8')
    print(f"✓ 首页访问成功，状态码: {response.status}")
    print(f"\n页面内容（前 500 字符）：\n{html[:500]}\n")
except Exception as e:
    print(f"✗ 访问失败: {e}")
