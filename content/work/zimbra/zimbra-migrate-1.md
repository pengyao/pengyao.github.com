Title: Zimbra迁移资料
Date: 2013-08-26
Author: pengyao
Slug: zimbra-migrate-1
Tag: Zimbra, migrate
Category: Zimbra
Summary:  整理用到的Zimbra迁移资料(不定期更新)

近期Mail系统迁移至[Zimbra][], 整理下迁移过程中用到的资料.

Zimbra Wiki: <http://wiki.zimbra.com/wiki/>

## 迁移后防止用户通过POP重复接收之前的邮件 ##
* 参考资料: <http://wiki.zimbra.com/wiki/Prevent_duplicates_messages_for_POP3_users_post_migration>

POP3 Server会对每一个进入的邮件分配个唯一的数字(unique number, UIDL)，POP3的客户端下载邮件时会对比UIDL，这样就可以避开了同一封邮件重复接收的问题，只会下载新的UIDL邮件.

由于迁移了新的Server,邮件的UIDL并不做提供，因此会导致POP3客户端认为所有的邮件都是新的，导致邮件重复下载。解决方法为迁移后执行如下内容:

    # su - zimbra
    # zmpro ma <account> zimbraPrefPop3DownloadSince $(date "+%Y%m%d%H%M%S"Z)


