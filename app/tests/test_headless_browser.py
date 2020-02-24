from threading import Thread

from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from app.models import Domain, Client, Credential, Offset


class HeadlessTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        domain = Domain(name='selenium', url='selenium.org', chunk_size=10)
        domain.save()

        for i in range(0, 20):
            domain.username_set.create(username='username{}'.format(i))
        domain.username_set.create(username='ansible')
        for i in range(0, 20):
            domain.password_set.create(password='password{}'.format(i))
        domain.password_set.create(password='yankees')

        options = Options()
        options.headless = True

        cls.drivers = [
            WebDriver(options=options),
            WebDriver(options=options),
            WebDriver(options=options),
            WebDriver(options=options)
        ]

    def test_exfiltration(self):

        threads = []

        def visit_page(driver):
            print('call {}'.format(self.live_server_url))
            driver.get("{}/app/selenium/".format(self.live_server_url))

        for i in range(0, 4):
            t = Thread(target=visit_page, args=(self.drivers[i],))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.assertTrue(Credential.objects.filter(username='ansible', password='yankees').exists(),
                        'Credentials not found : {}'.format(list(Credential.objects.all())))

        print('End of test, clients : {}'.format(list(Client.objects.all())))

    @classmethod
    def tearDownClass(cls):
        for driver in cls.drivers:
            driver.quit()
        super().tearDownClass()
