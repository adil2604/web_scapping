### Kazpost  

---  

> **_NOTE:_**  You need to download ChromeDriver for Selenium (https://chromedriver.chromium.org/downloads) and add into PATH.  



##### Proxy
In root we have`settings.py` that have `get_proxies()` functions. Use this if need proxy list. **By default, it's not used.**

### Before run

 - You should install all required packages in `requirements.txt`.
 -  If you  don’t have a file `cities.txt,`then use the function `get_cities ()`   in `kazpost_models.py`  to parse cities. Same for **proxies**.
 
