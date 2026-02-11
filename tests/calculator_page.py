import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver

    def load_page(self):
        file_path = os.path.abspath("../src/index.html")
        self.driver.get(f"file://{file_path}")

    def is_loaded(self):
        return (
                self.driver.find_element(By.ID, "num1").is_displayed()
                and self.driver.find_element(By.ID, "num2").is_displayed()
                and self.driver.find_element(By.ID, "operation").is_displayed()
                and self.driver.find_element(By.ID, "calculate").is_displayed()
        )

    def clear_numbers(self):
        self.driver.find_element(By.ID, "num1").clear()
        self.driver.find_element(By.ID, "num2").clear()

    def enter_first_number(self, value):
        self.driver.find_element(By.ID, "num1").send_keys(str(value))

    def enter_second_number(self, value):
        self.driver.find_element(By.ID, "num2").send_keys(str(value))

    def select_operation(self, operation):
        select = Select(self.driver.find_element(By.ID, "operation"))
        select.select_by_value(operation)

    def click_calculate(self):
        self.driver.find_element(By.ID, "calculate").click()

    def get_result(self):
        # Attend que le texte ne soit plus vide
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(By.ID, "result").text.strip() != ""
        )
        return self.driver.find_element(By.ID, "result").text

    def wait_for_calculator_container(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "calculator"))
        )

    def get_input_sizes(self):
        num1 = self.driver.find_element(By.ID, "num1")
        num2 = self.driver.find_element(By.ID, "num2")
        return num1.size, num2.size

    def get_button_size(self):
        calc_btn = self.driver.find_element(By.ID, "calculate")
        return calc_btn.size

    def get_button_colors(self):
        calc_btn = self.driver.find_element(By.ID, "calculate")
        btn_bg = calc_btn.value_of_css_property("background-color")
        btn_color = calc_btn.value_of_css_property("color")
        return btn_bg, btn_color
