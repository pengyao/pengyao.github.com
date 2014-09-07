Salt中Syndic那点事
#####################

:date: 2014-09-07
:tags: saltstack, zeromq, syndic
:category: SaltStack
:slug: salt-syndic-01
:author: pengyao
:summary: `Salt`_ 在 `0.9.0版本 <http://docs.saltstack.com/en/latest/topics/releases/0.9.0.html>`_ 中增加了 `Syndic`_ 特性. 通过Syndic, 可以快速构建出多层级的Salt拓扑, 使Salt变得更灵活. 那么Syndic是如何工作的? 当前有哪些优势和局限哪?

基本简介
****************
`Salt`_ 在 `0.9.0版本 <http://docs.saltstack.com/en/latest/topics/releases/0.9.0.html>`_ 中增加了 `Syndic`_ 特性. Syndic建立在中心Master和Minions之间, 并允许多层分级Syndic, 使Salt拓扑可以变得更为灵活. 那么Syndic是如何工作的? 当前有哪些优势和局限哪?

前置阅读
****************
* `0MQ - The Guide: Sockets and Patterns  <http://zguide.zeromq.org/page:all#Chapter-Sockets-and-Patterns>`_
* `Salt中ZeroMQ那点事 <http://pengyao.org/salt-zeromq-01.html>`_

环境说明
****************
* CentOS6.4
* Salt `2014.1.10 <https://github.com/saltstack/salt/tree/v2014.1.10/salt>`_ ,默认配置

安装配置Syndic
****************

安装Syndic
============
Syndic是Master的一个小组件, 位于salt-master软件包中, 安装salt-master时就安装了syndic

.. code-block:: bash

    yum -y install salt-master

配置Syndic
============
默认Syndic的配置文件位于Master配置文件中( */etc/salt/master* ), 需要配置的参数也非常简单:

 * syndic_master: 配置MasterOfMaster的IP地址
 * syndic_master_port: 配置MasterOfMaster的ret_port(默认为4506)
 * syndic_log_file: 指定syndic日志文件(绝对路径)
 * syndic_pidfile: 指定syndic pid文件(绝对路径)

同时MasterOfMaster需要将 *order_masters* 选项设置为 *True*, 为了使配置生效, 需要对其进行重启.

运行Syndic
=============

.. code-block:: bash

    chkconfig salt-master on
    chkconfig salt-syndic on
    service salt-master restart
    service salt-syndic restart

Syndic是如何工作的?
***********************

Syndic本质上是一个特殊的Minion, 这不, 其代码就位于 `minion.py <https://github.com/saltstack/salt/blob/v2014.1.10/salt/minion.py#L1516>`_ 中.

Syndic需要在本地运行Master, 并将需要管理的Minions的master指向syndic所在的主机. Syndic是这么来工作的:

1. 冒充Minion, 建立连接MasterOfMaster PUB接口的SUB接口, 订阅所有来自MasterOfMaster下发的任务

.. code-block:: python

    self.socket = self.context.socket(zmq.SUB)
    self.socket.setsockopt(zmq.SUBSCRIBE, '')
    self.socket.setsockopt(zmq.IDENTITY, self.opts['id'])
    self.socket.connect(self.master_pub)


2. 接收到MasterOfMaster下发的数据后, 首先进行解密, 解密完成后, 将其扔到本地的Master接口上进行二次下发:

.. code-block:: python

    payload = self.serial.loads(self.socket.recv())
    self._handle_payload(payload)

.. code-block:: python

    # Send out the publication
    self.local.pub(data['tgt'],
                   data['fun'],
                   data['arg'],
                   data['tgt_type'],
                   data['ret'],
                   data['jid'],
                   data['to'])


3. 在2中进行的二次下发之后, 监听本地event接口, 获取旗下Minions的返回:

.. code-block:: python

    event = self.local.event.get_event(0.5, full=True)

并将返回发送给MasterOfMaster Ret接口

.. code-block:: python

    self._return_pub(jids[jid], '_syndic_return')


Syndic的优势和局限
**********************

优势
=========

1. 通过Syndic, 可以建立多层级的Salt拓扑, Syndic下的Minions即可通过Syndic所在的Master进行管理, 也可以通过MasterOfMaster及更高层级的Master进行管理, 架构变得异常灵活.

2. 由于Syndic只订阅MasterOfMaster下发下来的任务, 对于文件服务等, Syndic本地需要进行配置,可以有效的降低MasterOfMaster的负载

局限
=========

由于Syndic弱化了MasterOfMaster, 采用区域自治方法. 在某些应用场景下, 会有局限性:

1. 优势2中的优势, 也带来了局限, 需要保证Syndic上的file_roots及pillar_roots与MasterOfMaster是一致的. 为了解决这个问题, 我们在使用Syndic时采用了 `gitfs backend <http://docs.saltstack.com/en/latest/topics/tutorials/gitfs.html>`_

2. 由于Syndic管理了旗下Minions的认证, 使MasterOfMaster并不知道有多少Syndic主机, Syndic下边有多少Minions. 在MasterOfMaster及更高层级的Master上使用salt命令行下发远程执行命令时, 如果Syndic此时与MasterOfMaster网络抖动, 导致没有收到消息或延迟收到消息, MasterOfMaster并不知情; Syndic并没有返回结果或延迟返回结果, MasterOfMaster并不能感知到, 会导致结果不完整. 如果没有其他验证机制, 将变得不可控. 官方提供的解决方案是增大 *syndic_wait* 选项, 但个人认为只能缓解,并不能根治本问题.


.. _Salt: https://github.com/saltstack/salt
.. _Syndic: http://docs.saltstack.com/en/latest/topics/topology/syndic.html 
.. _ZeroMQ: http://zeromq.org/
