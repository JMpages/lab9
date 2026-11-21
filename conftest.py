import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura de pantalla automática en caso de fallo"""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs['driver']
        screenshot = driver.get_screenshot_as_base64()
        html = (
            f'<div><img src="data:image/png;base64,{screenshot}" '
            f'alt="screenshot" style="width:304px;height:228px;" '
            f'onclick="window.open(this.src)" align="right"/></div>'
        )
        extras.append(pytest_html.extras.html(html))

    report.extras = extras

@pytest.fixture
def driver():
    """Fixture del navegador configurada para ejecución local y CI/CD"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()