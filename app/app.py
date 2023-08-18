# -*- coding: utf-8 -*-
#Maxwell Wippich
from selenium import webdriver
from datetime import datetime
from flask import Flask, request
import boto3, configparser
import os
from selenium import webdriver

path_name = ''
service_name = 'default'
app = Flask(__name__)
@app.route("/",methods=['GET'])
def home():
    args = request.args
    url = args.get("url", type=str)
    print(url)
    URL_id = None
    if url:
        URL_id = url
    bucket = request.args.get("bucket")
    if bucket:
        bucket_name = bucket
    service = request.args.get("service")
    if service:
        service_name = service
    path = request.args.get("path")
    if path:
        path_name = path
    name = request.args.get("name")
    if name:
       filename = name
    else:
        name = "ScreenShot"
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_time *= 3
        name += current_time

        filename =  name


    #logging.basicConfig(filename='/logs/error.log', level=INFO)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-crash-reporter")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-in-process-stack-traces")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36") 

    # Setup chrome driver
    # service = ChromeService(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(URL_id)
    width = 750
    height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
    driver.set_window_size(width,height)
    #page_body = driver.find_element(By.TAG_NAME, "body")
    # Saving screenshot of the browser
    driver.get_screenshot_as_file(filename + '.png')
    #logging.info(f"image saved to {filename + '.png'}")

    with open(filename + '.png', "rb") as image:
      f = image.read()
      b = bytearray(f)
    
    if(service_name == 's3'):
        config_s3 = configparser.ConfigParser()
        config_s3.read('/app/s3.config')
        s3_service = 'contabo'
        print(f"config_s3.read ${config_s3['contabo']}")
        s3 = boto3.client('s3',
                          endpoint_url=config_s3[s3_service].get('endpoint_url'),
                          aws_access_key_id=config_s3[s3_service].get('aws_access_key_id'),
                          aws_secret_access_key=config_s3[s3_service].get('aws_secret_access_key'))

        content_type = 'image/png'
        #bucket_name = "test.incomaker.screenshoter"
        content_length = os.path.getsize(filename + ".png")

        s3.put_object(Bucket=bucket_name, Key= path_name + filename + ".png", Body= f, ContentType=content_type, ContentLength=content_length)

        os.remove(filename + '.png')
    else:
        with open("Binary.txt", "wb") as binary_file:# Write bytes to file
            binary_file.write(b)
        with open("Binary.txt", "rb") as binary_file:
            text = binary_file.read()
        os.remove("Binary.txt")
        #os.remove(filename + '.png')
        return "png should be"

    driver.quit()
    return ("Screenshots saved of :" + URL_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
