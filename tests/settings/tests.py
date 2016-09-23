from wego import settings, api, exceptions
import unittest


class TestSettingsInit(unittest.TestCase):

    def test_init(self):
        a = settings.init(
            APP_ID='1',
            APP_SECRET='1',
            REGISTER_URL='www.quseit.com/',
            REDIRECT_PATH='/',
            MCH_ID='1',
            MCH_SECRET='1',
            PAY_NOTIFY_PATH='/a',
            HELPER='wego.helpers.official.DjangoHelper',
            CERT_PEM_PATH='/',
            KEY_PEM_PATH='2'
        )
        self.assertTrue(isinstance(a, api.WegoApi))

    def test_error(self):
        with self.assertRaises(exceptions.InitError):
            settings.init(
                APP_SECRET='1',
                REGISTER_URL='/',
                REDIRECT_PATH='1',
                MCH_ID='1',
                MCH_SECRET='1',
                PAY_NOTIFY_PATH='/a',
                HELPER='wego.helpers.official.DjangoHelper'
            )

        with self.assertRaises(AttributeError):
            settings.init(
                APP_ID='1',
                APP_SECRET='1',
                REGISTER_URL='/',
                REDIRECT_PATH='/',
                MCH_ID='1',
                MCH_SECRET='1',
                PAY_NOTIFY_PATH='/a',
                HELPER='wego.helpers.official.ErrorHelper',
                KEY_PEM_PATH='2',
                CERT_PEM_PATH='1'
            )


if __name__ == '__main__':
    unittest.main()
