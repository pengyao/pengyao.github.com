Title: Zabbix绘图显示中文
Date: 2013-04-10
Author: pengyao
Slug: zabbix-frontend-graph-chinese 
Tags: zabbix, 中文
Category: Zabbix 
Summary: Zabbix前端在调整语言为中文后，绘图部分字符将以方块显示，其原因是zabbix前端自带的字体并不支持中文的缘故，解决方法是增加支持中文的字体,推荐使用文泉驿


国内的朋友喜欢在使用zabbix frontend时，将语言调整为中文，以方便使用，但调整后却发现绘图中部分字符显示为方框，其原因是因为zabbix自带的字体并不支持中文的缘故，要想正常使用，解决方法是增加中文字体.

本文假设zabbix frontend存放在*/var/lib/www/zabbix*目录下,适用版本**zabbix 2.0**

zabbix frontend自带的字体文件存放在*/var/lib/www/zabbix/fonts/*目录下，对应的文件名为*DejaVuSans.ttf*, 下载支持中文的开源字体[文泉驿microhei字体](http://sourceforge.net/projects/wqy/files/wqy-microhei/):

    #!bash
    # wget 'http://downloads.sourceforge.net/project/wqy/wqy-microhei/0.2.0-beta/wqy-microhei-0.2.0-beta.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fwqy%2Ffiles%2Fwqy-microhei%2F0.2.0-beta%2F&ts=1365584502&use_mirror=jaist' -O wqy-microhei-0.2.0-beta.tar.gz
    # tar xvf wqy-microhei-0.2.0-beta.tar.gz 
    # cp wqy-microhei/wqy-microhei.ttc /var/lib/www/zabbix/fonts/wqy-microhei.ttf

修改*/var/lib/www/zabbix/include/defines.inc.php*，将默认字体*DejaVuSans*替换为*wqy-microhei*字体:

    #!bash
    # sed -i 's/DejaVuSans/wqy-microhei/g' /var/lib/www/zabbix/include/definese.inc.php

重新访问zabbix frontend绘图，中文将完美显示。
    




