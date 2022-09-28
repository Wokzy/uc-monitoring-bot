import os
import time

from PIL import Image
from io import BytesIO
from constants import *
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fullpage_screenshot(driver, element=None):

        print("Starting full page screenshot workaround ...")

        total_width = driver.execute_script("return document.body.offsetWidth")
        if element:
            total_height = driver.execute_script("return arguments[0].scrollHeight", element)
        else:
            total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        rectangles = []

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

                print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        previous = None
        part = 0
        stitched_image = Image.new('RGB', (total_width, total_height))

        for rectangle in rectangles:
            if not previous is None:
                if element:
                    driver.execute_script("arguments[0].scrollTo({0}, {1})".format(rectangle[0], rectangle[1]), element)
                else:
                    driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                time.sleep(3)

            file_name = "part_{0}.png".format(part)
            print("Capturing {0} ...".format(file_name))

            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        print("Finishing full page screenshot workaround...")
        return stitched_image, total_height, total_width


def make_screen(urls, grafana=None):
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)

    driver.get(urls[0]['url'])

    if grafana:
        username = grafana['LOGIN']
        password = grafana['PASSWORD']
        driver.find_element_by_xpath('//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input').send_keys(username)
        driver.find_element_by_xpath('//*[@id="current-password"]').send_keys(password)
        driver.find_element_by_xpath('//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button').click()
        WebDriverWait(driver=driver, timeout=10).until(lambda x: x.execute_script("return document.readyState === 'complete'"))
        time.sleep(5)

    total_height = 0
    images = []
    for url in urls:
        driver.get(url['url'])
        timer = datetime.now()
        time.sleep(url['timeout'])
        images.append(fullpage_screenshot(driver))
        total_height += images[-1][1]

    stitched_image = Image.new('RGB', (images[-1][2], total_height))
    i = 0
    for image in images:
        stitched_image.paste(image[0], (0, i))
        i += image[1]
    stitched_image.save(SCREENSHOTFILENAME)

    driver.quit()

    print('success')
    return True