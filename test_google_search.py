import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class GoogleSearchTest(unittest.TestCase):
    
    def setUp(self):
        """This method will run before every test case to set up the WebDriver."""
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get('https://www.google.com')
    
    def test_title(self):
        """Test that the page title is 'Google'."""
        self.assertEqual(self.driver.title, "Google")

   def test_no_results_for_random_string(self):
    """Test that a random string yields no relevant results."""
    search_box = self.driver.find_element('name', 'q')
    search_box.send_keys('fhqwhgadsxxzzyy')  # Using a random string that likely has no results
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    self.driver.implicitly_wait(5)

    # Check for the absence of results by looking for the "Did you mean:" text
    # If this text is present, it indicates that there were suggestions, thus, results were found
    did_you_mean = self.driver.find_elements('xpath', "//*[contains(text(), 'Did you mean')]")
    self.assertFalse(did_you_mean, "Search returned results when none were expected")
    
    # Alternatively, we can check for any search result links or elements
    search_results = self.driver.find_elements('css selector', 'h3')  # Check for result titles (h3 tags)
    self.assertEqual(len(search_results), 0, "Search results should be empty but found some")


    def test_search_suggestions(self):
        """Test that search suggestions appear when typing in the search box."""
        search_box = self.driver.find_element('name', 'q')
        search_box.send_keys('Selenium')
        
        # Wait for the suggestions to load
        self.driver.implicitly_wait(5)

        # Check if suggestions are displayed
        suggestions = self.driver.find_elements('xpath', "//ul[@role='listbox']/li")
        self.assertGreater(len(suggestions), 0, "No search suggestions found")

    def test_search_image_results(self):
        """Test that the image search tab is accessible after performing a search."""
        search_box = self.driver.find_element('name', 'q')
        search_box.send_keys('Kittens')
        search_box.send_keys(Keys.RETURN)
        
        # Wait for the results to load
        self.driver.implicitly_wait(5)

        # Click on the "Images" link
        images_link = self.driver.find_element('link text', 'Images')
        images_link.click()
        
        # Wait for image results to load
        self.driver.implicitly_wait(5)

        # Check for the presence of an image result
        image_results = self.driver.find_elements('css selector', "img")
        self.assertGreater(len(image_results), 0, "No images found in image search results")

    def test_search_videos_results(self):
        """Test that the video search tab is accessible after performing a search."""
        search_box = self.driver.find_element('name', 'q')
        search_box.send_keys('Nature videos')
        search_box.send_keys(Keys.RETURN)
        
        # Wait for the results to load
        self.driver.implicitly_wait(5)

        # Click on the "Videos" link
        videos_link = self.driver.find_element('link text', 'Videos')
        videos_link.click()
        
        # Check that the URL contains 'tbm=vid' indicating video search
        self.assertIn('tbm=vid', self.driver.current_url)

  

    def tearDown(self):
        """This method will run after every test case to close the browser."""
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
