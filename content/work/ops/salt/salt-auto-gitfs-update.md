Title: Salt自动化之自动更新Gitfs
Date: 2015-05-26
Tags: Salt, saltstack, gitfs, reactor, webhook, rest_api
Category: SaltStack
Slug: salt-auto-gitfs-update
Author: pengyao
Summary: Salt API提供Webhook功能, 同时基于Reactor实现git提交代码至仓库后自动更新Gitfs

Salt支持[Gitfs](http://docs.saltstack.com/en/latest/topics/tutorials/gitfs.html), 可以将State Tree放入Git远程仓库中, 进行版本控制, 易于管理. 当提交更新至远程Git仓库后, 需要手动在Master执行如下操作:

```bash
salt-run fileserver.update
```

或者等待一段时间,由Master的maintenance进程进行更新(默认更新间隔为60s, 可以通过master配置文件 *loop_interval* 选项进行调整). 那么有没有一种方案, 能够实现Push代码至Git仓库后, 自动触发Gitfs的更新哪? 

常见的Git仓库管理系统, 如Gitlab, Github, Bitbucket都支持Webhook功能, 即当Push代码至仓库时, 能够自动触发外部Webhook调用, 而Salt API提供Webhook功能, 可以通过Webhook触发Event, Reactor系统又能基于Event进行Salt自动化管理, 看看可以就此入手, 实现Gitfs自动更新方案.

## 前置阅读

* [Salt Gitfs教程](http://docs.saltstack.com/en/latest/topics/tutorials/gitfs.html)
* [Salt REST_CHERRYPY教程](http://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.htm)
* [Salt Reactor教程](http://docs.saltstack.com/en/latest/topics/reactor/)

## 环境说明

* CentOS 6.5 With EPEL
* salt-master及salt-api版本2015.5.0
* Master端已安装python-pygit2
* Master端已安装Nginx(用于salt-api安全防护)
* 本次采用Github作为远程仓库Demo
* 本次采用临时域名*salt-api-demo.pengyao.org*进行测试, 请根据自己真实环境进行调整

## 开工
* 以下操作, 如非说明, 均在Master端进行

### 配置Salt API

*/etc/salt/master.d/api.conf*

```yaml
rest_cherrypy:
  port: 8000
  host: 127.0.0.1
  debug: True
  disable_ssl: True
  webhook_url: /hook
  webhook_disable_auth: True
```
由于第三方Webhook部分并不支持认证功能, 所以关闭了webhook认证(*webhook_disable_auth*参数)

重启Salt API服务, 以使配置生效

```bash
service salt-api restart
```

由于关闭了Webhook认证, 意味着公网所有人都可以触发本Webhook, 所以Master端安装了Nginx对Webhook接口增加Basic Auth认证功能

*/etc/nginx/conf.d/salt-api-demo.pengyao.org.conf*

```
upstream salt-api-demo {
  server 127.0.0.1:8000;
}

server {
  listen 80;
  server_name salt-api-demo.pengyao.org;

  location / {
    proxy_pass  http://salt-api-demo;
  }
  location /hook {
    proxy_pass  http://salt-api-demo;
    auth_basic  "salt api demo";
    auth_basic_user_file  /opt/htpasswd;
  }
}
```

重启Nginx服务, 以使配置生效

```bash
service nginx restart
```

创建Basic Auth用户文件:

```bash
echo "demo:$(echo -n demo_pass |openssl passwd -stdin)"  > /opt/htpasswd
```

Master下载eventlisten.py, 监听Event

```bash
wget https://raw.githubusercontent.com/saltstack/salt/develop/tests/eventlisten.py
python eventlisten.py
```

开启新窗口, 手动触发webhook, 进行测试

```
curl http://demo:demo_pass@salt-api-demo.pengyao.org/hook/test -XPOST -d "demo=True"
```

运行eventlisten.py的控制台有如下输出:

```
Event fired at Tue May 26 00:33:04 2015
*************************
Tag: salt/netapi/hook/test
Data:
{'_stamp': '2015-05-25T16:33:04.425532',
 'body': '',
 'headers': {'Accept': '*/*',
             'Authorization': 'Basic ZGVtbzpkZW1vX3Bhc3M=',
             'Connection': 'close',
             'Content-Length': '9',
             'Content-Type': 'application/x-www-form-urlencoded',
             'Host': 'salt-api-demo',
             'Remote-Addr': '127.0.0.1',
             'User-Agent': 'curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.14.0.0 zlib/1.2.3 libidn/1.18 libssh2/1.4.2'},
 'post': {'demo': 'True'}}
```

webhook测试达到预期

### 建立远程仓库

登陆[Github](https://github.com/pengyao/)建立远程仓库, 本次Demo仓库地址: https://github.com/pengyao/salt-gitfs-demo.git

### 配置Gitfs

*/etc/salt/master.d/gitfs.conf*

```yaml
# Gitfs backend
fileserver_backend:
  - git

# Gitfs provider
gitfs_provider: pygit2

# Gitfs repositories
gitfs_remotes:
  - https://github.com/pengyao/salt-gitfs-demo.git
```

重启Salt Master服务, 以使配置生效

```bash
service salt-master restart
```

重启完毕后, 获取gitfs中的文件列表(启动时, 会自动触发拉取最新的远程仓库代码)

```bash
salt-run fileserver.file_list
```

输出如下:

```yaml
- README
```

### 配置Reactor

*/etc/salt/master.d/reactor.conf*

```yaml
reactor:
  - 'salt/netapi/hook/gitfs/*':
    - /srv/reactor/gitfs.sls
```

*/srv/reactor/gitfs.sls*

```
{% if 'gitfs/update' in tag %}
gitfs_update:
  runner.fileserver.update
{% endif %}
```

重启Salt Master服务, 以使配置生效

```bash
service salt-master restart
```

重启完毕后, 测试webhook:

```bash
curl http://demo:demo_pass@salt-api-demo.pengyao.org/hook/gitfs/update -XPOST -d "demo=True"
```

运行eventlisten.py的窗口, 有如下输出:

```
Event fired at Tue May 26 00:49:11 2015
*************************
Tag: salt/netapi/hook/gitfs/update
Data:
{'_stamp': '2015-05-25T16:49:11.694576',
 'body': '',
 'headers': {'Accept': '*/*',
             'Authorization': 'Basic ZGVtbzpkZW1vX3Bhc3M=',
             'Connection': 'close',
             'Content-Length': '9',
             'Content-Type': 'application/x-www-form-urlencoded',
             'Host': 'salt-api-demo',
             'Remote-Addr': '127.0.0.1',
             'User-Agent': 'curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.14.0.0 zlib/1.2.3 libidn/1.18 libssh2/1.4.2'},
 'post': {'demo': 'True'}}
Event fired at Tue May 26 00:49:11 2015
*************************
Tag: salt/event/new_client
Data:
{'_stamp': '2015-05-25T16:49:11.737823'}
Event fired at Tue May 26 00:49:11 2015
*************************
Tag: salt/run/20150526004911736899/new
Data:
{'_stamp': '2015-05-25T16:49:11.742807',
 'fun': 'runner.fileserver.update',
 'jid': '20150526004911736899',
 'user': 'Reactor'}
Event fired at Tue May 26 00:49:14 2015
*************************
Tag: salt/run/20150526004911736899/ret
Data:
{'_stamp': '2015-05-25T16:49:14.168910',
 'fun': 'runner.fileserver.update',
 'jid': '20150526004911736899',
 'return': True,
 'success': True,
 'user': 'Reactor'}
```

可以看到, 本次测试, 产生了4条event:

1. webhook产生, 对应Tag为: salt/netapi/hook/gitfs/update
2. 由于配置的有对应的Reactor, 所以会自动创建Reactor线程, 产生第二条Event
3. 产生的Reactor线程在获取对应的sls发现需要运行*runner.fileserver.update*任务, 所以自动创建该任务, 对应的Tag为: salt/run/$jid/new
4. runner任务结果返回, 对应的Tag为: salt/run/$jid/ret

测试达到预期

### 配置GitHub Webhook

进入[项目配置页面](https://github.com/pengyao/salt-gitfs-demo/settings), 选择"Webhooks & Services"左侧导航条, 选择 "Add Webhook", 分别输入如下内容:

* Payload URL: http://demo:demo_pass@salt-api-demo.pengyao.org/hook/gitfs/update

输入完毕后, 选择 *Add Webhook*进行保存

### 自动更新Gitfs测试

本地clone本项目, 进行如下操作:

```bash
git clone git@github.com:pengyao/salt-gitfs-demo.git
cd salt-gitfs-demo
echo "I am a test" > test
git add -A
git commit -m "add test"
git push -u origin master
```

git push后, 在运行eventlisten.py窗口, 有如下输出:

```
Event fired at Tue May 26 01:04:15 2015
*************************
Tag: salt/netapi/hook/gitfs/update
Data:
{'_stamp': '2015-05-25T17:04:15.495458',
 'body': '{"ref":"refs/heads/master","before":"efe61d0816e4f34c7c0117945ef2383a4183ac26","after":"e2264a6386bf5c6b8ec6daee0ddca3155b4e3ccc","created":false,"deleted":false,"forced":false,"base_ref":null,"compare":"https://github.com/pengyao/salt-gitfs-demo/compare/efe61d0816e4...e2264a6386bf","commits"
 ......此处省略若干字......
 Event fired at Tue May 26 01:04:15 2015
*************************
Tag: salt/event/new_client
Data:
{'_stamp': '2015-05-25T17:04:15.523955'}
Event fired at Tue May 26 01:04:15 2015
*************************
Tag: salt/run/20150526010415522645/new
Data:
{'_stamp': '2015-05-25T17:04:15.529005',
 'fun': 'runner.fileserver.update',
 'jid': '20150526010415522645',
 'user': 'Reactor'}
Event fired at Tue May 26 01:04:19 2015
*************************
Tag: salt/run/20150526010415522645/ret
Data:
{'_stamp': '2015-05-25T17:04:19.393239',
 'fun': 'runner.fileserver.update',
 'jid': '20150526010415522645',
 'return': True,
 'success': True,
 'user': 'Reactor'}
```

检查gitfs仓库文件列表:

```bash
salt-run fileserver.file_list
```

输出如下:

```
- README
- test
```

达到预期

## 结束语

Reactor系统的加入, Salt插上智能化的翅膀, 轻松甩开竞争对手几条街. 简单易用的Salt REST API接口, 更易于和第三方系统整合, 使Salt轻松成为运维系统自动化引擎. 

人生苦短, 我用Salt!

欢迎加入[中国SaltStack用户组](http://www.saltstack.cn/)
