from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from typing import List
import time
def parse_flats(city:str, flat_types:List[str]) -> None:
    """Парсит данные о квартирах с веб-страницы и сохраняет их в формате JSON.

    Args:
        city (str): Название города, данные о квартирах которого необходимо парсить.
        flat_types (List[str]): Список типов квартир для парсинга.

    Returns:
        None

    Description:
        Эта функция открывает веб-страницу для указанного города и типов квартир,
        последовательно переходит по страницам с помощью кнопок "Следующая",
        извлекает данные о квартирах из сетевых запросов и сохраняет их в формате JSON.

    """
    driver = webdriver.Firefox()
    for flat_type in flat_types:
        driver.get(f'https://{city}.etagi.com/{flat_type}/')
        while True:
            try:
                next_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[class="jJShB Y5bqE _jBUx GmYmq zPhuj"]')
                for button in next_buttons:
                    if button.text == "Следующая":
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="jJShB Y5bqE _jBUx GmYmq zPhuj"]')))
                        button.click()
                        break
                else:
                    break
            except Exception as e:
                print(e)
                continue
            time.sleep(0.5)
    lst = []
    for request in driver.requests:
        if request.response:
            if 'FlatsWithCharacteristics' in request.url:
                response = request.response
                body = decode(response.body, response.headers.get('Content-Encoding', 'identity'))
                body_content = body.decode("utf-8")
                try:
                    data_dict = json.loads(body_content)
                    if 'data' in data_dict:
                        lst.extend(data_dict['data'])
                except json.JSONDecodeError:
                    print("Ошибка декодирования JSON для запроса:", request.url)
    driver.quit()
    with open(f"{city}.json", "w", encoding="utf-8") as f:
        json.dump(lst, f, ensure_ascii=False, indent=4)

city = "msk"
types = ["realty"]
parse_flats(city, types)