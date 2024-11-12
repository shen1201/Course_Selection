from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import ttk
from threading import Thread, Event
import sys
import time

def task(username, password, course_id):
    print("Executing task...")
    login_page_url = 'https://cos.tcu.edu.tw/ScasWebSite/Default.aspx?id='

    while not stop_event.is_set():
        try:
            # 建立 Chrome options 物件
            chrome_options = Options()
            # 添加無頭模式參數
            chrome_options.add_argument("--headless")
            # 添加其他參數，例如視窗大小
            chrome_options.add_argument("--window-size=1920x1080")

            # 指定 ChromeDriver 路徑
            s = Service(r'chromedriver-win64\chromedriver.exe')

            # 初始化 WebDriver，並使用上述定義的參數
            driver = webdriver.Chrome(service=s, options=chrome_options)

            # 打開登入頁面
            driver.get(login_page_url)

            # 填寫登入表單
            driver.find_element(By.NAME, "logUser$UserName").send_keys(username)
            driver.find_element(By.NAME, "logUser$Password").send_keys(password)

            # 提交表單
            driver.find_element(By.NAME, "logUser$LoginButton").click()

            # 登入成功後的其他處理，例如驗證登入成功
            print("登入成功")

            # 使用輸入的課程代碼
            Code0 = course_id

            # 加選課程
            driver.get("https://cos.tcu.edu.tw/ScasWebSite/SelectAddCode.aspx")

            # 填寫課程代碼
            driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$WcClassAddSwitch1$WcClassQueryCode1$txtCode0").send_keys(Code0)

            # 確認
            driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$WcClassAddSwitch1$WcClassQueryCode1$btnQuery").click()

            # 獲取當前日期和時間
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("------------------------------------------------")
            print("選課時間:", now)

            # 定位並點擊「加選」連結
            add_link_id = "ctl00_ContentPlaceHolder1_WcClassListSelect1_gvStepFullClassList_ctl03_btnAdd"
            try:
                driver.find_element(By.ID, add_link_id).click()
                alert = Alert(driver)
                alert_text = alert.text
                print(f"彈出窗口內容: {alert_text}")
                alert.accept()
                alert.accept()
                print("終於加選成功了!!!")
                driver.quit()
                sys.exit()
            except Exception as e:
                print("沒搶到哈哈哈")
        except Exception as e:
            print(f"發生錯誤: {e}")

        driver.quit()

    print("------------------------------------------------")

def start_task(username_entry, password_entry, course_id_entry):
    global stop_event
    stop_event.clear()
    username = username_entry.get()
    password = password_entry.get()
    course_id = course_id_entry.get()
    t = Thread(target=task, args=(username, password, course_id))
    t.start()
    print("任務已啟動...")

def stop_task():
    stop_event.set()
    print("任務已停止...")

def exit_program():
    stop_event.set()
    print("退出程式...")
    root.destroy()
    sys.exit()

stop_event = Event()

root = tk.Tk()
root.title("TCU 選課程式")
root.minsize(400, 300)
root.configure(bg='#e6f2ff')  # 淡藍色背景

style = ttk.Style()
style.configure('TLabel', background='#e6f2ff', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12), background='#cce6ff')
style.map('TButton', background=[('active', '#b3d9ff')])

username_label = ttk.Label(root, text="學號:")
username_label.grid(row=0, column=0, padx=20, pady=10, sticky='E')
username_entry = ttk.Entry(root)
username_entry.grid(row=0, column=1, padx=20, pady=10)

password_label = ttk.Label(root, text="密碼:")
password_label.grid(row=1, column=0, padx=20, pady=10, sticky='E')
password_entry = ttk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=20, pady=10)

course_id_label = ttk.Label(root, text="課程代碼:")
course_id_label.grid(row=2, column=0, padx=20, pady=10, sticky='E')
course_id_entry = ttk.Entry(root)
course_id_entry.grid(row=2, column=1, padx=20, pady=10)

start_button = ttk.Button(root, text="開始搶課", command=lambda: start_task(username_entry, password_entry, course_id_entry))
start_button.grid(row=3, column=0, padx=10, pady=10)

stop_button = ttk.Button(root, text="停止搶課", command=stop_task)
stop_button.grid(row=3, column=1, padx=10, pady=10)

exit_button = ttk.Button(root, text="結束程式", command=exit_program)
exit_button.grid(row=3, column=2, padx=10, pady=10)

root.mainloop()
