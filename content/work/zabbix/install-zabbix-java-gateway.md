Title: 安装配置Zabbix Java GateWay
Date: 2013-05-05
Author: pengyao
Slug: install-zabbix-java-gateway
Tags: java, zabbix, java gateway, 安装
Category: Zabbix
Summary: 从Zabbix 2.0开始，自带了一个用于监控JMX应用的程序，称为"Zabbix Java GateWay"，本文将讲述如何安装Zabbix Java GateWay。

从Zabbix 2.0开始，软件包中自带了一个用于监控JMX应用的程序，称为"Zabbix Java GateWay"，非常方便使用其来监控JMX，有一个朋友问我它如何安装使用，将之前个人在环境中使用的方法分享出来。

## 环境说明 ##
* 安装方法: 编译安装
* Zabbix软件包: Zabbix-2.0.6.tar.gz
* JDK版本: 1.7.0_21 
* 宿主系统: CentOS 6.3 X86_64
## 前置配置 ##
* 前置阅读: <https://www.zabbix.com/documentation/2.0/manual/concepts/java>
* 由于Zabbix Java GateWay基于Java开发，所以需要先安装JDK
### JDK安装配置 ###
* 访问<http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html> 并下载对应系统的jdk包,下载完成后将包传输到需要安装Zabbix Java GateWay的主机上
* 解压并安装jdk:

        #!bash
        # tar xvf jdk-7u21-linux-x64.tar.gz -C /usr/localource /etc/bashrc
        # ln -s /usr/local/jdk1.7.0_21 /usr/local/jdk 

* 配置JAVA_HOME及PATH


        #!bash
        # echo 'JAVA_HOME=/usr/local/jdk' >> /etc/bashrc
        # echo 'PATH=$PATH:${JAVA_HOME}/bin/' >> /etc/bashrc
        # echo 'export JAVA_HOME PATH' >> /etc/bashrc
        # source /etc/bashrc
 
### 下载Zabbix安装包(可选) ###
* 如果需要安装Zabbix Java GateWay的主机并没有下载Zabbix安装包，需要下载Zabbix安装包,下载地址: <http://downloads.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/2.0.6/zabbix-2.0.6.tar.gz?r=http%3A%2F%2Fwww.zabbix.com%2Fdownload.php&ts=1367766309&use_mirror=jaist> 
* 解压zabbix安装包

        #!bash
        # tar xvf zabbix-2.0.6.tar.gz
        # cd zabbix-2.0.6

## 安装Zabbix Java GateWay ##


    #!bash
    # ./configure --prefix=/usr/local/zabbix_java_gateway-2.0.6 --enable-java
    # make && make install
    # ln -s /usr/local/zabbix_java_gateway-2.0.6 /usr/local/zabbix_java_gateway
    # test -d /etc/zabbix || mkdir /etc/zabbix
    # cp /usr/local/zabbix_java_gateway/sbin/zabbix_java/settings.sh /etc/zabbix/zabbix_java_gateway.conf

Zabbix中自带的zabbix_java_gateway维护脚本比较差，重写了维护脚本, 下载地址: <https://raw.github.com/pengyao/zabbix/master/Zabbix_Java_GateWay/scripts/zabbix_java_gateway>


    #!bash
    # wget https://raw.github.com/pengyao/zabbix/master/Zabbix_Java_GateWay/scripts/zabbix_java_gateway -O /etc/init.d/zabbix_java_gateway
    # chmod +x /etc/init.d/zabbix_java_gateway
    # chkconfig zabbix_java_gateway on

## 配置Zabbix Java GateWay ##
* 配置文件: /etc/zabbix/zabbix_java_gateway.conf
* 支持的配置选项为:
 
名称            |    选项说明
--------------- | ----------------------------
LISTEN_IP       | 指定bind的地址,默认值为0.0.0.0
LISTEN_PORT     | 指定bind的端口,默认值为10052
PID_FILE        | 指定PID文件存放目录，默认为 /tmp/zabbix_java.pid
START_POLLERS   | 指定启动多少进程, 默认为5

* Zabbix Java GateWay启动后，也需要在Zabbix Server/Proxy上进行配置,对应的配置文件选项为:
 
名称             |    选项说明
---------------- | ----------------------------
JavaGateway      | 指定Zabbix Java GateWay地址
JavaGatewayPort  | 指定Zabbix Java GateWay端口，默认为10052
StartJavaPollers | 指定启动时启动的Java Pollers数量


* 注意：Zabbix Server/Proxy中的StartJavaPollers要小于等于Zabbix Java GateWay配置文件中的START_POLLERS
* 关于如何添加JMX监控，请访问: <https://www.zabbix.com/documentation/2.0/manual/config/items/itemtypes/jmx_monitoring>
* 小贴士：Zabbix Java GateWay类似于Proxy(只是不存储数据和配置)，所以在使用Proxy/Node等分布式环境中，推荐在每个区域部署对应的Zabbix Java GateWay






