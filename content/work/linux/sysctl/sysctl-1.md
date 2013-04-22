Title: Sysctl学习
Date: 2013-04-22
Author: pengyao
Slug: sysctl-1
Tags: linux, sysctl
Category: Linux
Summary: 之前liu.cy老师分享出来他们关于sysctl的PUPPET DSL，征得他同意后，对其中的内容进行逐项学习并分享出来.

刘老师在PUPPET群里边分享出来他们关于sysctl的PUPPET DSL，对应内容如下图:
![sysctl puppet dsl](/static/images/work/linux/sysctl/liu.cy-sysctl.jpg “sysctl Puppet DSL”)

对其逐项学习,对应如下:

### kernel.msgmnb ###
指定内核中每个消息队列的最大字节限制.

### kernel.msgmax ###
指定内核中单个消息的最大长度(bytes). 进程间的消息传递是在内核的内存中进行的，不会交换到磁盘上，所以如果增大该值，则将增大操作系统所使用的内存数量.  

### kernel.shmmax ###
指定共享内存片段的最大尺寸(bytes). 

### kernel.shmall ###
指定可分配的共享内存数量.

### kernel.sysrq###
是否开启sysrq

值说明:0为disable sysrq, 1为enable sysrq completely

关于sysrq的更多内容，可以访问<http://en.wikipedia.org/wiki/Magic_SysRq_key>

### net.core.netdev_max_backlog  ###
设置当接口(interface)接收到的数据包数量超过kernel能够处理(process)的数量时，在INPUT端放入队列的数据包的最大数目.

### net.core.somaxconn ###
表示socket监听(listen)的backlog上限


### net.core.rmem_default ###
表示接收套接字缓冲区大小的缺省值(bytes)

### net.core.rmem_max ###
表示接收套接字缓冲区大小的最大值(bytes)

### net.core.wmem_default ###
表示发送套接字缓冲区大小的缺省值(bytes)

### net.core.wmem_max ###
表示发送套接字缓冲区大小的最大值(bytes)

### net.ipv4.conf.all.accept_redirects ###
是否接受ICMP转发

如果不是路由器，该值需要设置为 0

### net.ipv4.conf.default.accept_redirects ###
是否接受ICMP转发

如果不是路由器，该值需要设置为 0

### net.ipv4.conf.all.accept_source_route ###
是否接受源路由(source route)

### net.ipv4.conf.default.accept_source_route ###
是否接受源路由(source route)

### net.ipv4.conf.all.arp_ignore ###
是否忽略arp请求

值说明:

* 0: (default): reply for any local target IP address, configured on any interface
* 1: reply only if the target IP address is local address, configured on the incoming interface 
* 2: reply only if the target IP address is local address, configured on the incoming interface and both with the sender's IP address are part from same subnet on this interface
* 3: do not reply for local addresses configured with scope host, only resolutions for global and link addresses are replied
* 4-7: 保留
* 8: do not reply for all local addresses 

**注意**: 如果本机作为lvs-dr, 则需要将本值设置为*1*

### net.ipv4.conf.default.arp_ignore ###
同net.ipv4.conf.all.arp_ignore

### net.ipv4.conf.all.rp_filter ###
reverse-path filtering,反向过滤技术，当系统接从A网口接收到一个IP包时，检查其IP实B，然后考察对于B的这个IP，在发送时应该用哪个网卡，如果不在应该接收到的该包的网卡上接收到该IP得包，则认为该包是hacker行为，丢弃(drop)掉.

**注意**: 如果内部网络中机器为多网卡并配置的有静态路由，需要关注本值

### net.ipv4.conf.default.rp_filter ###
同net.ipv4.conf.all.rp_filter

### net.ipv4.conf.all.secure_redirects ###
Prevents hijacking of routing path by only allowing redirects from gateways known in our routing table.

如果服务器不作为网关/路由器,该值建议设置为0

### net.ipv4.conf.default.secure_redirects ###
同net.ipv4.conf.all.secure_redirects

### net.ipv4.conf.all.send_redirects ###
是否发送ICMP转发(redirect)

如果服务器不作为网关/路由器,该值建议设置为0

