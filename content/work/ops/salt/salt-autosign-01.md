Title: Salt之AutoSign那点事
Date: 2015-05-04
Tags: Salt, saltstack, autosign, reactor
Category: SaltStack
Slug: salt-autosign-01
Author: pengyao
Summary: Salt内置AutoSign功能, 同时Auth时会产生Event, 也可以基于Reactor完成AutoSign功能


Salt基于安全考虑, Minion在连接Master时, 需要在Master端先接受Minion的Pub Key, 之后Minion才能解密Master发过来的指令. 

如果Minion数目较少, 可以直接使用*salt-key*来管理Minion的keys. 如果规模较大, 维护Key将变得麻烦起来. 为此Salt提供了如下几种AutoSign的方案:

### open_mode

**默认值**: False

**使用方法**: Master配置文件中增加 `open_mode: True`, 并重启Master以使配置生效

**推荐指数**: **-1**

说明: 该选项开启后, Master将关闭Auth功能, 并告诉master接受所有认证. 生产环境中**强烈不推荐**使用该选项

### auth_accept

**默认值**: False

**使用方法**: Master配置文件中增加 `auth_accept: True`, 并重启Master以使配置生效

**推荐指数**: **0**

该选项开启后, Master将自动接受所有minion发过来的Pub Key. 生产环境中**不推荐**使用该选项

### autosign_file

**默认值**: 无

**使用方法**: Master配置文件中增加 `autosign_file: /etc/salt/autosign.conf`, 并重启Master以使配置生效. 之后编辑autosign_file, 增加autosign minion_id匹配规则(无需重启Master)

**推荐指数**: **5**

该选项开启后, master接收到minion的Pub Key后, 会逐行读取autosign_file(所以更新autosign_file无需重启Master), 一旦匹配, 直接Accept. minion_id匹配规则支持字符完全匹配, Glob匹配, 正则匹配.

如想匹配`minion-01.example.com`, 则如下条目均可匹配:

```bash
minion-01.example.com     # 字符完全匹配
minion-*.example.com      # Glob匹配
minion-\d+\.example\.com  # 正则匹配
```

### autosign_time

**默认值**: 120   (单位: 分)

**使用方法**: 该选项只是指定下autosign_dir目录下minion_id文件有效期为多长时间, 可以根据实际情况调整该参数. 想进行autosign时, 只需要在autosign_dir目录(默认: */etc/salt/pki/master/minions_autosign/*)下创建需要自动Accept的minion_id文件即可. 在文件创建后的autosign_time时间内, minion进行auth时会直接Accept并自动删除本文件. 文件超过有效期, 将自动删除本文件.

**推荐指数**: **8**

相对于*autosign_file*参数, 该方法支持有效期功能, 劣势是只支持字符完全匹配.

### Reactor

适用等级: 高

推荐指数: **10**

Salt底层构建了Event BUS, 操作均会产生Event, 如Auth相关, 就会产生tag为*salt/auth*的event. 所以可以基于Reactor构建一个autosign方案, 灵活性要强与Salt内置的autosign方案.

直接上Demo:

*/srv/reactor/autosign.sls*

```python
#!py

import logging

log = logging.getLogger(__name__)

def check_autosign(minion_id):
    if minion_id.endswith('example.com'):
        return True
    return False

def run():
    '''
    Autosign demo by reactor
    '''
    minion_id = data['id']
    if data.get('act') == 'pend' and check_autosign(minion_id):
        log.info('I will accept {0} key by reactor'.format(minion_id))
        return {
            'minion_add': {
                'wheel.key.accept': [{
                    'match': minion_id}]
            }
        }
    return {}
```

Minion在启动连接Master时, 会将自己的Pub Key发送给Master, Master未Accept时, 会产生一条playload中*act*为*pend*的event. 可以自定义check_autosign函数, 进行判断该minion是否需要autosign, 如果需要, 则借助[*wheel*的key模块](http://docs.saltstack.com/en/latest/ref/wheel/all/salt.wheel.key.html#salt.wheel.key.accept "wheel.key")进行自动Accept该minion public key.

*/etc/salt/master.d/reactor.conf*

```yaml
reactor:
  - 'salt/auth':
    - /srv/reactor/autosign.sls
```

发现tag为*salt/auth*的event, 则触发*/srv/reactor/autosign.sls*的执行, 从而实现AutoSign功能



 

















