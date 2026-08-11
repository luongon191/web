from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd # Thư viện xử lý Excel

# --- CẤU HÌNH ---
TU_KHOA = "laptop dell cũ giá rẻ" # Từ khóa muốn kiểm tra
WEB_CAN_TIM = "thegioididong.com" # Tên web của khách hàng

print(">>> ĐANG KHỞI ĐỘNG TOOL...")
# Setup Chrome (Chế độ ẩn danh để kết quả khách quan nhất)
options = webdriver.ChromeOptions()
options.add_argument("--incognito") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 1. Vào Google
    print("1. Đang truy cập Google...")
    driver.get("https://www.google.com.vn")
    time.sleep(2)

    # 2. Tìm ô tìm kiếm và nhập từ khóa
    print(f"2. Đang tìm kiếm từ khóa: {TU_KHOA}")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(TU_KHOA)
    search_box.send_keys(Keys.RETURN) # Bấm Enter
    time.sleep(3) # Đợi load kết quả

    # 3. Quét toàn bộ kết quả trang 1
    print("3. Đang quét dữ liệu...")
    # Lấy tất cả các thẻ h3 (Tiêu đề bài viết)
    results = driver.find_elements(By.CSS_SELECTOR, "div.g") 
    
    danh_sach_ket_qua = []
    found = False

    rank = 1
    for result in results:
        try:
            # Lấy tiêu đề và link
            title = result.find_element(By.TAG_NAME, "h3").text
            link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
            
            # Lưu vào danh sách
            danh_sach_ket_qua.append({
                "Thứ hạng": rank,
                "Tiêu đề": title,
                "Link": link
            })
            
            # Kiểm tra xem có phải web của khách không
            if WEB_CAN_TIM in link:
                print(f"\n[PHÁT HIỆN] Web của khách nằm ở TOP {rank}")
                print(f"Tiêu đề: {title}")
                print(f"Link: {link}\n")
                found = True
            
            rank += 1
        except:
            continue

    # 4. Xuất ra file Excel
    if danh_sach_ket_qua:
        df = pd.DataFrame(danh_sach_ket_qua)
        ten_file = "ket_qua_seo.xlsx"
        df.to_excel(ten_file, index=False)
        print(f"4. Đã xuất dữ liệu ra file: {ten_file}")
    
    if not found:
        print(f"Rất tiếc, web {WEB_CAN_TIM} không nằm trong trang 1.")

except Exception as e:
    print(f"Có lỗi xảy ra: {e}")

finally:
    # Giữ màn hình 5s rồi tắt
    time.sleep(15)
    driver.quit()
    print(">>> TOOL ĐÃ CHẠY XONG.")