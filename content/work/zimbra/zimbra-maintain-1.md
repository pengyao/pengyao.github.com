Title: Zimbra维护资料
Date: 2013-08-26
Author: pengyao
Slug: zimbra-maintain-1
Tags: zimbra, maintain
Category: Zimbra
Summary: 整理常用的Zimbra维护资料(不定期更新)

近期Mail系统切换至[Zimbra][], 整理下日常维护中用到的资料.

Zimbra Wiki: http://wiki.zimbra.com/wiki/

## 重置Admin密码 ##
* 参考资料: http://wiki.zimbra.com/wiki/Admin_Password_Reset

    # su - zimbra
    $ zmprov sp <admin email address> <new password> 
    $ zmprov gaaa                        //列出当前所有administrator账户

## Web Client切换为HTTPS ##
* 参考资料: http://www.zimbra.com/docs/os/6.0.8/administration_guide/A_app-command-line.13.13.html

zmtlsctl [metod]，支持的metod如下:
</p>
<table class="wiki">
<tr><th> method </th><th> 描述 </th><th> 备注 
</th></tr><tr><td>http</td><td>只提供HTTP的访问方式</td><td>-
</td></tr><tr><td>https</td><td>只提供HTTPS的访问方式，只允许使用<a class="ext-link" href="https://访问，不允许使用http://访问"><span class="icon">​</span>https://访问，不允许使用http://访问</a></td><td>-
</td></tr><tr><td>mixed</td><td>如果用户使用htt://访问，登录时将自动切换成https://，登录完成后普通session流量将使用http://， 如果用户使用<a class="ext-link" href="https://访问，将一直使用https://"><span class="icon">​</span>https://访问，将一直使用https://</a></td><td>-
</td></tr><tr><td>both</td><td>用户可以使用<a class="ext-link" href="http://和https://访问"><span class="icon">​</span>http://和https://访问</a></td><td>-
</td></tr><tr><td>redirect</td><td>如果用户使用<a class="ext-link" href="http://访问，将自动切换成https://进行之后的所有访问"><span class="icon">​</span>http://访问，将自动切换成https://进行之后的所有访问</a></td><td>-
</td></tr></table>

切换方法:

    # su - zimbra
    $ zmtlsctl redirect
    $ zmmailboxdctl restart




[Zimbra]: http://www.zimbra.com/

