显示Salt进程具体名称
##########################

:date: 2015-01-08
:tags: saltstack, process, 进程名
:category: SaltStack
:slug: howto-display-salt-process-name
:author: pengyao
:summary: `Salt`_ 当前已经支持显示具体的进程名, 只需要安装 `setproctitle`_ 重启后即可显示Salt进程的具体名称, 便于Debug

`Salt`_ 当前已经支持显示具体的进程名, 只需要安装 `setproctitle`_ 重启后即可显示Salt进程的具体名称, 便于Debug

环境说明
**************
* 操作系统环境: CentOS 6.5，已配置EPEL源
* Salt Master/Minion版本: 2017.7.0


测试
******************

安装setproctitle

.. code-block:: bash

    yum -y install python-setproctitle

重启salt

.. code-block:: bash

    service salt-master restart
    service salt-minion restart

查看Master端进程

.. code-block:: bash

    ps ax |grep salt |grep -v salt

Master端显示如下(同时个人在行尾追加上进程的具体用途)::

    2943 ?        S      0:00 /usr/bin/python /usr/bin/salt-master -d ProcessManager       # 中心进程管理器
    2944 ?        S      0:00 /usr/bin/python /usr/bin/salt-master -d _clear_old_jobs      # 清除旧的Jobs文件及更新fileserver
    2945 ?        Sl     0:00 /usr/bin/python /usr/bin/salt-master -d Publisher            # 将任务PUB到Minion端
    2946 ?        Sl     0:00 /usr/bin/python /usr/bin/salt-master -d EventPublisher       # Event Publisher进程
    2951 ?        S      0:00 /usr/bin/python /usr/bin/salt-master -d ReqServer_ProcessManager    # ReqServer进程管理器
    2952 ?        Sl     0:01 /usr/bin/python /usr/bin/salt-master -d MWorker              # 劳苦大众, 奋斗在一线的Worker进程
    2953 ?        Sl     0:01 /usr/bin/python /usr/bin/salt-master -d MWorker              # 同楼上
    2954 ?        Sl     0:01 /usr/bin/python /usr/bin/salt-master -d MWorker
    2955 ?        Sl     0:01 /usr/bin/python /usr/bin/salt-master -d MWorker
    2956 ?        Sl     0:01 /usr/bin/python /usr/bin/salt-master -d MWorker
    2957 ?        Sl     0:00 /usr/bin/python /usr/bin/salt-master -d MWorkerQueue         # 将Ret接口(ROUTER)数据转发到Worker(DEALER)

执行个任务, 看看Minion端怎么显示(同时个人在行尾追加上进程的具体用途)::

    2003 ?        Sl     0:01 /usr/bin/python /usr/bin/salt-minion -d        # Minion进程, 接收来自Master端的任务
    2069 ?        S      0:00 /usr/bin/python /usr/bin/salt-minion -d 20150108034936245247   # 接收到任务后, 会启动名为对应jid的进程进行任务处理及结果反馈

这样, 就可以非常清晰的知道Salt的每个进程是做什么用途的, 如果Master/Minion进程异常, 也可以迅速的定位

.. _Salt: http://saltstack.com/
.. _setproctitle: https://pypi.python.org/pypi/setproctitle

