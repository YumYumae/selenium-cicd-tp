import pytest
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from calculator_page import CalculatorPage


class TestCalculator:
    @pytest.fixture(scope="class")
    def driver(self):
        chrome_options = Options()

        if os.getenv("CI"):
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_page_loads(self, driver):
        page = CalculatorPage(driver)
        page.load_page()
        assert "Calculatrice Simple" in driver.title
        assert page.is_loaded()

    def test_addition(self, driver):
        page = CalculatorPage(driver)
        page.load_page()
        page.enter_first_number("10")
        page.enter_second_number("5")
        page.select_operation("add")
        page.click_calculate()
        assert "Résultat: 15" in page.get_result()

    def test_division_by_zero(self, driver):
        page = CalculatorPage(driver)
        page.load_page()
        page.clear_numbers()
        page.enter_first_number("10")
        page.enter_second_number("0")
        page.select_operation("divide")
        page.click_calculate()
        assert "Erreur: Division par zéro" in page.get_result()

    def test_all_operations(self, driver):
        page = CalculatorPage(driver)
        page.load_page()

        operations = [
            ("add", "8", "2", "10"),
            ("subtract", "8", "2", "6"),
            ("multiply", "8", "2", "16"),
            ("divide", "8", "2", "4"),
        ]

        for op, num1, num2, expected in operations:
            page.clear_numbers()
            page.enter_first_number(num1)
            page.enter_second_number(num2)
            page.select_operation(op)
            page.click_calculate()
            assert f"Résultat: {expected}" in page.get_result()
            time.sleep(0.5)

    def test_page_load_time(self, driver):
        page = CalculatorPage(driver)
        start_time = time.time()
        page.load_page()
        page.wait_for_calculator_container()
        load_time = time.time() - start_time
        print(f"Temps de chargement: {load_time:.2f} secondes")
        assert load_time < 3.0

    def test_decimal_numbers(self, driver):
        """
        Test 5.1: Décimaux
        On tente d'abord avec '.', puis avec ',' si l'app est en format FR.
        """
        page = CalculatorPage(driver)
        page.load_page()

        # Tentative 1: format point
        page.clear_numbers()
        page.enter_first_number("10.5")
        page.enter_second_number("2.25")
        page.select_operation("add")
        page.click_calculate()

        try:
            res = page.get_result(timeout=3)
            assert "12.75" in res
            return
        except Exception:
            pass

        # Tentative 2: format virgule (FR)
        page.load_page()
        page.clear_numbers()
        page.enter_first_number("10,5")
        page.enter_second_number("2,25")
        page.select_operation("add")
        page.click_calculate()

        res = page.get_result(timeout=5)
        # Selon l'affichage possible: "12.75" ou "12,75"
        assert ("12.75" in res) or ("12,75" in res)

    def test_negative_numbers(self, driver):
        page = CalculatorPage(driver)
        page.load_page()
        page.clear_numbers()
        page.enter_first_number("-8")
        page.enter_second_number("2")
        page.select_operation("subtract")
        page.click_calculate()
        assert "-10" in page.get_result()

    def test_ui_styles(self, driver):
        page = CalculatorPage(driver)
        page.load_page()

        num1_size, num2_size = page.get_input_sizes()
        btn_size = page.get_button_size()

        assert num1_size["width"] > 100
        assert num1_size["height"] > 20
        assert num2_size["width"] > 100
        assert num2_size["height"] > 20

        assert btn_size["width"] > 80
        assert btn_size["height"] > 25

        btn_bg, btn_color = page.get_button_colors()
        assert btn_bg is not None and btn_bg != ""
        assert btn_color is not None and btn_color != ""


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