### net.ipv4.conf.default.send_redirects ###
同net.ipv4.conf.all.send_redirects

### net.ipv4.icmp_echo_ignore_broadcasts ###
是否忽略广播(broadcast)或多播(multicast)的ICMP ECHO请求

### net.ipv4.icmp_ignore_bogus_error_responses ###
是否开启而已ICMP错误消息防护

### net.ipv4.ip_forward ###
是否开启转发

**注意**: 如果作为路由/网关，该值需要设置为1

### net.ipv4.tcp_fin_timeout ###
该参数决定保持在FIN-WAIT-2状态的时间

### net.ipv4.tcp_max_syn_backlog ###
指定 SYN队列的长度，默认为1024,如果网络负载较高，可以加大该值，以容纳更多等待连接的网络连接数

### net.ipv4.tcp_max_tw_buckets ###
指定系统中允许同时保持处于TIME_WAIT状态的sockets数目，如果超过该值，将销毁sockets并打印一条警告信息. 默认值为180000. 

### net.ipv4.tcp_sack ###
是否开启有选择性的应答(Selective Acknowledgement,简称SACK), 具体可以参考[RFC2883][]

### net.ipv4.tcp_synack_retries ###
指定当接收到SYN请求时，会进行多少次SYN ACK重传(retransmit),该值默认是5，每次重传大约花费30-40s，意味着默认情况下被动(passive) TCP连接握手最大会花费180s

### net.ipv4.tcp_syncookies ###
是否开启syn cookies

syn cookies在一定程度上能缓解"syn flood attack"，建议生产系统中开启该选项

### net.ipv4.tcp_timestamps ###
是否开启tcp timestamps，在高速网络中推荐开启本功能

### net.ipv4.tcp_tw_recycle ###
是否开启TIME-WAIT快速重用功能，不建议将该值设置成1，除非你知道该参数会带来什么影响

火丁笔记之前有一篇文章[记一次TIME_WAIT网络故障][]，有关于本参数的分析，推荐一看

### net.ipv4.tcp_tw_reuse ###
允许对新连接重用TIME-WAIT sockets

### net.ipv4.tcp_rmem ###
指定tcp接收缓存(receive memory buffers)，有三个值。第一个是每一个TCP连接最小的接收buffer; 第二个值是每个TCP连接默认分配的接收buffer,该值将覆盖net.core.rmem_default值；第三个是一个TCP连接最大可以分配的接收buffer

### net.ipv4.tcp_wmem ###
指定tcp发送缓存(send memory buffers)，有三个值，和net.ipv4.tcp_rmem类似

### net.ipv4.tcp_window_scaling ###
是否开启tcp滑动窗口

-----------
## 参考资料 ##
1. 文中关于kernel相关选项参考自: <http://www.360doc.com/content/11/0525/15/1429472_119292899.shtml>
2. 文中关于网络栈(network stack)的相关选项参考自: <http://www.cyberciti.biz/faq/linux-tcp-tuning/> 
3. 文中关于net.core.somaxconn参考自: <http://cloud.riaos.com/?p=8000429>
4. 文中部分net.core选项参考自: <http://xiaomaimai.blog.51cto.com/1182965/426842>
5. 文中关于arp选项参考自: <http://kb.linuxvirtualserver.org/wiki/Using_arp_announce/arp_ignore_to_disable_ARP> 
6. 关于arp_ignore与arp_announce参数设置，参考自: <http://www.linuxfly.org/post/539>
7. 关于rp_filter，参考自: <http://www.cnblogs.com/huazi/archive/2013/02/25/2932021.html>
8. 关于net.ipv4.tcp_*参考自: <http://running.iteye.com/blog/624598>
9. 关于sysctl的描述可以参考：<http://www.frozentux.net/ipsysctl-tutorial/ipsysctl-tutorial.html>
10. 记一次TIME_WAIT网络故障--火丁笔记: <http://huoding.com/2012/01/19/142>


[RFC2883]: http://tools.ietf.org/html/rfc2883
[记一次TIME_WAIT网络故障]: http://huoding.com/2012/01/19/142

