import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep

class TestRkantor(unittest.TestCase):
    """
    class containing different simple input/output fields tests, and tests of data extraction
    from elements
    """

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.site = "https://www.rkantor.com/"

    def select_option_by_id(self, driver, id_name, choice_value):
        elem = driver.find_element_by_id(id_name)
        v = "value"
        all_options = elem.find_elements_by_tag_name("option")
        for option in all_options:
            if option.get_attribute("value") == choice_value:
                print(f"clicked {option.get_attribute(v)}")
                option.click()

    def delete_obscuring_elements(self, driver):
        delete_element_script = """
        var elem = document.querySelector("#callpageWrapper");
        elem.remove();
        """
        coockies = driver.find_element_by_id("accept-cookies")
        coockies.click()
        sleep(3)
        driver.execute_script(delete_element_script)

    def test_simpletest(self):
        """
        checks if page opens
        :return: "Kantor" in title assertion
        """
        driver = self.driver
        driver.get(self.site)
        print(f"test 0: {driver.title}")
        assert "Kantor" in driver.title

    def test_task_1(self):
        """
        go to site, fill in specific values into calculator and obtain a calculated value of exchange

        reason for "double selecting" is that unfortunately site responds first time as selecting always first option
        from available options, second selection attempts to fix that

        many times throughout this test there are sleeps, to take time for UI to respond and events to trigger on site,
        also it is nice to see what it does while it works

        during the time selenium goes to fields to fill/make a selection, there are 2 elements that event triggers add
        to the document that has to be removed due to UI obscuring inputs. JS script attempts to remove those and fix
        UI.

        :return: EUR to PLN exchange values
        """
        driver = self.driver
        driver.get(self.site)

        money_exchange_field = driver.find_element_by_id("calc-amount")
        money_exchange_field.clear()
        money_exchange_field.send_keys("1234,56")
        self.delete_obscuring_elements(driver)

        self.select_option_by_id(driver, "currency1", "EUR")
        self.select_option_by_id(driver, "currency1", "EUR")
        sleep(3)
        self.select_option_by_id(driver, "currency2", "PLN")
        self.select_option_by_id(driver, "currency2", "PLN")
        sleep(3)
        self.select_option_by_id(driver, "calc-bank", "ING")
        sleep(3)

        # driver.find_element_by_id("new-savings-form-submit").click()
        # ^ doesn't work since getting "not clickable element in point (185,850) due to object p obscuring"
        money_exchange_field.send_keys(Keys.ENTER)
        sleep(3)

        results = {"money_exchange_service_value": driver.find_element_by_id("nc-first-price").text,
                   "bank_exchange_value": driver.find_element_by_id("nc-second-price").text,
                   "exchange_gain": driver.find_element_by_id("nc-savings").text}
        print("test 1:")
        for key in results:
            print(results[key])
            assert results[key] is not None

    def test_task_2(self):
        """
        this test attempts to read bank names from specific document section
        :return:
        """
        driver = self.driver
        driver.get(self.site)
        banks_list = driver.find_element_by_id(
            "free-transfer").find_element_by_tag_name(
            "ul").find_elements_by_tag_name("li")
        print(len(banks_list))
        banks = dict()
        i = 1
        for elem in banks_list:
            bank_text = elem.find_element_by_class_name("txt").text
            banks[str(i)] = bank_text
            i += 1
        for k in banks:
            print(f"{k}: {banks[k]}")
        assert banks["16"]
        assert len(banks_list) == 16

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()