from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
import sys

class NewVisitorTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Acceder a la
        #webpage
        self.browser.get(self.server_url)

        #Ver como se llama el sitio web
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        #Descubrir la posibilidad de escribir un elemento
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
            )

        #Escribir "Buy peacock feathers"
        #dentro de la caja de texto
        inputbox.send_keys('Buy peacock feathers')

        #Darle al 'intro' y enviar
        #el texto
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/+')

        #Introducir un nuevo elemento en la lista
        #'Use peacock feathers to make a fly'
        #y ver el resultado

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        #nuevo usuario, Francias el del Actual

        #Vamos cerrarlo todo para que no haya problemas
        #entre un usuario y otro

        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Francis entra a la principal, no debe haber restos de la
        #anterior usuaria, Edith.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)


        #Francis comienza una nueva lista
        #Es menos interesante que Edith
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        #Ahora Francis tiene una URL exclusiva
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        #Volvemos a comprobar que no hay rastro de Edith
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertIn('Buy milk', page_text)

        #Satisfecho, ambos se acuestan
        
        #self.fail('Finish the test')

        #visita a la web, la lista sigue en su sitio

        #fin de la visita.

    def test_layout_and_styling(self):

        #Edith va la pagina principal
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024,768)

        #Se da cuenta de que la entrada de datos esta entrada
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width'] / 2,
            512,
            delta=5
        )

        #Comienza una nueva lista y se percata de que la entrada de texto
        #esta igual de primorosamente centrada
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width'] / 2,
            512,
            delta=5
        )
        
        



