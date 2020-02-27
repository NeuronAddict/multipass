from threading import Thread

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from app.models import Domain, Client, Credential


class credentials_found(object):
    """
    An expectation for checking that credentials are found.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, driver):
        return Credential.objects.filter(username=self.username, password=self.password).exists()


@override_settings(DEBUG=True)
class HeadlessTest(StaticLiveServerTestCase):
    """
    This test must be run with postgresql
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        domain = Domain(name='example', url='selenium.org', chunk_size=2)
        domain.save()

        for i in range(0, 10):
            domain.username_set.create(username='username{}'.format(i))
        domain.username_set.create(username='ansible')
        for i in range(0, 10):
            domain.password_set.create(password='password{}'.format(i))
        domain.password_set.create(password='yankees')

        options = Options()
        options.add_argument('-headless')
        options.headless = True

        d = DesiredCapabilities.FIREFOX
        d['loggingPrefs'] = {'browser': 'ALL'}

        cls.drivers = [
            Firefox(firefox_options=options, desired_capabilities=d),
            Firefox(firefox_options=options, desired_capabilities=d),
            Firefox(firefox_options=options, desired_capabilities=d),
            Firefox(firefox_options=options, desired_capabilities=d)
        ]

    def test_exfiltration(self):

        found_creds = False
        threads = []

        def visit_page(driver):
            try:
                global found_creds
                driver.get("{}/app/example/".format(self.live_server_url))
                wait = WebDriverWait(driver, 15)
                try:
                    wait.until(credentials_found('ansible', 'yankees'))
                except TimeoutException as e:
                    for entry in driver.get_log('browser'):
                        print(entry)
                    raise e

                print('creds found ...')
                found_creds = True
            finally:
                driver.quit()

        for driver in self.drivers:
            t = Thread(target=visit_page, args=(driver,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        # self.assertTrue(found_creds, 'Credentials not found : {}'.format(list(Credential.objects.all())))
        self.assert_credentials_found()

        print('End of test, clients : {}'.format(list(Client.objects.all())))

    def assert_credentials_found(self):
        self.assertTrue(Credential.objects.filter(username='ansible', password='yankees').exists(),
                        'Credentials not found : {}'.format(list(Credential.objects.all())))
