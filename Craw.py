from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import pandas as pd

# Đọc danh sách các link từ file websites.csv
websites = []
with open('data/websites.csv', mode='r') as file:
    csv_websites = csv.reader(file)
    for website in csv_websites:
        websites.append(website[0])

# Cấu hình chế độ incognito cho trình duyệt
chromeOptions = Options()
chromeOptions.add_argument("--incognito")
chromeOptions.add_argument('--start-maximized')

driver = webdriver.Chrome(options=chromeOptions)

# Đăng nhập Facebook
driver.get("https://vi-vn.facebook.com/login.php/")
time.sleep(2)

txtUser = driver.find_element(By.ID, "email")
txtUser.send_keys("zds34054@dcobe.com")
txtPass = driver.find_element(By.ID, "pass")
txtPass.send_keys("khdl123@")
txtPass.send_keys(Keys.ENTER)

time.sleep(2)

# Danh sách để lưu dữ liệu nội dung post
postData = []

# Duyệt qua các website trong danh sách
for website in websites:
    driver.get(website)
    time.sleep(5)  # Chờ trang tải

    try:
        # Tìm phần tử <span> chứa nội dung post dựa trên class đã cung cấp
        postElement = driver.find_element(
            By.XPATH, '//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"]')
        postContent = postElement.text  # Lấy nội dung từ text của span
        print(f'Link: {website}, Post content: {postContent}')
    except NoSuchElementException:
        postContent = "Content not found"
        print(f'Link: {website}, Post content not found')

    # Lưu dữ liệu vào danh sách
    postData.append({'link': website, 'content': postContent})

# Lưu dữ liệu nội dung post vào file posts.csv
df = pd.DataFrame(postData)
df.to_csv('data/posts.csv', index=False)

# Đóng trình duyệt
driver.quit()