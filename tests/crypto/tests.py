from wego.lib.WEGOBizMsgCrypt import WXBizMsgCrypt
import unittest

class TestSettingsInit(unittest.TestCase):

    def test_encrypt(self):
        to_xml = """ <xml><ToUserName><![CDATA[oia2TjjewbmiOUlr6X-1crbLOvLw]]></ToUserName><FromUserName><![CDATA[gh_7f083739789a]]></FromUserName><CreateTime>1407743423</CreateTime><MsgType>  <![CDATA[video]]></MsgType><Video><MediaId><![CDATA[eYJ1MbwPRJtOvIEabaxHs7TX2D-HV71s79GUxqdUkjm6Gs2Ed1KF3ulAOA9H1xG0]]></MediaId><Title><![CDATA[testCallBackReplyVideo]]></Title><Descript  ion><![CDATA[testCallBackReplyVideo]]></Description></Video></xml>"""
        token = "spamtest"
        nonce = "1320562132"
        appid = "wx2c2769f8efd9abc2"
        encryp_test = WXBizMsgCrypt(token,encodingAESKey,appid)
        ret,encrypt_xml = encryp_test.EncryptMsg(to_xml,nonce)   
        self.assertEqual(ret, 0)

    def test_encrypt(self):
        encodingAESKey = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG" 
        token = "spamtest"
        timestamp = "1409735669"
        appid = "wx2c2769f8efd9abc2"
        nonce = "1320562132"
        msg_sign  = "5d197aaffba7e9b25a30732f161a50dee96bd5fa"   

        from_xml = """<xml><ToUserName><![CDATA[gh_10f6c3c3ac5a]]></ToUserName><FromUserName><![CDATA[oyORnuP8q7ou2gfYjqLzSIWZf0rs]]></FromUserName><CreateTime>1409735668</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[abcdteT]]></Content><MsgId>6054768590064713728</MsgId><Encrypt><![CDATA[hyzAe4OzmOMbd6TvGdIOO6uBmdJoD0Fk53REIHvxYtJlE2B655HuD0m8KUePWB3+LrPXo87wzQ1QLvbeUgmBM4x6F8PGHQHFVAFmOD2LdJF9FrXpbUAh0B5GIItb52sn896wVsMSHGuPE328HnRGBcrS7C41IzDWyWNlZkyyXwon8T332jisa+h6tEDYsVticbSnyU8dKOIbgU6ux5VTjg3yt+WGzjlpKn6NPhRjpA912xMezR4kw6KWwMrCVKSVCZciVGCgavjIQ6X8tCOp3yZbGpy0VxpAe+77TszTfRd5RJSVO/HTnifJpXgCSUdUue1v6h0EIBYYI1BD1DlD+C0CR8e6OewpusjZ4uBl9FyJvnhvQl+q5rv1ixrcpCumEPo5MJSgM9ehVsNPfUM669WuMyVWQLCzpu9GhglF2PE=]]></Encrypt></xml>"""
        decrypt_test = WXBizMsgCrypt(token,encodingAESKey,appid)
        ret ,decryp_xml = decrypt_test.DecryptMsg(from_xml, msg_sign, timestamp, nonce)
        self.assertEqual(ret, 0)