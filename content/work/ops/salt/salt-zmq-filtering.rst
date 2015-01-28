Salt zmq_filtering测试
##########################

:date: 2015-01-27
:tags: saltstack, zeromq, zmq_filtering, envelopes
:category: SaltStack
:slug: salt-zmq-filtering
:author: pengyao
:summary: Salt 2014.7新增了zmq_filtering配置项, 利用zeromq PUB/SUB Envelopes技术, 可以实现消息只发送到target minion(目前只支持list target)

Salt 2014.7新增 `zmq_filtering`_ 配置项, 基于zeromq PUB-SUB `Envelopes`_ 技术,
在Master端(publisher)进行message过滤(ZeroMQ 3.0+版本,之前版本是在subscriber端进行过滤), 以实现如果该指令只是少量主机执行的话,
只将指令发送到匹配的Minion端, 而并非发送到所有的Minion端. 需要注意的是, 目前zmq_filtering只作用list target, 即使用-L来指定target.
本文将对其进行功能及效果测试.

前置阅读
***************

* ZeroMQ PUB-SUB Message Envelopes: http://zguide.zeromq.org/page:all#Pub-Sub-Message-Envelopes

环境说明
*************

* OS: CentOS 6.5 X86_64
* Salt: Master/Minion架构, 2014.7.1版本

开工
*********

配置zmq_filtering
====================

.. note::

    zmq_filtering参数在Master端及Minion端均需要配置才能生效, 默认为False

Master端配置zmq_filtering

.. code-block:: bash

    echo "zmq_filtering: True" >> /etc/salt/master
    service salt-master restart

Minion端配置zmq_filtering

.. code-block:: bash

    echo "zmq_filtering: True" >> /etc/salt/minion
    service salt-minion restart

操作完毕后, Master进行test.ping测试

.. code-block:: bash

    salt '*' test.ping

输出如下内容::

    minion-02.example.com:
        True
    minion-01.example.com:
        True

测试zmq_filtering
======================

.. note::

    以下操作如非特别声明, 均在Master端进行

在Master端开启一个新的控制台, 使用tcpdump进行抓包

.. code-block:: bash

    tcpdump -i eth0 src port 4505

使用Globbing target进行测试

.. code-block:: bash

    salt 'minion-01.example.com' test.ping

tcpdump抓包结果如下::

    07:21:18.104954 IP salt-master.example.com.4505 > salt-minion-01.example.com.58024: Flags [P.], seq 396:602, ack 1, win 227, options [nop,nop,TS val 4253627 ecr 4239803], length 206
    07:21:18.105190 IP salt-master.example.com.4505 > salt-minion-02.example.com.33595: Flags [P.], seq 396:602, ack 1, win 227, options [nop,nop,TS val 4253627 ecr 4294907239], length 206

从结果来看, 虽然指定了minion-01.example.com, 因为Salt是PUB-SUB结构, 消息均会发送到所有的Minion

使用List target进行测试

.. code-block:: bash

    salt -L 'minion-01.example.com' test.ping

tcpdump抓包结果如下::

    07:23:35.378587 IP salt-master.example.com.4505 > salt-minion-01.example.com.58024: Flags [P.], seq 602:839, ack 1, win 227, options [nop,nop,TS val 4390900 ecr 4245316], length 237

从结果看, 在Master进行了过滤, 虽然是PUB-SUB, 但消息只发送给了salt-minion-01.example.com, 并没有发送到其他Minion上, 达到了zmq_filtering的效果.

测试ZeroMQ PUB-SUB Message Envelopes性能
============================================

开启zmq_filtering, 如果不是所有Minion均需要执行的操作, 通过在Master端进行消息过滤, 能够大大降低Master端发送指令时的带宽消耗, 那么zmq_filtering的性能又如何?

由于zmq_filtering只是利用ZeroMQ的PUB-SUB Message Envelopes, 其性能测试个人觉得只需要测试ZeroMQ PUB/SUB即可. 因此就假设了如下极端场景:

* publisher 1节点, subscriber 1000节点(单节点开启1000个线程)
* 进行1000次消息发送, 每条消息均需要发送到所有subscriber


直接上代码:

**publisher.py**

