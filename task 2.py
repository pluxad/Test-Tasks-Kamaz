from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from collections import Counter

# Настройка драйвера
driver = webdriver.Chrome()

try:
    # Переходит на сайт
    driver.get("https://www.arealme.com/colors/ru/")
    
    # Дает время странице загрузиться
    time.sleep(5)

    # ожидание, чтобы кнопка стала кликабельной
    start_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'progress-button'))
    )
    start_button.click()

    # Начало цикла
    start_time = time.time()
    while time.time() - start_time < 80:  # 80 секунд
        try:
            # Находит все div элементы с классом patra-color
            containers = driver.find_elements(By.CSS_SELECTOR, "div.patra-color div")
            
            for container in containers:
                # Находит все span элементы внутри контейнера
                spans = container.find_elements(By.TAG_NAME, "span")
                
                # Получает цвета каждого span
                colors = [driver.execute_script("return window.getComputedStyle(arguments[0]).backgroundColor;", span) for span in spans]
                
                # Подсчитывает количество каждого цвета
                color_count = Counter(colors)
                
                # Находит уникальный цвет
                unique_color = [color for color, count in color_count.items() if count == 1]
                
                if unique_color:
                    # Находит индекс уникального цвета
                    unique_index = colors.index(unique_color[0])
                    
                    # Кликает по элементу с уникальным цветом
                    unique_span = spans[unique_index]
                    driver.execute_script("arguments[0].click();", unique_span)
                    
                    # Задержка
                    time.sleep(0.1)

        except Exception as e:
            print(f"Ошибка при поиске элементов: {e}")
            break

finally:
    # Закрывает браузер
    driver.quit()
