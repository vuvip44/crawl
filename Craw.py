from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

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

# Kiểm tra đăng nhập thành công
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(@aria-label, "Trang chủ")]'))
    )
    print("Đăng nhập thành công!")
except TimeoutException:
    print("Đăng nhập không thành công. Vui lòng kiểm tra lại thông tin đăng nhập.")
    driver.quit()
    exit()

# Danh sách các URL nhóm Facebook
group_urls = [
    'https://www.facebook.com/groups/174764463261090'
]

# Danh sách để lưu dữ liệu nội dung post
postData = []

# Số lượng bài viết muốn lấy
n = 10  # Thay đổi giá trị này theo số lượng bài viết bạn muốn lấy

# Duyệt qua các URL nhóm
for group_url in group_urls:
    driver.get(group_url)

    # Chờ cho đến khi một số bài viết được tải
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="article"]'))
        )
    except TimeoutException:
        print(f'Timeout waiting for posts to load in {group_url}')
        continue  # Chuyển sang nhóm tiếp theo nếu không tải được bài viết

    # Khởi tạo danh sách post_elements
    post_elements = []

    # Cuộn trang để tải thêm bài viết
    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(post_elements) < n:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Tìm tất cả các bài viết hiện tại
        new_posts = driver.find_elements(By.XPATH, '//div[@role="article"]')
        if len(new_posts) > len(post_elements):
            post_elements = new_posts
        else:
            break

        # Kiểm tra xem có bài viết mới được tải hay không
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Lấy nội dung từ các bài viết và dừng khi đủ số lượng
    count = 0
    for post in post_elements:
        if count >= n:
            break

        try:
            # Thử tìm nội dung của bài viết qua nhiều cách khác nhau
            content = None
            try:
                content_element = post.find_element(By.XPATH, './/div[contains(@data-ad-preview, "message")]')
                content = content_element.text
            except NoSuchElementException:
                try:
                    # Dùng các cách khác để tìm nội dung bài viết
                    content_element = post.find_element(By.XPATH, './/span[not(ancestor::div[contains(@aria-label, "Reactions")]) and not(ancestor::span[@role="button"])]')
                    content = content_element.text
                except NoSuchElementException:
                    try:
                        content_element = post.find_element(By.XPATH, './/p')
                        content = content_element.text
                    except NoSuchElementException:
                        content = "Content not found in this post"

            # Kiểm tra nếu nội dung rỗng
            if not content:
                content = "Content not found or empty in this post"
            
            print(f'Post content: {content.encode("utf-8", "ignore").decode("utf-8")}')
        except NoSuchElementException:
            content = "Content not found in this post"
            print(content)

        # Lưu dữ liệu vào danh sách
        postData.append({'link': group_url, 'content': content})

        count += 1

# Lưu dữ liệu nội dung post vào file posts.csv
df = pd.DataFrame(postData)
print(df)
df.to_csv('data/posts.csv', index=False, encoding='utf-8-sig')

# Đóng trình duyệt
driver.quit()