.. code-block:: python

    import sys
    import zmq
    import time
    import json
    import hashlib

    def pub():
        context = zmq.Context()
        socket = context.socket(zmq.PUB)

        socket.bind("tcp://*:5556")
        return context, socket

    def sub_ids(subs=100):
        sub_list = []
        for each_sub in xrange(1, subs + 1):
            idx = hashlib.md5(str(each_sub)).hexdigest()
            sub_list.append(idx)
        return sub_list

    def main(broadcast=True, times=100, subs=100):
        context, socket = pub()
        message = {'tgt_type': 'glob', 'jid': '20150106053023956920', 'tgt': '*', 'ret': '', 'user': 'sudo_vagrant', 'arg': [], 'fun': 'test.ping'}
        message = json.dumps(message)
        if not broadcast:
            sub_list = sub_ids(subs=subs)

        # sleep 30 seconds, guarantee all subscribes have  subscribed
        time.sleep(30)

        print "regain consciousness"
        start_time = time.time()
        for each in xrange(1, times+1):
            if broadcast:
                socket.send(message)
            else:
                for each_sub in sub_list:
                   socket.send(each_sub, flags=zmq.SNDMORE)
                   socket.send(message)

        end_time = time.time()

        print "-------------------------------"
        print "Exec times: %s, Exec time: %dms" %(times, end_time * 1000 - start_time * 1000)

    if __name__ == '__main__':
        subs = 1000
        times = 1000
        if len(sys.argv) == 2 and sys.argv[1] == 'unicast':
            broadcast = False
        else:
            broadcast = True
        print "broadcast subscriber: %s" % broadcast
        main(broadcast=broadcast, times=times, subs=subs)

**subscriber.py**

.. code-block:: python

    import sys
    import zmq
    import threading
    import hashlib

    def sub(pub_uri, times=100, idx=None):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(pub_uri)
        if idx:
            socket.setsockopt(zmq.SUBSCRIBE, idx)
        else:
            socket.setsockopt(zmq.SUBSCRIBE, '')
        for each in xrange(1, times + 1):
            socket.recv()
        socket.close()


    def main(subs=100, times=100, broadcast=True):
        pub_uri = 'tcp://salt-master.example.com:5556'
        sub_list = []
        for each_sub in xrange(1, subs+1):
            if broadcast:
                sub_list.append(threading.Thread(target=sub, args=(pub_uri,), kwargs={'times': times}))
            else:
                idx = hashlib.md5(str(each_sub)).hexdigest()
                sub_list.append(threading.Thread(target=sub, args=(pub_uri,), kwargs={'times': times, 'idx': idx}))
        for each_sub in sub_list:
            each_sub.start()
        print "subscriber start ok"
        for each_sub in sub_list:
            each_sub.join()
        print "subscriber done"


    if __name__ == '__main__':
        subs = 1000
        times = 1000
        if len(sys.argv) == 2 and sys.argv[1] == 'unicast':
            broadcast = False
        else:
            broadcast = True
        print "broadcast subscriber: %s" % broadcast
        main(subs=subs, times=times, broadcast=broadcast)

**测试用例1: 默认的PUB-SUB**

.. code-block:: bash

    python publisher.py    # 在Publisher(Master)端进行
    python subscriber.py   # 在Subcriber(Minion-01)端进行

执行时间为 1588ms

**测试用例2: 启用PUB-SUB Message Envelopes**

.. code-block:: bash

    python publisher.py unicast   # 在Publisher(Master)端进行
    python subscriber.py unicast   # 在Subcriber(Minion-01)端进行

执行时间为 6786ms

两者相差5s左右, 由于本次测试, 为极端情况(1000次且每次都需要发送到所有subscriber), 增加的成本在可承受范围之内.


QA
========

**Q: 如果只是单边启动zmq_filtering, 是否会影响使用?**

A: 这里边有两种情况

* Master端配置了zmq_filtering, 对于没有配置zmq_filtering的Minion, 将像以前一样, master端依然会将消息发送给它(不管target是否匹配), 对于已经开启zmq_filtering的minion, 则如果list target不匹配, master则不会发送消息给它.
* Master没有配置zmq_filtering, 而Minion进行了配置, 则该Minion收不到任何指令


**Q: zmq_filtering适用场景**

A: 当前zmq_filtering只会匹配list target, 对于其他的target方式, 则采用默认的PUB-SUB. zmq_filtering适用于大规模集群, 但每次执行只是少数主机运行指令的场景.





.. _zmq_filtering: https://github.com/saltstack/salt/pull/13285
.. _Envelopes: http://zguide.zeromq.org/page:all#Pub-Sub-Message-Envelopes
