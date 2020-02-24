from threading import Thread

from django.test import LiveServerTestCase
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from app.models import Domain, Client, Credential


class HeadlessTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        domain = Domain(name='selenium', url='selenium.org', chunk_size=2)
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

        cls.drivers = [
            Firefox(firefox_options=options),
            Firefox(firefox_options=options),
            Firefox(firefox_options=options),
            Firefox(firefox_options=options)
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
        # noinspection PyUnresolvedReferences
        for driver in cls.drivers:
            driver.quit()
        super().tearDownClass()
