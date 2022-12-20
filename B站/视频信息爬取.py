from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains    # 动作链
from selenium.webdriver import ChromeOptions    # 浏览器配置
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os.path
import requests


page = 1

def get_serch(url):
    # 创建浏览器对象
    driver = webdriver.Chrome()
    # 时间等待
    wait = WebDriverWait(driver,10)
    # 发送请求
    driver.get(url=url)
    # 窗口最大化
    driver.maximize_window()
    time.sleep(1)
    # 直到出现这个元素
    wait.until(EC.presence_of_element_located((By.TAG_NAME,'input')))
    # input输入
    entry = driver.find_element(By.TAG_NAME,'input')
    entry.send_keys('金泰梨')#搜索信息
    time.sleep(1)
    # click
    button = driver.find_element(By.XPATH,'//div[@class="nav-search-btn"]')
    button.click()
    # 切换窗口视角
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    # 回到旧版
    dic = driver.find_element(By.XPATH,'//*[@id="i_cecream"]/div[1]/div[2]/div/div/div/div/button[1]')
    dic.click()
    time.sleep(1)
    return driver




def get_data(driver):
    all_data = []   # 空列表

    num = 1
    while num <= 20:
        print(f'=====================================正在保存第{num}页的数据内容=================================')
        # 动作链
        try:
            action = driver.find_element(By.XPATH, '//*[@class="page-item next"]/button')
            ActionChains(driver).move_to_element(action).perform()
        except:
            print('==============================没有下一页了========================')

        # 全部视频
        time.sleep(1)
        all_li = driver.find_elements(By.XPATH,'//*[@id="all-list"]/div[1]/div[2]/ul[2]/li')
        # 判断空列表
        if all_li == []:
            all_li = driver.find_elements(By.XPATH, '//*[@id="all-list"]/div[1]/ul/li')
        elif all_li != []:
            all_li = driver.find_elements(By.XPATH,'//*[@id="all-list"]/div[1]/div[2]/ul[2]/li')
        time.sleep(1)
        for i in all_li:
            ditail = i.find_element(By.XPATH,'./div/div[1]/a').get_attribute('href')
            title = i.find_element(By.XPATH,'./div/div[1]/a').get_attribute('title')
            new_time = i.find_element(By.XPATH,'./div/div[3]/span[3]').text
            user = i.find_element(By.XPATH,'./div/div[3]/span[4]').text
            images = i.find_element(By.XPATH,'./a/div/div[1]/img').get_attribute('src')
            if images == '':
                images = 'https://i0.hdslb.com/bfs/archive/9974b552950679b49c0e73d10bd55c29fcec35b9.png@400w_250h_1c.webp'
            watch = i.find_element(By.XPATH,'./div/div[3]/span[1]').text
            item = {
                '标题': title,
                '详情页': ditail,
                '发布时间': new_time,
                'up博主': user,
                '图片': images,
                '观看次数': watch
            }
            print(item)
            all_data.append(item)
            save_Images(title,images)


        time.sleep(1)
        try:
            # 翻页
            net_page = driver.find_element(By.XPATH,'//*[@class="page-item next"]/button')
            net_page.click()
            time.sleep(3)
            num += 1
        except:
            break

    return all_data





def save_csv(all_data):
    df = pd.DataFrame(all_data)
    df.to_csv('哔哩.csv',index=False)



def save_Images(title,images):
    global page
    if not os.path.exists('./B站图片抓取/'):
        os.mkdir('./B站图片抓取/')
    response = requests.get(url=images).content
    with open('./B站图片抓取/' + str(page) + '.jpg',mode='wb')as f:
        f.write(response)
        print('正在保存图片:' + title)
        page += 1




def mian():
    url = 'https://www.bilibili.com/'
    driver = get_serch(url)
    all_data = get_data(driver)
    save_csv(all_data)




if __name__ == '__main__':
    mian()

