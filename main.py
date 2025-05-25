import requests
import json

## These top imports we will use to prompt local ollama server & format responses
### Now say we want to pass a fun variable to this generation ## This model is text based so it will have to do. 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    print(f"Moving to {url} and gathering content.")
    ## Use body as it will contain most of the bulk of info
    text = driver.find_element(By.TAG_NAME, 'body').text
    driver.quit()
    print(f"Closing.")

    return text

interest = "Julius_Caesar"
language = "en"

url = f"https://{language}.wikipedia.org/wiki/{interest}"
text = get_page(url)

content = text
print(f"Text gathered.")

def generate_response(content: str, model="mistral"):
    url = "http://localhost:11434/api/generate"
    system_prompt = f"Make a historical summary of, do not repeat yourself and ignore information that is not relevant to the main subject:"
    payload = {
        "model": model,
        ## Reduction as it's heavy in context
        "prompt": f"{system_prompt}: {content}",
        "stream": False
    }
    try:
        print(f"Starting generation.")
        response = requests.post(url, json=payload)
        print(f"Response status code: {response.status_code}")
        ## Log 200 Ok
        ## Log 404 > Server 
        print(f"Response headers: {response.headers}")
        response.raise_for_status()
        response_json = response.json()
        
        print("Response JSON:")

        print(json.dumps(response_json, indent=4))
        return response_json.get('response', '')
    except requests.exceptions.RequestException as e:
        print(f"Error getting AI response: {e}")
        return None

generated_response = (generate_response(content))
print(generated_response)
