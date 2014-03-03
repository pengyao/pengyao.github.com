ntpq peers字段说明
########################

:date: 2014-03-03
:tags: ntp, nptq, peers
:category: ntp
:slug: ntpq-peers
:author: pengyao
:summary: 服务器为了保持时间的统一, 经常会部署ntpd服务. 经常使用 ``ntpq -p`` 来查看ntpd peers的运行状态信息, 但其输出中的各个字段是什么含义哪?

服务器为了保持时间的统一, 会部署NTPD来进行时间的同步. 对于ntpd当前的状态, 经常会通过 ``ntpq -p`` 或 通过 ``ntpq`` 的console使用 ``peers`` 来进行查看. 输出以下类似结果::

         remote           refid      st t when poll reach   delay   offset  jitter
    ==============================================================================
    +42.96.167.209   202.118.1.46     2 u   32   64  377   19.047   19.838  38.791
    *dns1.synet.edu. 202.118.1.46     2 u   16   64  377  120.494   48.096  25.146
    +114.113.198.166 202.118.1.46     2 u   24   64  377   29.381    9.855  24.694
    +61.135.250.78   223.255.185.2    2 u   24   64  377    4.793   30.086  20.347

那么每个字段代表什么含义哪?

字段含义
================
tally
------------

single-character code indicating current value of the select field of the peer status word

在每个peer最前边的一个标签字符串, 用来表示该peer的select状态. 

* ``*`` : sys.peer, 表示该peer已标记为system peer, 以其变量作为系统变量.
* ``+`` : candidat, 表示该peer存活并且作为候选peer.
* ``-`` : outlyer, 表示该peer已经被ntp cluster算法标记为偏远的peer.
* ``#`` : selected, 表示该peer存活, 但并不在前六个同步peer的范围内.
* ``.`` : excess, 表示该peer不在前十个同步peer的范围内.
* ``o`` : pps.peer, The peer has been declared the system peer and lends its variables to thesystem variables. However, the actual system synchronization is derived from a pulse-per-second (PPS) signal, either indirectly via the PPS reference clock driver or directly via kernel interface.
* ``x`` : falsetick, The peer is discarded by the intersection algorithm as a falseticker.
* 空字符: space reject, 表示该peer标记为不可达.

remote
-------------

host name (or IP number) of peer

该peer的主机名或IP地址, 可以在运行 ``ntp`` 命令时使用 ``-n`` 选项来不进行DNS解析, 直接显示为IP地址

refid
------------

association ID or kiss code

该peer的关联ID, 及该peer自身的 system.peer.

st
-----------------

stratum

该peer在NTP结构中的层级. NTP为层级结构, 数字越小表示其层级越高, 有效值是0到15.

t
---------------

type

peer类型. ``u`` 为单播(unicast), ``b`` 为广播(broadcast), ``l`` 为本地(local).

when
-----------

sec/min/hr since last received packet

上次收到的该peer的ntp回应包距当前的时间.

poll
-----------

poll interval

查询间隔, 单位为秒. ntp算法会基于该peer的时间状况对该peer的查询间隔进行动态调整. 如果该peer的时间状态良好, 会在同步过程中加大该同步间隔, 反之则减小查询间隔. 在CentOS 6系统中, 默认的该查询间隔的最小值是64s, 最大值是1024s.

reach
------------

reach shift register (octal)

标记该peer的reach计数, 该值是8进制数.

该值是写本文的直接原因, 因为发现之对该值的理解是错误的. 之前的理解是参照`鸟哥书中的描述 <http://linux.vbird.org/linux_server/0440ntp.php#server_start>`_ , *已經向上層 NTP 伺服器要求更新的次數*. 而实际上该值并不是计数器, 而是表示最近八次ntp查询的reach状态.

该值为8进制数, 由三个数组组成, 每个八进制对应3比特. 起始值是0, 之后的比特将每次进行完pool之后左移一位(如果收到ntp回应,则设置为1, 反之为0) 

因此通常启动时, 该值的变化为: 0, 1, 3, 17, 37, 77, 177, 377

以本文中输出为例, 377八进制数换算成2进制为11111111, 即最近八次查询均可达.


delay
--------------

roundtrip delay

查询往返延迟, 单位是毫秒(milliseconds)

offset
------------

offset

peer与本机时间偏差, 单位为毫秒(milliseconds)


jitter
-------------

jitter

尚未学习该字段含义



参考链接
=====================
* ntpq手册: ``man ntpq``
* ntp手册: http://doc.ntp.org/4.2.0/ntpq.html
* NTP协议: http://en.wikipedia.org/wiki/Network_Time_Protocol
* NTP Debugging Techniques: http://www.fifi.org/doc/ntp-doc/html/debug.htm

