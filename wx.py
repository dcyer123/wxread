from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import math

# 配置浏览器选项
option = webdriver.EdgeOptions()
option.add_argument(r"user-data-dir=C:\\Users\\OVO\\AppData\\Local\\Microsoft\\Edge\\User Data")
# 添加更多隐蔽性选项
option.add_argument("--disable-blink-features=AutomationControlled")
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)

# 隐藏WebDriver属性
driver = webdriver.Edge(options=option)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.get("https://weread.qq.com/web/reader/aef326f05d0f19aef085d2b")
wait = WebDriverWait(driver, timeout=120)

# 获取窗口尺寸
window_width = driver.execute_script("return window.innerWidth")
window_height = driver.execute_script("return window.innerHeight")

# 模拟人类阅读模式
def simulate_human_reading():
    # 随机阅读时间（60-75秒）
    timesleep = random.randint(60, 75)
    start_time = time.time()
    
    # 在阅读时间内模拟各种人类行为
    while time.time() - start_time < timesleep:
        # 随机间隔执行不同操作
        action_delay = random.uniform(3, 8)
        time.sleep(action_delay)
        
        # 随机选择一种行为
        action_type = random.randint(1, 6)
        
        if action_type == 1:
            # 模拟鼠标移动（更自然的曲线移动）
            simulate_natural_mouse_movement()
        elif action_type == 2:
            # 模拟轻微滚动
            scroll_amount = random.randint(50, 200)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
        elif action_type == 3:
            # 模拟暂停阅读（短暂停留）
            time.sleep(random.uniform(2, 5))
        elif action_type == 4:
            # 模拟文本选择（偶尔选择文本）
            try:
                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                if paragraphs:
                    random_paragraph = random.choice(paragraphs)
                    # 使用ActionChains模拟文本选择
                    actions = ActionChains(driver)
                    actions.move_to_element(random_paragraph)
                    actions.click_and_hold()
                    actions.move_by_offset(random.randint(20, 100), 0)
                    actions.release()
                    actions.perform()
                    # 短暂停留后取消选择
                    time.sleep(0.5)
                    driver.execute_script("window.getSelection().removeAllRanges();")
            except:
                pass
        elif action_type == 5:
            # 模拟调整窗口大小或移动窗口
            try:
                # 轻微调整窗口滚动位置
                scroll_pos = random.randint(0, 100)
                driver.execute_script(f"window.scrollBy(0, {scroll_pos})")
            except:
                pass

# 模拟更自然的鼠标移动
def simulate_natural_mouse_movement():
    try:
        # 创建贝塞尔曲线路径
        start_x = random.randint(0, window_width)
        start_y = random.randint(0, window_height)
        end_x = random.randint(0, window_width)
        end_y = random.randint(0, window_height)
        
        # 控制点
        control_x = random.randint(0, window_width)
        control_y = random.randint(0, window_height)
        
        # 沿着曲线路径移动
        steps = random.randint(10, 20)
        for i in range(steps):
            t = i / steps
            # 二次贝塞尔曲线公式
            x = (1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * end_y
            
            # 使用JavaScript移动鼠标
            driver.execute_script(f"""
                var event = new MouseEvent('mousemove', {{
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': {x},
                    'clientY': {y}
                }});
                document.dispatchEvent(event);
            """)
            
            # 添加随机延迟，使移动更自然
            time.sleep(random.uniform(0.05, 0.1))
    except:
        pass

# 随机化点击行为
def randomized_click(element):
    try:
        # 先移动到元素附近
        actions = ActionChains(driver)
        location = element.location_once_scrolled_into_view
        x_offset = random.randint(-5, 5)
        y_offset = random.randint(-5, 5)
        
        # 稍微偏离精确位置点击，更像人类
        actions.move_to_element_with_offset(element, x_offset, y_offset)
        actions.pause(random.uniform(0.2, 0.5))
        actions.click()
        actions.perform()
        return True
    except:
        try:
            # 备用点击方法
            driver.execute_script("arguments[0].click();", element)
            return True
        except:
            return False

# 主循环
for i in range(300):
    # 模拟人类阅读行为
    simulate_human_reading()
    
    # 尝试翻页
    try:
        # 等待下一页按钮可点击
        next_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'renderTarget_pager_button_right') and .//span[text()='下一页']]")
        ))
        
        # 随机化点击
        if not randomized_click(next_button):
            # 如果点击失败，尝试使用键盘翻页
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.RIGHT)
            
    except Exception as e:
        print(f"翻页失败: {str(e)}")
        # 尝试使用键盘翻页作为备用方案
        try:
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.RIGHT)
        except:
            pass

# 关闭浏览器
driver.quit()