#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'pengyao'
SITENAME = u"PengYao's Weblog"
SITEURL = 'http://pengyao.org'

TIMEZONE = 'Asia/Taipei'


DEFAULT_LANG = u'zh'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_DATE = (2013,01,01,01,01,01)

FILES_TO_COPY = (('extra/favicon.ico', 'favicon.ico'),
                 ('extra/CNAME', 'CNAME'),
                 ('extra/README', 'README'),)

MD_EXTENSIONS = ['codehilite', 'extra', 'toc', 'tables']
OUTPUT_PATH = 'output/'
STATIC_PATHS = ['images', 'extra']

THEME = 'themes/tuxlite_tbs'

# Blogroll
LINKS =  ((u'SaltStack中文社区', 'http://saltstack.cn/'),)

# Social widget
SOCIAL = (('Github', 'https://github.com/pengyao'),
          ('Weibo', 'http://weibo.com/yaoxuanwei'),)

GITHUB_URL = "https://github.com/pengyao"
DISQUS_SITENAME = "pengyao-blog"
BAIDU_TONGJI = "87206c0d4319a1f476378557aa7c50ca"

DEFAULT_PAGINATION = 10
SUMMARY_MAXLENGTH = 100

