import unittest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class TestCheckLcwLocators(unittest.TestCase):
    baseUrl = "https://www.lcwaikiki.com/tr-TR/TR"

    MENU = (By.LINK_TEXT, "KADIN")
    SUB_CAT = (By.LINK_TEXT, "Pijama Takımı")
    PRODUCT = (By.CLASS_NAME, "product-card__product-info")
    SIZE = (By.CSS_SELECTOR, "#option-size a:not([data-stock*='0']")
    ADD_TO_CART_BUTTON = (By.LINK_TEXT, "SEPETE EKLE")
    CART_ITEM_COUNT = (By.CLASS_NAME, "badge-circle")
    HOME_PAGE_LOGO = (By.CLASS_NAME, "main-header-logo")

    def setUp(self):
        option = Options()
        option.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=option)
        self.driver.maximize_window()
        self.driver.get(self.baseUrl)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.implicitly_wait(15)

    def test_lcw_check(self):
        self.driver.get(self.baseUrl)
        self.assertIn('LC Waikiki', self.driver.title)

        kadin = self.driver.find_element(*self.MENU)
        hover = ActionChains(self.driver).move_to_element(kadin)
        hover.perform()

        self.driver.find_element(*self.SUB_CAT).click()
        self.assertIn('Kadın Pijama', self.driver.title.split(",")[0])

        self.driver.find_elements(*self.PRODUCT)[2].click()
        self.assertTrue(self.wait.until(
            EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)).text)

        self.driver.find_element(*self.SIZE).click()
        self.driver.find_element(*self.ADD_TO_CART_BUTTON).click()

        self.driver.find_element(*self.CART_ITEM_COUNT).click()
        self.assertEqual("https://www.lcwaikiki.com/tr-TR/TR/sepetim", self.driver.current_url)

        self.driver.find_element(*self.HOME_PAGE_LOGO).click()
        self.assertIn('LC Waikiki', self.driver.title)

    def tearDown(self):
        self.driver.close()
