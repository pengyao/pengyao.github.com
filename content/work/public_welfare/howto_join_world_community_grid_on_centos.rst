CentOS平台上如何加入World Community Grid参与运算
#####################################################

:date: 2013-12-10
:tags: CentOS, EPEL, World Community Grid,世界公共网格, boinc
:category: Public_Welfare
:slug: howto_join_world_community_grid_on_centos
:author: pengyao
:summary: `World Community Grid`_ 是一项基于互联网的公益性分布式计算项目，该项目联合分布在各地的自愿者们提供的计算资源，用于一些能够为全人类带来福音的大型科技研究项目。 当手头有CentOS操作系统的计算资源，安装上 `Boinc`_ client, 进行简单配置即可参与计算。

`Wikipedia`_ 对 `World Communtiy Grid <http://zh.wikipedia.org/wiki/%E4%B8%96%E7%95%8C%E5%85%AC%E5%85%B1%E7%BD%91%E6%A0%BC>`_ 有如下描述::

    World Community Grid，中文译名为“世界社群网格”、“世界共同体网格计划”或“世界公共网格”。是由IBM公司主持的一项基于互联网的公益性分布式计算项目，开始于2004年11月16日。该项目将联合分布于世界各地的志愿者们提供的计算资源，用于一些能为全人类带来福音的大型科学研究项目。
    
    World Community Grid 创立之初是基于 Grid.org 的平台搭建的，之后于 2007 年开始全面迁移至开源的 BOINC 平台。World Community Grid 在底层计算平台的基础上，为具体的计算项目提供了一个更高层次的计算平台。

    
如果手头刚好有空闲的计算资源, 只需要安装上 `Boinc`_ client，进行简单的配置即可参与计算，贡献自己的一份力量,本文以 `CentOS`_ 为例进行说明。

注册World Community Grid账户
********************************

访问: `World Community Grid 注册URL <https://secure.worldcommunitygrid.org/reg/viewRegister.do>`_ 进行账户注册。注册完毕后，可以在 *settings* 中设置参与哪些项目的运算，并在My Profile页面获取到 *Weak Account Key*.

安装配置Boinc Client
************************
`EPEL`_ 中已经有了 `Boinc`_ client软件包，直接进行安装。如果你还没有安装EPEL，请在进行以下操作前先进行EPEL的安装。

**安装boinc-client**

.. code-block:: bash

    yum install boinc-client

**配置boinc-client**

.. code-block:: bash

    echo 'BOINCOPTS="--daemon --attach_project www.worldcommunitygrid.org/ weak_account_key"' >>/etc/sysconfig/boinc-client

.. note::

    请将命令中的 *weak_account_key* 替换为之前在My Profile页面获取到的 *Weak Account Key*

**启动boinc-client**

.. code-block:: bash

    chkconfig boinc-client on
    service boinc-client start

查看已参与运算的设备信息
****************************
安装配置boinc-client并运行后，访问 `World Community Grid`_ 的 `Device Manager <https://secure.worldcommunitygrid.org/ms/device/viewDevices.do>`_ 即可查询到当前已参与运算的设备信息。

Technology solving problems!


.. _Wikipedia: http://www.wikipedia.org/
.. _World Community Grid: http://www.worldcommunitygrid.org/
.. _Boinc: http://boinc.berkeley.edu/
.. _CentOS: http://www.centos.org/
.. _EPEL: http://fedoraproject.org/wiki/EPEL/zh-cn
