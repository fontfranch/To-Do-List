from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Acceder a la
        #webpage
        self.browser.get('http://localhost:8000')

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

        #Introducir un nuevo elemento en la lista
        #'Use peacock feathers to make a fly'
        #y ver el resultado

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers',[row.text for row in rows])
        self.assertIn('2: Use peacock feathers to make a fly',[row.text for row in rows])
        
        self.fail('Finish the test')

        

if __name__ == '__main__':
    unittest.main(warnings='ignore')


