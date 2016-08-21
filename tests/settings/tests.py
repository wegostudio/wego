from wego import settings, wechat, exceptions
import unittest


class TestSettingsInit(unittest.TestCase):

    def test_init(self):
        a = settings.init(
            APP_ID='1',
            APP_SECRET='1',
            REGISTER_URL='/',
            REDIRECT_PATH='1',
            MCH_ID='1',
            MCH_SECRET='1',
            HELPER='wego.helpers.official.DjangoHelper'
        )
        self.assertTrue(isinstance(a, wechat.WechatApi))

    def test_error(self):
        with self.assertRaises(exceptions.InitError):
            settings.init(
                APP_SECRET='1',
                REGISTER_URL='/',
                REDIRECT_PATH='1',
                MCH_ID='1',
                MCH_SECRET='1',
                HELPER='wego.helpers.official.DjangoHelper'
            )


if __name__ == '__main__':
    unittest.main()