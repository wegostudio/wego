<p align="center"><a href="http://vuejs.org" target="_blank"><img width="100"src="http://ww2.sinaimg.cn/large/62e721e4gw1f83zeuykk5j20sg0sgtb6.jpg"></a></p>

## WEGO

一个简单易用的微信开发框架，能协助你在微信开发中专注业务逻辑摆脱微信接口调试的烦恼。

## Example

<p align="center">
    <img width="220"src="http://ww2.sinaimg.cn/large/62e721e4gw1f8bd8tn1kwj20a90a9gmt.jpg"><br/><br/>
    微信扫一扫查看示例公众号
</p>

## Install

```
$ pip(3) install wego
```

## Usage

```
# django
@w.login_required
def index(request):
    hello = 'Hello %s!' % request.wx_user.nickname
    return HttpResponse(hello)

# tornado
class IndexHandler(tornado.web.RequestHandler):
    @w.login_required
    def get(self):
        hello = 'Hello %s!' % self.wx_user.nickname
        return self.write(hello)
```

## Document

未完成，持续更新中: [wego.readthedocs.io](http://wego.readthedocs.io/zh_CN/latest/)

## Discuss

<table>
    <tr>
        <td><img src="http://ww1.sinaimg.cn/mw690/c41e7f9agw1f8xnci4vhfj20kw0r2tam.jpg" width="142"></td>
        <td><img src="http://ww2.sinaimg.cn/large/62e721e4gw1f84078j40pj207s07st9m.jpg" width="142"></td>
    </tr>
    <tr>
        <td>微信群</td>
        <td>Telegram</td>
    </tr>
</table>
<p>如果微信群二维码过期，请加微信river4，备注wego user即可。</p>
<p>如果有商务合作建议或者有企业支持的需求，请加微信river4。</p>


## Donate

<table>
    <tr>
        <td><img src="http://ww3.sinaimg.cn/mw690/c41e7f9agw1f8xp9au5pgj20e80e8abz.jpg" width="142"></td>
        <td><img src="" width="142"></td>
    </tr>
    <tr>
        <td>通过支付宝捐助</td>
        <td></td>
    </tr>
</table>
Wego项目是由优趣工作室（QuseitLab）开发并提供支持，我们将会一如既往地推进开源，造福大众，感谢您捐助我们。


## License

[Apache](http://www.apache.org/licenses/)


