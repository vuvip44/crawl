from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
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

# Kiểm tra đăng nhập thành công (ví dụ: kiểm tra sự hiện diện của nút "Trang chủ")
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(@aria-label, "Trang chủ")]'))
    )
    print("Đăng nhập thành công!")
except TimeoutException:
    print("Đăng nhập không thành công. Vui lòng kiểm tra lại thông tin đăng nhập.")
    driver.quit()  # Thoát trình duyệt nếu đăng nhập không thành công
    exit()  # Dừng chương trình

# Danh sách các URL nhóm Facebook bạn muốn lấy dữ liệu
group_urls = [
    'https://www.facebook.com/groups/174764463261090'
    # ... thêm các URL nhóm khác vào đây
]

# Danh sách để lưu dữ liệu nội dung post
postData = []

# Số lượng bài viết muốn lấy
n = 10 # Thay đổi giá trị này theo số lượng bài viết bạn muốn lấy

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

    # Khởi tạo post_elements với danh sách rỗng
    post_elements = []

    # Cuộn trang để tải thêm bài viết
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Đợi một chút để nội dung tải

        # Kiểm tra xem có bài viết mới được tải hay không
        new_posts = driver.find_elements(By.XPATH, '//div[@role="article"]')
        if len(new_posts) == len(post_elements):  # Không có bài viết mới
            break

        post_elements = new_posts
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Lấy nội dung từ các bài viết và dừng khi đủ số lượng
    count = 0
    for post in post_elements:
        try:
            # Điều chỉnh XPath này dựa trên cấu trúc thực tế
            content_element = post.find_element(By.XPATH, './/div[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f"]/span[1]')
            content = content_element.text
            print(f'Post content: {content.encode("utf-8", "ignore").decode("utf-8")}')
        except NoSuchElementException:
            content = "Content not found in this post"
            print(content)

        # Lưu dữ liệu vào danh sách
        postData.append({'link': group_url, 'content': content})

        count += 1
        if count >= n:
            break 

# Lưu dữ liệu nội dung post vào file posts.csv
df = pd.DataFrame(postData)
print(df)
df.to_csv('data/posts.csv', index=False, encoding='utf-8-sig')

# Đóng trình duyệt
driver.quit()