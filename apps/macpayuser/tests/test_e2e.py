import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.test.client import Client
from django.utils.importlib import import_module

driver = webdriver.Firefox()

def create_session_store():
    """ Creates a session storage object. """

    engine = import_module(settings.SESSION_ENGINE)
    # Implement a database session store object that will contain the session key.
    store = engine.SessionStore()
    store.save()
    return store

class Dashboard(unittest.TestCase):
    def setUp(self):
        session_items = create_session_store()

        driver.get("http://127.0.0.1:8000/login")
        self.assertIn("MacPay", driver.title) 
        driver.find_element_by_id("login_to_continue").click()
        username = driver.find_element_by_name("username")
        username.send_keys("andela")
        password= driver.find_element_by_name("password")
        password.send_keys("andela")
        driver.find_element_by_name("action").click()

        session_items['sessionid'] = 'c9rf510ewmexa6zbwcydr9fkx8kmmgoe'
        session_items.save()
        driver.add_cookie({'name':'sessionid', 'value': 'c9rf510ewmexa6zbwcydr9fkx8kmmgoe'})  

    def test_dashboard(self):     
        driver.maximize_window()  
        driver.get("http://127.0.0.1:8000/dashboard/") 
        self.assertLessEqual(len(driver.find_elements_by_class_name("fellows-list")), 20)
        #Go to next page and check same 
        #driver.find_element_by_id("fellows-table_next")
        #self.assertLessEqual(len(driver.find_elements_by_class_name("fellows-list")), 20)

        search = driver.find_element_by_tag_name("input")
        search.send_keys("Kosi")

    def tearDown(self):
        driver.close()

if __name__ == "__main__":
    unittest.main()

