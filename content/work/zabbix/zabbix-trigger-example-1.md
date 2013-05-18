Title: Zabbix Trigger表达式实例
Date: 2013-05-18
Author: pengyao
Slug: zabbix-trigger-example-1
Tags: zabbix, trigger, 表达式, 实例
Category: Zabbix
Summary: 整理常用的Zabbix Trigger表达式实例

Zabbix提供强大的触发器(Trigger)函数以方便进行更为灵活的报警及后续动作，具体触发器函数可以访问<https://www.zabbix.com/documentation/2.0/manual/appendix/triggers/functions>, 之前也有翻译本文章，地址为: <http://pengyao.org/zabbix-triggers-functions.html>

今天用实例来说明常见的监控需求，应该如何来编写Trigger表达式. 主人公就暂且叫做"绿肥"吧.

## 前奏 ##
"绿肥，别整天就知道聊QQ，也关注下服务器运行情况吧." 老大颇不满意的说.

"哦"，绿肥只好先应承下来

“关注服务器? 咋关注？” 绞尽脑汁，听说有个监控神器叫**zabbix**, 按照手册里边说的部署上了zabbix、将"test-01"服务器也安装了agent, 添加了"*agent.ping*" item用来测试agent是否可以连通； "*system.uptime*" item用来收集主机运行时间; “*system.cpu.util[,idle]*” item用来收集CPU空闲百分比.

收集完这些值，通过simple graph能看到运行状况，老大似乎很满意. 但接下来的一天, 主机不知道什么时候重启了，老大劈头盖脸的说“机器重启了都不知道？要这个监控有什么用？”

看来是时候学习下zabbix trigger了，看下什么情况下触发报警.

## Zabbix Trigger实例 ##
"得，还是先学习下怎么判断机器是否重启了吧"，绿肥喃喃的说

system.uptime映入眼帘，这个item是采集主机运行时间的,一直累加的计数器，如果当前采集值小于上一次的采集值，那就意味着机器重启了

怎么判断当前值小于上一次哪？ 查询手册发现change函数, 看来对应的Trigger表达式是: 

    {test-01:system.uptime.change(0)}<0 

表达式加上后，配合上默认的Action规则，手动重启了下服务器，真的告警的耶，绿肥愉快的笑了起来.

**直到又一天的到来......**

这天机器重启了，因为硬盘故障, 结果系统没起来, 直到老大发现...... 

"哎，又挨了一通训", 不过的确是工作不到位，系统没启动都不知道，这工作做得真叫一个差

"怎么搞"，*agent.ping*映入了眼帘，看来得拿它"出出气"了，ping不通都不告诉我，哼，不整治你整治谁

"系统没起来，也就意味着zabbix agent没启动起来，没启动起来，那就是说我大zabbix server根本取不到agent的数据，那么该用哪个函数那?", "**nodata**"，对，就是它，写出来的表达式是这样的:

    {test-01:agent.ping.nodata(3m)}=1

三分钟取不到*agent.ping*的值，那也就是说agent宕了或者服务器挂了，不错，不错.

**直到又一天来临了.....** 

"什么情况，怎么网站打开这么慢？" 老大在那里嘟囔着

趁机看了下CPU使用率，我擦，已经持续一小时CPU 100%满负荷运行了，看来隔壁研发小妹又写了个死循环,不过我是不是得增加个CPU的报警?

说干就干，既然是CPU有问题，那就从CPU下手，之前增加过"*system.cpu.util[,idle]*"的item,这次就写个trigger, 写出来的trigger是这个样子:

    {test-01:system.cpu.util[,idle].last(0)}<20

也就是说如果cpu空闲小于20%即CPU占用超过80%立即触发报警，嘿嘿，看来不错

一天过去了，邮箱里增加了几百封关于"CPU使用率超过80%的邮件"，查询一看，CPU使用率总是冒个尖就马上就下来了,看来它把这里当城门了，这里用*last(0)*有点不靠谱，那么该用哪个函数哪？ 还得好好翻翻手册.

"最近几分钟，最近几分钟，最近几分钟"，绿肥若有所思的自言自语着......

    {test-01:system.cpu.util[,idle].avg(3m)}<20

连续三分钟CPU使用率平均值超过80%触发报警, 有没有更狠一点的，三分钟CPU使用率持续在80%以上触发报警

    {test-01:system.cpu.util[,idle].max(3m)}<20

连续三分钟CPU空闲率中的最大值小于20%即每一个值都小于20%，对应的是就是CPU使用率全部都在80%以上，看来这个的确更狠一点.

似乎还有点不妥，发现CPU占用率在79.9%左右竟然也给我报OK，不爽，不爽, 看来需求得调整为"连续三分钟CPU使用率超过80%触发报警，如果连续三分钟CPU使用率低于50%才认为恢复正常"

手册里边有个"**TRIGGER.VALUE**"宏，看来得从这里下下手.

**TRIGGER.VALUE**对应的为Trigger状态，0代表OK, 1代表Problem，分解下需求:

* 正常情况下连续三分钟CPU使用率超过80%，看起来表达式是:
 
        {TRIGGER.VALUE}=0&{test-01:system.cpu.util[,idle].max(3m)}<20

* 故障时连续三分钟CPU使用率低于50%恢复正常，即故障时刻CPU使用率持续三分钟高于50%依然为故障，表达式是这个样子的:

        {TRIGGER.VALUE}=1&{test-01:system.cpu.util[,idle].min(3m)}<50

然后整合下表达式，就成了下边这个样子:

    ({TRIGGER.VALUE}=0&{test-01:system.cpu.util[,idle].max(3m)}<20) | ({TRIGGER.VALUE}=1&{test-01:system.cpu.util[,idle].min(3m)<50}


不错，不错，看起来多高端，颇有成就感!

**直到又一天的到来......**






 

