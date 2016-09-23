<p align="center"><a href="http://vuejs.org" target="_blank"><img width="100"src="http://ww2.sinaimg.cn/large/62e721e4gw1f83zeuykk5j20sg0sgtb6.jpg"></a></p>

## WEGO

一个简单易用的微信开发框架，能协助你在微信开发中专注业务逻辑摆脱微信接口调试的烦恼。

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

未完成，持续更新中: [wegostudio.github.io/wego/](https://wegostudio.github.io/wego/)

## Discuss

<table>
    <tr>
        <td><img src="http://ww2.sinaimg.cn/large/62e721e4gw1f84040ds0pj207s07st9m.jpg" style="width: 142px"></td>
        <td><img src="http://ww2.sinaimg.cn/large/62e721e4gw1f84078j40pj207s07st9m.jpg" style="width: 142px"></td>
    </tr>
    <tr>
        <td>微信群</td>
        <td>Telegram</td>
    </tr>
</table>

## License

[Apache](http://www.apache.org/licenses/)


