Title: 基于Zabbix IPMI监控服务器硬件状况
Date: 2013-04-27
Author: pengyao
Slug: zabbix-monitor-ipmi-1
Tags: zabbix, ipmi, dell
Category: Zabbix
Summary: IDC空调开始不给力了，为了防患未然，需要对服务器温度、风扇转速等进行监控。本文将用实例讲述在Zabbix平台如何使用IPMI完成相关信息收集。


最近温度升高，IDC空调也开始不给力了(谣传12306曾因空调问题导致业务无法工作), 为了防患未然，将可能引发的故障扼杀在萌芽里。由于之前已经部署了Zabbix监控系统，本次将结合Zabbix自带的IPMI，完成服务器温度及风扇转速的监控.


## 环境说明 ##
### 被监控端 ###
* 服务器型号：Dell PowerEdge R415，配置有iDrac Enterprise
* 安装系统: CentOS 6.3 
* 规划分配的IPMI地址: 10.0.2.121
### Zabbix监控平台说明
* Zabbix版本: 2.0.4，在安装时，已经**--with-openipmi**
* Zabbix网络接口可以连通10.0.2.121

## 前置学习 ##

* 维基百科IPMI: <http://zh.wikipedia.org/wiki/IPMI>
* IBM DeveloperWorks -- 使用ipmitool实现Linux系统下对服务器的ipmi管理: <http://www.ibm.com/developerworks/cn/linux/l-ipmi/>
* Dell -- Managing Dell PowerEdge Servers Using IPMItool: <http://www.dell.com/downloads/global/power/ps4q04-20040204-Murphy.pdf>
* Zabbix IPMI checks: <https://www.zabbix.com/documentation/2.0/manual/config/items/itemtypes/ipmi>
* 使用IPMITOOL实现终端重定向(课外读物): <http://docs.linuxtone.org/ebooks/Dell/ipmitool.pdf>


## 配置IPMI ##
### 配置IPMI地址 ###
可以参考前置推荐中的《Managing Dell PowerEdge Servers Using IPMItool》在服务器启动时进行IPMI地址的配置，并开启IPMI Over LAN

如果当前服务器已经处于运行状态，可以通过发行版自带的IPMItool进行IPMI的配置，以下是配置说明:

首先安装IPMItool软件包并开启IPMI服务:

    #!bash
    # yum install OpenIPMI ipmitool
    # service ipmi start
启动服务，将自动添加直接连接BMC的设备驱动。

配置IPMI地址:

    #!bash
    # ipmitool lan set 1 ipaddr 10.0.2.121
    # ipmitool lan set 1 netmaks 255.255.255.0
    # ipmitool lan set 1 defgw ipaddr 10.0.2.1
    # ipmitool lan print 1
将本机的IPMI地址配置为10.0.2.121/24,网关为10.0.2.1

开启IPMI Over LAN

    #!bash
    # ipmitool lan set 1 access on

### 配置用户 ###
本次的需求为监控服务器传感器信息，只需要USER级别用户即可.

    #!bash
    # ipmitool user set name 15 sensor
    # ipmitool user set password 15 sensor_pass
    # ipmitool user enable 15
    # ipmitool user priv 15 2 1
    # ipmitool user list 1
将建立id为15（为嘛是15不是13，因为俺喜欢15这个数字），用户名为sensor，密码为sensor_pass,权限为User(对应2)
### 测试 ###
登录Zabbix服务器，通过ipmitool远程访问Dell服务器传感器信息

    #!bash
    # ipmitool -H 10.0.2.121  -Usensor -L USER sensor list

## 配置Zabbix ##
* 注：为了支持IPMI,需要在zabbix server/proxy安装时增加**--with-openipmi**参数

服务器端配置zabbix IPMI pollers

    #!bash
    # sed -i '/# StartIPMIPollers=0/aStartIPMIPollers=5' zabbix_server.conf
    # service zabbix-server restart

导入监控模板(模板下载地址: <https://raw.github.com/pengyao/zabbix/master/Server/templates/zbx_templates_DELL_R415.xml>)

添加监控主机，关联上本模板，并在**IPMI**页面，设置*Authentication algorithm*为*Default*, *Privilege level*为*User*, *Username*为*sensor*, *Password*为*sensor_pass*，保存即可


## 总结 ##
在应用过程中，发现当前Zabbix IPMI监控效率较低，希望新版本能够有所改善
