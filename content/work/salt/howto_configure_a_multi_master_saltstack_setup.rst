【翻译】如何建立多Master的SaltStack环境
########################################

:date: 2013-09-25
:tags: saltstack, multi-master, 多master, howto
:category: SaltStack
:slug: howto_configure_a_multi_master_saltstack_setup
:author: pengyao
:summary: 翻译的《How To Configure A Multi-Master SaltStack Setup》

* 英文原文出处: http://intothesaltmine.org/how_to_configure_a_multi_master_saltstack_setup.html

0.16.0版本的发布，带来了minion可以连接多Master的特性. 这种方式称为多master( ``multi-master`` )配置, 使环境中的SaltStack冗余。在这种配置下，Salt Minions将连接所有配置的Salt Master. 本文将带你了解如何建立多Master的环境.

Master Keys
===============

在建立多Master的配置中，主要的一点就是所有的Master使用同样的private key. 这些key将在Master第一次启动时自动生成。 因此在多Master环境建立时，需要从原始的(original) Master上拷贝其private key至第二个Master以提供它启动时自动生成的那个, 以此类推.

Master的private key存储在Master本地的 ``pki_dir`` 目录下. 默认的目录是 ``/etc/salt/pki/master/master.pem`` . 将该key拷贝到新增的master上. 需要注意的是，在拷贝的时候，需要确保新增的master上并没有minion连接进来.

Configure Minions
======================

当配置多Master时，Minion需要知道需要连接的每个Master的网络地址. 需要在Minion的配置文件中进行配置，默认的配置文件是 ``/etc/salt/minion`` 。 找到 ``master`` 配置项, 更新需要新增的Master.

下边是一个多Master的配置例子:

.. code-block:: yaml

    master:
      - master1.example.tld
      - master2.example.tld

配置完毕后，需要重启Minion以确保配置生效. 此时所有的Master均可以控制你的minions.


Sharing Files Between Masters
=================================

Salt并不会自动在Master间共享文件. 本小节将带你了解Master间哪些文件需要同步以保持一致.

Minion Keys
----------------------

Minion的keys需要每个Master都进行accept. 可以使用 ``salt-key`` 手动接接受minion的key， 也可以在Master间保持key目录的同步. 需要同步的目录有:

* /etc/salt/pki/master/minions
* /etc/salt/pki/master/minions_pre
* /etc/salt/pki/master/minions_rejected

.. note::

  直接共享 ``/etc/salt/master`` 目录是强烈反对的. 允许外部访问 master.pem key将带来严重的安全风险


file_roots
-----------------

``file_roots`` 的内容需要在Master间同步以保持一致. 这里存放Salt State配置管理文件. 推荐同步内容使用 ``gitfs`` backend，或者直接将 ``file_roots`` 存储在共享存储上.

pillar_roots
----------------

同理，对于 ``pillar_roots`` 也是如此，需要保持Pillar数据一致.

Master Configuration
---------------------------

最后你需要确保有关Master的配置选项在所有Master间是同步的. 除非你知道你不需要这么做,你需要保证以下的设置Master间是同步的:

    * external_auth
    * client_acl
    * peer
    * peer_run


Conslusion
==================

多Master环境配置提供了控制Minions的冗余性，配置相当简单. 只需要保证key及State文件在你的多Master间是同步的，你就可以透明的在多Master上控制你的Minions
