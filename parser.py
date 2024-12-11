from playwright.sync_api import sync_playwright
import json
import os
import time
from urllib.parse import urlparse
import requests
import re

class CarParser:
    def __init__(self):
        pass
        
    def parse_car_page(self, url):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            
            try:
                page = context.new_page()
                page.goto(url, wait_until='networkidle')
                page.wait_for_selector('.head-info_price-wrap__Y4bxi', timeout=30000)
                
                # Получаем название и год
                car_title = page.locator('.line-1.tw-flex-1').inner_text()
                print(f"Найдено название: {car_title}")
                
                # Получаем цены с более точными селекторами
                price_block = page.locator('.head-info_price-wrap__Y4bxi')
                
                # Получаем текстовые значения цен
                new_car_price_text = price_block.locator('p:has-text("新车指导价")').inner_text()
                saving_text = price_block.locator('p:has-text("比新车省")').inner_text()
                
                print(f"Цена нового авто: {new_car_price_text}")
                print(f"Экономия: {saving_text}")
                
                # Извлекаем числовые значения
                new_car_match = re.search(r'(\d+\.?\d*)', new_car_price_text)
                saving_match = re.search(r'(\d+\.?\d*)', saving_text)
                
                if new_car_match and saving_match:
                    new_car_price = float(new_car_match.group(1))
                    saving = float(saving_match.group(1))
                    current_price = new_car_price - saving
                else:
                    raise Exception("Не удалось извлечь числовые значения из цен")
                
                price_info = {
                    'current_price': f"{current_price:.2f}万",
                    'new_car_price': f"{new_car_price}万",
                    'saving': f"{saving}万"
                }
                
                print(f"Обработанные цены: {price_info}")
                
                # Получаем изображения
                images = []
                img_elements = page.query_selector_all('ul[data-log-view] img[src*="dcarimg.com"]')
                for img in img_elements:
                    src = img.get_attribute('src')
                    if src:
                        if not src.startswith('http'):
                            src = 'https:' + src
                        images.append(src)
                
                print(f"Найдено изображений: {len(images)}")
                
                car_id = urlparse(url).path.split('/')[-1]
                car_dir = f"cars/{car_id}"
                os.makedirs(car_dir, exist_ok=True)
                
                car_data = {
                    "title": car_title,
                    "prices": price_info,
                    "url": url,
                    "images": images
                }
                
                # Сохраняем JSON
                with open(f"{car_dir}/info.json", 'w', encoding='utf-8') as f:
                    json.dump(car_data, f, ensure_ascii=False, indent=4)
                
                # Скачиваем изображения
                self.download_images(images, car_dir)
                
                return car_data
                
            except Exception as e:
                print(f"Ошибка при парсинге: {str(e)}")
                return None
            finally:
                context.close()
                browser.close()

    def download_images(self, image_urls, save_dir):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.dongchedi.com/'
        }
        
        for i, url in enumerate(image_urls):
            try:
                print(f"Скачивание изображения {i+1}: {url}")
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    image_path = f"{save_dir}/image_{i+1}.webp"
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Изображение сохранено: {image_path}")
                time.sleep(0.5)
            except Exception as e:
                print(f"Ошибка при скачивании изображения {url}: {str(e)}")