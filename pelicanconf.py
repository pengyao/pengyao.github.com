#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'pengyao'
SITENAME = u"PengYao's Weblog"
SITEURL = 'http://pengyao.org'

TIMEZONE = 'Asia/Taipei'


DEFAULT_LANG = u'zh'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_DATE = (2013,01,01,01,01,01)

EXTRA_PATH_METADATA = {
  'extra/favicon.ico': {'path': 'favicon.ico'},
  'extra/CNAME': {'path': 'CNAME'},
  'extra/README': {'path': 'README'},
  'extra/images/user_logo.jpg': {'path': 'user_logo.jpg'},
}

MD_EXTENSIONS = ['codehilite', 'extra', 'toc', 'tables']
OUTPUT_PATH = 'output/'
STATIC_PATHS = ['images', 'extra']

THEME = 'themes/pelican-svbhack'
USER_LOGO_URL = SITEURL + '/user_logo.jpg'

# Blogroll
LINKS =  ((u'中国SaltStack用户组', 'http://saltstack.cn/'),
          (u'静思学吧', 'http://www.jsxubar.info/'),
          (u'HeyLinux', 'http://heylinux.com/'),
         )

# Social widget
SOCIAL = (('Github', 'https://github.com/pengyao'),
          ('Weibo', 'http://weibo.com/yaoxuanwei'),)

GITHUB_URL = "https://github.com/pengyao"
DISQUS_SITENAME = "pengyao-blog"
BAIDU_TONGJI = "87206c0d4319a1f476378557aa7c50ca"

DEFAULT_PAGINATION = 10
SUMMARY_MAXLENGTH = 100

# Donate
DONATE = True 
RIPPLE_ADDRESS = "rPzFa7133QutTTh3ci62Cx1wvHftuqUqX3"
