Tomcat Manager Text API测试
=================================

:date: 2013-12-26
:tags: webserver, tomcat, manager, 字符接口, api
:category: WebServer
:slug: tomcat-manager-text-api-test
:author: pengyao
:summary: Tomcat Manager提供应用的状态查询,部署,维护等功能. 同时提供有Text API接口,对其进行基本测试.

基本介绍
----------
Tomcat Manager提供应用的状态查询, 部署, 维护等功能,  使用方法请参考: `Tomcat Manager HowTo`_

对Tomcat Manager的Text接口进行了测试, 附上测试用例及结果分析

环境说明
----------
* Tomcat: 7.0.49
* Manager URL: http://127.0.0.1:8080/manager/
* 测试工具: curl

manager访问控制配置
------------------------
* ${CATALINA_BASE}/conf/tomcat-users.xml

  .. code-block:: xml

    ......
    <tomcat-users>
        <user username="pengyao" password="pengyao_pass" roles="manager-script"/>
    </tomcat-users>
  
* ${CATALINA_BASE}/conf/Catalina/localhost/manager.xml 

  .. code-block:: xml

    <Context privileged="true" antiResourceLocking="false"  docBase="${catalina.home}/webapps/manager">
        <Valve className="org.apache.catalina.valves.RemoteAddrValve" allow="127.0.0.1" />
    </Context>

* 配置完成后需要重启Tomcat

测试
-------------

查询服务信息
^^^^^^^^^^^^^^

* Request:

  .. code-block:: bash

    curl -u pengyao:pengyao_pass http://127.0.0.1:8080/manager/text/serverinfo

* Response::

    OK - Server info
    Tomcat Version: Apache Tomcat/7.0.47
    OS Name: Linux
    OS Version: 2.6.32-358.11.1.el6.x86_64
    OS Architecture: amd64
    JVM Version: 1.6.0_45-b06
    JVM Vendor: Sun Microsystems Inc.


获取当前已部署应用列表
^^^^^^^^^^^^^^^^^^^^^^^^^

* Request:

  .. code-block:: bash

     curl -u pengyao:pengyao_pass http://127.0.0.1:8080/manager/text/list

* Response::

    OK - Listed applications for virtual host localhost
    /:running:0:ROOT
    /manager:running:6:manager
    /docs:running:0:docs
    /examples:running:0:examples
    /host-manager:running:0:host-manager

结果以冒号做分隔, 第一列为context path, 第二列为当前应用的状态, 第三列为当前活跃的session数, 第四列为appBase

获取应用sessions设置及当前sessions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Request:

  .. code-block:: bash

    curl -u pengyao:pengyao_pass http://127.0.0.1:8080/manager/text/sessions?path=/manager

* Response::

    OK - Session information for application at context path /manager
    Default maximum session inactive interval 30 minutes
    24 - <25 minutes: 1 sessions
    26 - <27 minutes: 1 sessions

启动应用
^^^^^^^^^^^^^^^^

* Request:

  .. code-block:: bash

    curl -u pengyao:pengyao_pass http://127.0.0.1:8080/manager/text/start?path=/examples

* Response::

    OK - Started application at context path /examples

如果指定的path(context path)不存在, 则报错::

    FAIL - No context exists for path /pengyao


关闭应用
^^^^^^^^^^^^^^^^

* Request:

  .. code-block:: bash
  
    curl -u pengyao:pengyao_pass http://127.0.0.1:8080/manager/text/stop?path=/examples

* Response::

    OK - Stopped application at context path /examples


重启应用
^^^^^^^^^^^^^^^^^

主要应用于更新了类或jar, 但没有配置 *reloadable*, 需要手动进行重启应用, 以使其生效

* Request:

  .. code-block:: bash

    curl -u pengyao:pengyao_pass http://127.0.0.1:8080/manager/text/reload?path=/examples


* Response::

    OK - Reloaded application at context path /examples

如果应用reload前并不处于running状态, 则会报错::

    FAIL - Encountered exception java.lang.IllegalStateException: Context with name [/examples] has not yet been started

卸载应用
^^^^^^^^^^^^^^^^^

* 注意: 该操作将会删除 appBase及对应的war包, 请谨慎使用. 如果只是想暂停某应用, 请使用 **关闭应用(stop)** 方法

* Request:

  .. code-block:: bash
    
    curl -u pengyao:pengyao_pass http://127.0.0.1:8080/manager/text/undeploy?path=/examples
 
* Response::

    OK - Undeployed application at context path /examples

如果应用不存在,则报错::

    FAIL - No context exists for path /pengyao
     
部署应用
^^^^^^^^^^^^

下载测试用例:

  .. code-block:: bash

     wget http://tomcat.apache.org/tomcat-6.0-doc/appdev/sample/sample.war -O /tmp/sample.war

**以PUT方式上传war包部署应用**

* Request:

  .. code-block:: bash

    curl -u pengyao:pengyao_pass -T /tmp/sample.war  http://127.0.0.1:8080/manager/text/deploy?path=/sample

* Response::

    OK - Deployed application at context path /sample

此时将能在${CATALINA_BASE}/webapps/下找到sample.war 及 sample目录

**以本地(Tomcat Server本地)war包部署应用**

* Request:

  .. code-block:: bash

    curl -u pengyao:pengyao_pass "http://127.0.0.1:8080/manager/text/deploy?path=/foo&war=file:/tmp/sample.war"

* Response::

    OK - Deployed application at context path /foo

此时将能在${CATALINA_BASE}/webapps/下找到foo.war 及 foo目录


.. _Tomcat Manager HowTo: http://tomcat.apache.org/tomcat-7.0-doc/manager-howto.html
