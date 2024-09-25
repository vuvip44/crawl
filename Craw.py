from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# Hàm cuộn trang để tải thêm bài viết
def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Chờ một khoảng thời gian để trang tải thêm nội dung

# Cấu hình chế độ incognito cho trình duyệt
chromeOptions = Options()
chromeOptions.add_argument("--incognito")
chromeOptions.add_argument('--start-maximized')
driver = webdriver.Chrome(options=chromeOptions)

# Đăng nhập Facebook
driver.get("https://vi-vn.facebook.com/login.php/")
time.sleep(2)
txtUser = driver.find_element(By.ID, "email")
txtUser.send_keys("zds34054@dcobe.com")  # Thay bằng email của bạn
txtPass = driver.find_element(By.ID, "pass")
txtPass.send_keys("khdl123@")  # Thay bằng mật khẩu của bạn
txtPass.send_keys(Keys.ENTER)
time.sleep(5)  # Đợi đăng nhập hoàn tất

# Truy cập vào nhóm Facebook
group_url = "https://www.facebook.com/groups/174764463261090"  # Thay bằng URL của nhóm bạn
driver.get(group_url)
time.sleep(5)  # Đợi trang nhóm tải

# Số lượng bài viết muốn lấy
n_posts = 10

# Danh sách để lưu dữ liệu nội dung post
postData = []
# Vòng lặp để cuộn và lấy bài viết
while len(postData) < n_posts:
    # Tìm tất cả các bài viết hiện có trên trang
    postElements = driver.find_elements(By.XPATH, '//div[@role="article"]')
    
    for postElement in postElements:
        if len(postData) >= n_posts:
            break  # Dừng nếu đã lấy đủ bài viết
        try:
            # Lấy phần tử chứa nội dung của bài viết
            contentElement = postElement.find_element(By.XPATH, './/span[contains(@class, "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u")]')
            postContent = contentElement.text
            print(f'Post content: {postContent}')
            postData.append({'content': postContent})
        except NoSuchElementException:
            print('Post content not found')
            postData.append({'content': 'Content not found'})
    
    # Cuộn trang xuống để tải thêm bài viết
    scroll_down(driver)

# Lưu dữ liệu nội dung post vào file posts.csv
df = pd.DataFrame(postData)
print(df)
df.to_csv('posts.csv', index=False, encoding='utf-8-sig')

# Đóng trình duyệt
driver.quit()
