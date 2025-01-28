from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import sys
import time

chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-proxy-server")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--dns-prefetch-disable")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-ssl-errors')

while True:

    driver = webdriver.Chrome(options=chrome_options)
    # driver.implicitly_wait(2)
    driver.get("https://www.accuweather.com/")


    city = input("Enter city name to check the weather forecast: ")
    print(f"Data collection for location: {city}. Please be patient...")
    location = ""
    back_to_start = False
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_weather = {"alert": "Brak"}
    next_days_weather = {}


    #Agreements confirmation
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "p.fc-button-label"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.banner-button.policy-accept"))).click()

    #City input to search bar
    search_bar = driver.find_element(By.CSS_SELECTOR, "input.search-input")
    search_bar.send_keys(city)

    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "p.search-bar-result__name"))).text.lower() == city.lower()
    except Exception as e:
        back_to_start = True
        print(f"Location not found (\"{city}\").\nCheck if you have entered the name of the town correctly.")
        time.sleep(2)
        
    if back_to_start == True:
        continue
    else:
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH,f"//p[@class='search-bar-result__name' and translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{city.lower()}']"))).click()
        except Exception as e:
            print(f"Location not found (\"{city}\").\nCheck if you have entered the name of the town correctly.")
            time.sleep(5)
            sys.exit()

        #Collecting weather data
        location = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.header-loc"))).text

        try:
            current_weather["alert"] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.severe-alert-banner__type"))).text
        except TimeoutException :
            pass

        current_weather["sky"] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.phrase"))).text
        current_weather["ambient_temperature"] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='temp-container'] div[class='temp']"))).text
        current_weather["perceived_temperature"] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='temp-container'] div[class='real-feel']"))).text[10:]+"C"
        current_weather["wind"] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='cur-con-weather-card__panel details-container'] div:nth-child(1) span:nth-child(2)"))).text
        current_weather["wind_gusts"] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='cur-con-weather-card__panel details-container'] div:nth-child(2) span:nth-child(2)"))).text
        current_weather["air_quality"] = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='cur-con-weather-card__panel details-container'] div:nth-child(3) span:nth-child(2)"))).text

        next_days_weather[WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='two-column-page-content '] a:nth-child(1) div:nth-child(1) p:nth-child(1)"))).text] = [WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(1) div:nth-child(1) p:nth-child(2)"))).text, (WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(1) div:nth-child(3) span:nth-child(1)"))).text)+"C", WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(1) div:nth-child(4) p:nth-child(1)"))).text, WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(1) div:nth-child(5)"))).text]

        next_days_weather[WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='two-column-page-content '] a:nth-child(2) div:nth-child(1) p:nth-child(1)"))).text] = [WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(2) div:nth-child(1) p:nth-child(2)"))).text, (WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(2) div:nth-child(3) span:nth-child(1)"))).text)+"C", WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(2) div:nth-child(4) p:nth-child(1)"))).text, WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(2) div:nth-child(5)"))).text]

        next_days_weather[WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='two-column-page-content '] a:nth-child(3) div:nth-child(1) p:nth-child(1)"))).text] = [WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(3) div:nth-child(1) p:nth-child(2)"))).text, (WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(3) div:nth-child(3) span:nth-child(1)"))).text)+"C", WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(3) div:nth-child(4) p:nth-child(1)"))).text, WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(3) div:nth-child(5)"))).text]

        next_days_weather[WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='two-column-page-content '] a:nth-child(4) div:nth-child(1) p:nth-child(1)"))).text] = [WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(4) div:nth-child(1) p:nth-child(2)"))).text, (WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(4) div:nth-child(3) span:nth-child(1)"))).text)+"C", WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(4) div:nth-child(4) p:nth-child(1)"))).text, WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(4) div:nth-child(5)"))).text]

        next_days_weather[WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='two-column-page-content '] a:nth-child(5) div:nth-child(1) p:nth-child(1)"))).text] = [WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(5) div:nth-child(1) p:nth-child(2)"))).text, (WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(5) div:nth-child(3) span:nth-child(1)"))).text)+"C", WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(5) div:nth-child(4) p:nth-child(1)"))).text, WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='daily-list content-module'] a:nth-child(5) div:nth-child(5)"))).text]

        # Returning data
        print("\nWeather forecast for: " + location + ", on day: " + current_datetime+"\n")
        print("Alerts: "+ current_weather["alert"])
        print("Cloud cover: "+ current_weather["sky"])
        print("Ambient temperature: "+ current_weather["ambient_temperature"])
        print("Apparent temperature: "+ current_weather["perceived_temperature"])
        print("Wind: "+ current_weather["wind"])
        print("Wind gusts: "+ current_weather["wind_gusts"])
        print("Air quality: "+ current_weather["air_quality"]+"\n")
        print("Forecast for the next few days:" )
        for key,value in next_days_weather.items():
            tekst = (
                f"{key} ({value[0]}): "
                f"Temperature: {value[1]}, "
                f"Cloud cover: {value[2]}, "
                f"Precipitation probability: {value[3]}"
            )
            print(tekst)

        answer = input("\nIf you want to choose another location, enter: \"yes\", to finish type any letter...").strip().lower()
        
        if answer == "yes":
            continue
        else:
            print("Thank you and see you soon!")
            time.sleep(1)
            break
