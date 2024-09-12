import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import shutil

def clear_directory(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Не удалось удалить {file_path}. Причина: {e}')

# Путь к директории
directory_path = r'C:\task1'
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
clear_directory(directory_path)

# Настройка пути для скачивания
download_dir = directory_path

# Настройка WebDriver с указанием пути для скачивания файлов
chrome_options = webdriver.ChromeOptions()
prefs = {
    'download.default_directory': download_dir,
    'download.prompt_for_download': False,  # Отключает запрос на сохранение
    'safebrowsing.enabled': True  # Включает безопасное скачивание
}
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=chrome_options)


try:
    # Переходит на сайт
    driver.get('https://www.rpachallenge.com/')

    # Качает файл Excel
    download_link = driver.find_element(By.XPATH, '//a[contains(@href, "challenge.xlsx")]')
    download_link.click()

    # Ждет, пока файл не будет загружен
    file_path = os.path.join(download_dir, 'challenge.xlsx')
    for _ in range(10):  # Попробуем максимум 10 раз
        if os.path.exists(file_path):
            break
        time.sleep(1)

    # Проверяет, существует ли файл
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Файл {file_path} не найден.')

    # Загружает данные из Excel
    data = pd.read_excel(file_path)

    # Выводит имена столбцов
    print(data.columns)

    # Нажимает кнопку "Start"
    start_button = driver.find_element(By.XPATH, '//button[text()="Start"]')
    start_button.click()

    # Ждет, чтобы формы появились
    time.sleep(1)
    
    data.columns = data.columns.str.strip()

    # Заполняет формы
    for index, row in data.iterrows():
        driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelFirstName"]').send_keys(row['First Name'])
        driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelLastName"]').send_keys(row['Last Name'])
        driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelCompanyName"]').send_keys(row['Company Name'])
        driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelRole"]').send_keys(row['Role in Company'])
        driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelAddress"]').send_keys(row['Address'])
        driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelEmail"]').send_keys(row['Email'])
        driver.find_element(By.XPATH, '//input[@ng-reflect-name="labelPhone"]').send_keys(str(row['Phone Number']))

        # Жмет кнопку "Submit"
        submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
        submit_button.click()

        # Ждет, чтобы формы обновились
        time.sleep(1)

    # Делает скриншот результата
    driver.save_screenshot(os.path.join(download_dir, 'result.png'))

finally:
    # Закрывает браузер
    driver.quit()
