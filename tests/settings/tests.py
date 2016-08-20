from wego import settings, wechat
import unittest


class TestSettingsInit(unittest.TestCase):

    def test_init(self):
        a = settings.init(
            APP_ID='1',
            APP_SECRET='1',
            REGISTER_URL='/',
            REDIRECT_URL='1',
            MCH_ID='1',
            MCH_SECRET='1',
            HELPER='wego.helpers.django_helper'
        )
        self.assertTrue(isinstance(a, wechat.wechat_api))


if __name__ == '__main__':
    unittest.main()