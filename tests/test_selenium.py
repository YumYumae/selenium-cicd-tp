import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

from calculator_page import CalculatorPage


class TestCalculator:
    @pytest.fixture(scope="class")
    def driver(self):
        """Configuration du driver Chrome pour les tests"""
        chrome_options = Options()
        # Configuration pour environnement CI/CD
        if os.getenv("CI"):
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_page_loads(self, driver):
        """Test 1: Vérifier que la page se charge correctement"""
        page = CalculatorPage(driver)
        page.load_page()

        # Vérifier le titre
        assert "Calculatrice Simple" in driver.title

        # Vérifier la présence des éléments principaux
        assert page.is_loaded()

    def test_addition(self, driver):
        """Test 2: Tester l'addition"""
        page = CalculatorPage(driver)
        page.load_page()

        page.enter_first_number("10")
        page.enter_second_number("5")
        page.select_operation("add")
        page.click_calculate()

        assert "Résultat: 15" in page.get_result()

    def test_division_by_zero(self, driver):
        """Test 3: Tester la division par zéro"""
        page = CalculatorPage(driver)
        page.load_page()

        page.clear_numbers()
        page.enter_first_number("10")
        page.enter_second_number("0")
        page.select_operation("divide")
        page.click_calculate()

        assert "Erreur: Division par zéro" in page.get_result()

    def test_all_operations(self, driver):
        """Test 4: Tester toutes les opérations"""
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
            time.sleep(1)

    def test_page_load_time(self, driver):
        """Test 5: Mesurer le temps de chargement de la page"""
        page = CalculatorPage(driver)

        start_time = time.time()
        page.load_page()

        page.wait_for_calculator_container()

        load_time = time.time() - start_time
        print(f"Temps de chargement: {load_time:.2f} secondes")

        assert load_time < 3.0, f"Page trop lente à charger: {load_time:.2f}s"

    def test_decimal_numbers(self, driver):
        """Test 5.1: Tester avec des nombres décimaux"""
        page = CalculatorPage(driver)
        page.load_page()

        page.clear_numbers()
        page.enter_first_number("10.5")
        page.enter_second_number("2.25")
        page.select_operation("add")
        page.click_calculate()

        assert "Résultat: 12.75" in page.get_result()

    def test_negative_numbers(self, driver):
        """Test 5.2: Tester avec des nombres négatifs"""
        page = CalculatorPage(driver)
        page.load_page()

        page.clear_numbers()
        page.enter_first_number("-8")
        page.enter_second_number("2")
        page.select_operation("subtract")
        page.click_calculate()

        assert "Résultat: -10" in page.get_result()

    def test_ui_styles(self, driver):
        """Test 5.3: Tester l'interface utilisateur (couleurs, tailles)"""
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
