Title: Salt之SSH API测试
Date: 2015-06-03
Tags: Salt, saltstack, salt-ssh,api, rest_api
Category: SaltStack
Slug: salt-ssh-api-01
Author: pengyao
Summary: Salt 2015.5版本增加了SSH Python API及REST API的支持, 对其做下功能测试

Salt 2015.5版本增加了SSH Python API及REST API的支持, 那么该怎么使用? 是否可以直接在生产环境中使用? 本文将对其进行测试.

## 前置阅读

* [Salt SSH教程](http://docs.saltstack.com/en/latest/topics/ssh/)
* [Salt Roster教程](http://docs.saltstack.com/en/latest/topics/ssh/roster.html)

## 环境说明

* CentOS 6.5 with EPEL
* salt-ssh/salt-minion/salt-api版本为: 2015.5.1
* salt-api采用[rest_cherrypy](http://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html)
* salt minion主机名为: minion-01.example.com, IP为: 192.168.33.225
* salt minion主机测试用户名为: root, 密码为vagrant

## 开工

### 配置Roster

本次采用[Flat Roster](http://docs.saltstack.com/en/latest/ref/roster/all/salt.roster.flat.html#module-salt.roster.flat)

*/etc/salt/roster:*

```yaml
minion-01.example.com:
  host: 192.168.33.225
  user: root
  passwd: vagrant
```

测试salt-ssh:

```bash
salt-ssh -i '*' test.ping
```

指定*-i*参数是为了SSH第一次连接, 能够自动将目标SSH Server的DSA Key记入~/.ssh/known_hosts而不进行提示.

如果roster文件中没有指定user和passwd, 也可以在运行salt-ssh命令时指定如下参数:

```bash
salt-ssh -i --user='root' --passwd='vagrant' '*' test.ping
```

输出如下:

```yaml
minion-01.example.com:
    True
```

### 测试SSH Python API

代码如下:

```python
from salt.client.ssh.client import SSHClient
client = SSHClient()
print client.cmd(tgt='*', fun='test.ping')
```

如果roster中并没有指定username和passwd, 也可以在client.cmd中进行指定:

```python
print client.cmd(tgt='*', fun='test.ping', salt_user='root', salt_passwd='vagrant')
```

输出为:

```
{'minion-01.example.com': {'fun_args': [], 'jid': '20150603121617516520', 'return': True, 'retcode': 0, 'fun': 'test.ping', 'id': 'minion-01.example.com'}}
```

目前SSH Python API支持 [cmd](https://github.com/saltstack/salt/blob/v2015.5.1/salt/client/ssh/client.py#L84)(执行完毕后统一返回结果)及[cmd_iter](https://github.com/saltstack/salt/blob/v2015.5.1/salt/client/ssh/client.py#L57)(以迭代器的方式返回结果)两个接口. 目前并不支持异步接口

### 测试SSH REST API

* 以下操作如非特别说明, 均在Master端执行

*/etc/salt/master.d/api.conf:*

```yaml
rest_cherrypy:
  port: 8000
  disable_ssl: True
```

重启Salt API, 以使配置生效

```bash
service salt-api restart
```

测试:

```bash
curl http://localhost:8000/run \
-H 'Accept: application/x-yaml' \
-d client='ssh' \
-d tgt='*' \
-d fun='test.ping'
```

输出如下:

```yaml
return:
- minion-01.example.com:
    fun: test.ping
    fun_args: []
    id: minion-01.example.com
    jid: '20150603142036393178'
    retcode: 0
    return: true
```

按照官方的说法, salt-ssh并不支持eauth, 其认证应该通过自身的SSH层进行. 而当前版本并不能直接传递用于salt-ssh的用户名和密码, 需要先在Roster中进行指定或者部署SSH无密码认证后才能使用, 灵活性较差. [该问题已经反馈给Salt官方](https://github.com/saltstack/salt/issues/24358), 期待未来版本会有一个好的解决方案.

由于该SSH REST API接口不支持认证, 相当于接口直接暴露出来, 所以如果在生产环境中使用本接口, 需要做好安全控制.

## 总结

Salt SSH的加入, 给Salt架构上带来了新的选择. 目前Salt SSH的功能还没有达到Master/Minion结构的水准(主要是因为Master/Minion结构水准太高), 不过从最近的几个版本Release Note来看, Salt SSH功能在不断的增强, 强烈关注.

回到本文本身, 从测试结果看, 当前2015.5.1版本中的Salt SSH API, 其Python API与Salt SSH命令行可以达到同样的功能, 可以在生产环境中使用. 而由于NetAPI中认证功能的缺失, 并**不推荐**直接在生产环境中使用.



