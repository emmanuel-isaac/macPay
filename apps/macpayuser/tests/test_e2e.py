import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.test.client import Client
from django.utils.importlib import import_module

def create_session_store():
    """ Creates a session storage object. """

    engine = import_module(settings.SESSION_ENGINE)
    # Implement a database session store object that will contain the session key.
    store = engine.SessionStore()
    store.save()
    return store

class HomePage(unittest.TestCase):
    def setUp(self):
        password = 'mypassword' 
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
        self.driver = webdriver.Firefox()

    def test_home_page(self):
        driver = self.driver
        # Create a session object from the session store object.
        session_items = create_session_store()

        driver.get("http://127.0.0.1:8000/login")
        self.assertIn("MacPay", driver.title) 
        login = driver.find_element_by_id("login_to_continue").click()
        username = driver.find_element_by_name("username")
        username.send_keys("andela")
        password= driver.find_element_by_name("password")
        password.send_keys("andela")
        submit = driver.find_element_by_name("action").click()

        # Add a session key/value pair.
        session_items['sessionid'] = 'c9rf510ewmexa6zbwcydr9fkx8kmmgoe'
        session_items.save()
        driver.add_cookie({'name':'sessionid', 'value': 'c9rf510ewmexa6zbwcydr9fkx8kmmgoe'})

        driver.get("http://127.0.0.1:8000/dashboard/")  
        #check for pagination
        paginate = driver.find_element_by_css_selector("#fellows-table tbody")
        #check if paginated items in current page is no more than 20
        self.assertLessEqual(len(paginate.find_elements_by_tag_name("tr")), 20)
        #Go to next page and check same 
        next_page = driver.find_element_by_id("fellows-table_next").click()
        self.assertLessEqual(len(paginate.find_elements_by_tag_name("tr")), 20)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

