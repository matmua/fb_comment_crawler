from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import logging
from multiprocessing.dummy import Pool as ThreadPool
import pymysql
import json





def init():
    # 设置浏览器
    browser = webdriver.Firefox()
    # s = Service('./venv/Scripts/chromedriver.exe')
    # browser = webdriver.Chrome(service=s)
    browser.maximize_window()  # 浏览器窗口最大化
    browser.implicitly_wait(1)  # 隐形等待1秒
    # 访问facebook网页
    try:
        browser.get('https://www.facebook.com')
        time.sleep(2)
    # 如果打开facebook页面失败，则尝试重新加载
    except:
        browser.find_element('reload-button').click()
        print('重新刷新页面')
    time.sleep(2)
    return browser


def login():
    # 输入账户密码
    email = ''
    password = ''

    browser.find_element(by=By.ID, value='email').clear()
    browser.find_element(by=By.ID, value='email').send_keys(email)
    browser.find_element(by=By.ID, value='pass').clear()
    browser.find_element(by=By.ID, value='pass').send_keys(password)

    # 模拟点击登录按钮，两种不同的点击方法
    try:
        browser.find_element(by=By.CSS_SELECTOR, value='[type=submit]').send_keys(Keys.ENTER)
    except:
        browser.find_element(by=By.XPATH, value='//input[@tabindex="4"]').send_keys(Keys.ENTER)
        # browser.find_element(by=By.XPATH, value='//a[@href="https://www.facebook.com/?ref=logo"]').send_keys(
        # Keys.ENTER)
    time.sleep(5)
    print('登陆成功！')
#https://www.facebook.com/voachinese/posts/pfbid032eMCp5oyvMuyzzjJ7ku87w4q8mhRtVMGmnVF7Ayaz7zYwHgoCpgGzT1vLeBMHDp8l

def comment_in_posts():
    xpath_comment_block = "//div[@class='x193iq5w xw7yly9 xvue9z xq1tmr x1ceravr']"#2
    posts_dec = browser.find_elements(by=By.XPATH, value=xpath_comment_block)  # 第一块
    block = posts_dec[0]

    xpath_comment_ori = ".//div[@class='x1y1aw1k xn6708d xwib8y2 x1ye3gou']"#2
    commenters = block.find_elements(by=By.XPATH, value=xpath_comment_ori)  # 评论者
    if len(commenters) != 0:
        # 评论的评论
        try:
            for i in range(4):
                try:
                    xpath_c2c_ori = ".//span[@class='x78zum5 x1w0mnb xeuugli']"#2
                    xpath_click = xpath_c2c_ori + "/ span"
                    clicks_back = block.find_elements(by=By.XPATH, value=xpath_click)
                    for click_c in clicks_back:
                        if click_c.text.split('藏') != '隐':
                            browser.execute_script("arguments[0].scrollIntoView();", click_c)
                            click_c.click()
                    time.sleep(1)
                except:
                    pass
        except:
            pass
        xpath_time_ori = ".//ul[@class='x1n0m28w x1rg5ohu x1wfe3co xat24cr xsgj6o6 x1o1nzlu xyqdw3p']"#2
        timec = block.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[3] / a / span")  # 时间
        if len(timec) == 0:
            timec = block.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[4] / a / span")  # 时间
        if len(timec) == 0:
            timec = block.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[2] / a / span")  # 时间
        # for num in range(1, 20):
        #xpath_comment_ori = ".//div[@class='e4ay1f3w r5g9zsuq aesu6q9g q46jt4gp']"#
        oriall = block.find_elements(by=By.XPATH, value=xpath_comment_ori)  # 定位分类符
        print("all1:" + str(len(oriall)))
        #print("debug:" + oriall[-5].find_element(by=By.XPATH, value="div / span / div / div").text)#debug
        commenters = block.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / a / span / span")  # 评论者
        commenter_urls = block.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / a")  # 评论者主页url
        if len(commenter_urls) == 0:
            commenters = block.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / span / a / span / span")  # 评论者
            commenter_urls = block.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / span / a")  # 评论者主页url
        for i in range(len(oriall)):
            js_input = {}
            js_input['source'] = url
            # print(i)
            js_input['num'] = i
            js_input['content'] = ''
            js_input['at_url'] = ''
            js_input['expression'] = '0'
            try:
                # print(commenters[i].text)
                js_input['commenter'] = commenters[i].text
            except:
                js_input['commenter'] = ''

            try:
                content21 = oriall[i].find_element(by=By.XPATH, value="div[2] / span / div / div").text
                # print(content21)
                js_input['content'] = content21
                content21_at_url = oriall[i].find_elements(by=By.XPATH, value="div[2] / span / div / div / a")
                if len(content21_at_url) != 0:
                    # print("at_url:" + content21_at_url[0].get_attribute("href").split('?')[0])
                    js_input['at_url'] = content21_at_url[0].get_attribute("href").split('?')[0]
                smell_father = oriall[i].find_elements(by=By.XPATH,
                                                       value="../../../div[2]/ div / div / div / span / div")
                if len(smell_father) != 0:
                    # print("smell:" + smell_father[0].get_attribute("aria-label"))
                    js_input['expression'] = smell_father[0].get_attribute("aria-label").split('个')[0]
            except:
                pass

            try:
                content22 = oriall[i].find_element(by=By.XPATH, value="div / span / div / div").text
                # if content21 != content22:
                if len(content22) != 0:
                    # print(content22)
                    js_input['content'] = content22
                content22_at_url = oriall[i].find_elements(by=By.XPATH, value="div / span / div / div / a")
                if len(content22_at_url) != 0:
                    # print("at_url:" + content22_at_url[0].get_attribute("href").split('?')[0])
                    js_input['at_url'] = content22_at_url[0].get_attribute("href").split('?')[0]
                smell_father = oriall[i].find_elements(by=By.XPATH,
                                                       value="../../../div[2]/ div / div / div / span / div")
                if len(smell_father) != 0:
                    # print("smell:" + smell_father[0].get_attribute("aria-label"))
                    js_input['expression'] = smell_father[0].get_attribute("aria-label").split('个')[0]
            except:
                pass
            try:
                # print(commenter_urls[i].get_attribute("href").split('?')[0])
                js_input['commenter_url'] = commenter_urls[i].get_attribute("href").split('?')[0]
            except:
                print("erurl")
                js_input['commenter_url'] = ''
                pass
            try:
                # print(timec[i].text)
                js_input['time'] = timec[i].text
            except:
                js_input['time'] = ''
                # timec = browser.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[2] / a / span")  # 时间
                # print(timec[i].text)
            with open(commentf, 'a', encoding='utf-8') as f:
                f.write(json.dumps(js_input, ensure_ascii=False))
                f.write(',\n')

def comments_in_others():
    # 讨论（视频）
    xpath_comment_ori = ".//div[@class='x1y1aw1k xn6708d xwib8y2 x1ye3gou']"#2
    commenters = browser.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / a / span / span")  # 评论者
    if len(commenters) != 0:
        # 评论的评论
        try:
            for i in range(4):
                try:
                    xpath_c2c_ori = ".//span[@class='x78zum5 x1w0mnb xeuugli']"  # 2
                    xpath_click = xpath_c2c_ori + "/ span"
                    clicks_back = browser.find_elements(by=By.XPATH, value=xpath_click)
                    #print(len(clicks_back))
                    for click_c in clicks_back:
                        if click_c.text.split('藏') != '隐':
                            browser.execute_script("arguments[0].scrollIntoView();", click_c)
                            browser.execute_script("window.scrollBy(0,-75)")
                            time.sleep(0.1)
                            click_c.click()
                    time.sleep(1)
                except Exception as e:
                    print(e)
                    print(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
                    print(f"error line:{e.__traceback__.tb_lineno}")
        except:
                pass

        xpath_time_ori = ".//ul[@class='x1n0m28w x1rg5ohu x1wfe3co xat24cr xsgj6o6 x1o1nzlu xyqdw3p']"#2
        timec = browser.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[3] / a / span")  # 时间
        if len(timec) == 0:
            timec = browser.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[4] / a / span")  # 时间
        if len(timec) == 0:
            timec = browser.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[2] / a / span")  # 时间
        # for num in range(1, 20):
        #xpath_comment_ori = "//div[@class='e4ay1f3w r5g9zsuq aesu6q9g q46jt4gp']"
        oriall = browser.find_elements(by=By.XPATH, value=xpath_comment_ori)  # 定位分类符
        print("all1:" + str(len(oriall)))

        commenters = browser.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / a / span / span")  # 评论者
        commenter_urls = browser.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / a")  # 评论者主页url
        if len(commenter_urls) == 0:
            commenters = browser.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / span / a / span / span")  # 评论者
            commenter_urls = browser.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / span / a")  # 评论者主页url
        for i in range(len(oriall)):
            js_input = {}
            js_input['source'] = url
            # print(i)
            js_input['num'] = i
            js_input['content'] = ''
            js_input['at_url'] = ''
            js_input['expression'] = '0'
            try:
                # print(commenters[i].text)
                js_input['commenter'] = commenters[i].text
            except:
                js_input['commenter'] = ''

            try:
                content21 = oriall[i].find_element(by=By.XPATH, value="div[2] / span / div / div").text
                # print(content21)
                js_input['content'] = content21
                content21_at_url = oriall[i].find_elements(by=By.XPATH, value="div[2] / span / div / div / a")
                if len(content21_at_url) != 0:
                    # print("at_url:" + content21_at_url[0].get_attribute("href").split('?')[0])
                    js_input['at_url'] = content21_at_url[0].get_attribute("href").split('?')[0]
                smell_father = oriall[i].find_elements(by=By.XPATH,
                                                       value="../../../div[2]/ div / div / div / span / div")
                if len(smell_father) != 0:
                    # print("smell:" + smell_father[0].get_attribute("aria-label"))
                    js_input['expression'] = smell_father[0].get_attribute("aria-label").split('个')[0]
            except:
                pass

            try:
                content22 = oriall[i].find_element(by=By.XPATH, value="div / span / div / div").text
                # if content21 != content22:
                if len(content22) != 0:
                    # print(content22)
                    js_input['content'] = content22
                content22_at_url = oriall[i].find_elements(by=By.XPATH, value="div / span / div / div / a")
                if len(content22_at_url) != 0:
                    # print("at_url:" + content22_at_url[0].get_attribute("href").split('?')[0])
                    js_input['at_url'] = content22_at_url[0].get_attribute("href").split('?')[0]
                smell_father = oriall[i].find_elements(by=By.XPATH,
                                                       value="../../../div[2]/ div / div / div / span / div")
                if len(smell_father) != 0:
                    # print("smell:" + smell_father[0].get_attribute("aria-label"))
                    js_input['expression'] = smell_father[0].get_attribute("aria-label").split('个')[0]
            except:
                pass
            try:
                # print(commenter_urls[i].get_attribute("href").split('?')[0])
                js_input['commenter_url'] = commenter_urls[i].get_attribute("href").split('?')[0]
            except:
                print("erurl")
                js_input['commenter_url'] = ''
                pass
            try:
                # print(timec[i].text)
                js_input['time'] = timec[i].text
            except:
                js_input['time'] = ''
                # timec = browser.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[2] / a / span")  # 时间
                # print(timec[i].text)
            with open(commentf, 'a', encoding='utf-8') as f:
                f.write(json.dumps(js_input, ensure_ascii=False))
                f.write(',\n')


    else:  # 故事
        try:
            for i in range(4):
                try:
                    xpath_c2c_ori = ".//span[@class='x78zum5 x1w0mnb xeuugli']"#1
                    xpath_click = xpath_c2c_ori + "/ span"
                    clicks_back = browser.find_elements(by=By.XPATH, value=xpath_click)
                    for click_c in clicks_back:
                        if click_c.text.split('藏') != '隐':
                            click_c.click()
                    time.sleep(2)
                except:
                    pass
        except:
            pass

        xpath_time_ori = ".//ul[@class='x1n0m28w x1rg5ohu x1wfe3co xat24cr xsgj6o6 x1o1nzlu xyqdw3p']"#1
        timec = browser.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[3] / a / span")  # 时间
        if len(timec) == 0:
            timec = browser.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[4] / a / span")  # 时间
        if len(timec) == 0:
            timec = browser.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[2] / a / span")  # 时间
        #xpath_comment_ori = "//div[@class='e4ay1f3w r5g9zsuq aesu6q9g q46jt4gp']"
        oriall = browser.find_elements(by=By.XPATH, value=xpath_comment_ori)  # 定位分类符
        print("all2:" + str(len(oriall)))
        commenters = browser.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / a / span / span")  # 评论者
        commenter_urls = browser.find_elements(by=By.XPATH, value=xpath_comment_ori + "/ span / a")  # 评论者主页url
        if len(commenter_urls) == 0:
            commenters = browser.find_elements(by=By.XPATH,
                                               value=xpath_comment_ori + "/ div / span / a / span / span")  # 评论者
            commenter_urls = browser.find_elements(by=By.XPATH,
                                                   value=xpath_comment_ori + "/ div / span / a")  # 评论者主页url
        for i in range(len(oriall)):
            js_input = {}
            js_input['source'] = url
            # print(i)
            js_input['num'] = i
            js_input['content'] = ''
            js_input['at_url'] = ''
            js_input['expression'] = '0'
            # print(i)
            try:
                # print(commenters[i].text)
                js_input['commenter'] = commenters[i].text
            except:
                js_input['commenter'] = ''
            try:
                content21 = oriall[i].find_element(by=By.XPATH, value="div[2] / span / div / div").text
                js_input['content'] = content21
                # print(content21)#内容
                content21_at_url = oriall[i].find_elements(by=By.XPATH, value="div[2] / span / div / div / a")
                if len(content21_at_url) != 0:
                    js_input['at_url'] = content21_at_url[0].get_attribute("href").split('?')[0]
                    # print("at_url:" + content21_at_url[0].get_attribute("href").split('?')[0])
                smell_father = oriall[i].find_elements(by=By.XPATH,
                                                       value="../../../div[2]/ div / div / div / span / div")
                if len(smell_father) != 0:
                    js_input['expression'] = smell_father[0].get_attribute("aria-label").split('个')[0]
                    # print("smell:" + smell_father[0].get_attribute("aria-label"))
            except:
                pass
            try:
                content22 = oriall[i].find_element(by=By.XPATH, value="div / span / div / div").text
                if len(content22) != 0:
                    js_input['content'] = content22
                    # print(content22)
                content22_at_url = oriall[i].find_elements(by=By.XPATH, value="div / span / div / div / a")
                if len(content22_at_url) != 0:
                    js_input['at_url'] = content22_at_url[0].get_attribute("href").split('?')[0]
                    # print("at_url:" + content22_at_url[0].get_attribute("href").split('?')[0])
                smell_father = oriall[i].find_elements(by=By.XPATH,
                                                       value="../../../div[2]/ div / div / div / span / div")
                if len(smell_father) != 0:
                    js_input['expression'] = smell_father[0].get_attribute("aria-label").split('个')[0]
                    # print("smell:" + smell_father[0].get_attribute("aria-label"))
            except:
                pass

            try:
                js_input['commenter_url'] = commenter_urls[i].get_attribute("href").split('?')[0]
                # print(commenter_urls[i].get_attribute("href").split('?')[0])
            except:
                js_input['commenter_url'] = ''
                # print("erurl")
                pass
            try:
                js_input['time'] = timec[i].text
                #print(timec[i].text)
            except:
                js_input['time'] = ''
                # timec = browser.find_elements(by=By.XPATH, value=xpath_time_ori + "/ li[3] / a / span")  # 时间
                # print(timec[i].text)
            with open(commentf, 'a', encoding='utf-8') as f:
                f.write(json.dumps(js_input, ensure_ascii=False))
                f.write(',\n')

    # 故事

def comments(url):
#每次先点-1
    browser.get(url)  # 访问用户主页
    time.sleep(6)

    xpath_comment_block = "//div[@class='x193iq5w xw7yly9 xvue9z xq1tmr x1ceravr']"#2
    posts_dec = browser.find_elements(by=By.XPATH, value=xpath_comment_block)  # 是否存在块
    if len(posts_dec) != 0:
        comment_in_posts()#评论
    else:
        comments_in_others()






if __name__ == "__main__":  # 当程序执行时

    browser = init()
    login()

    commentf = "./评论_tect/healthy_v4_蔡天鳳碎屍案.txt"

    if browser.current_url.find('login') > 0:  # 未跳转主页再次登录
        login()
    #urls = ["https://www.facebook.com/dpptw/videos/458584419531433/",
#"https://www.facebook.com/dpptw/videos/782320609672542/",
#"https://www.facebook.com/dpptw/videos/1417997562044125/" ]18
    urls = ["https://www.facebook.com/mingpaoinews/posts/pfbid0DDED3pKxgxS6biZGQbvPz3H9mwkjZUsANZvMfQBAX8sdJ6LAA4q4DtTknamW6dmVl",
"https://www.facebook.com/eastweek.com.hk/posts/pfbid0zxpGSEsrDHnXJeVRZXuVZCQeZgfTtZYjZPLKCBU6pVhffaaciM19kcTfb9Z5kPY3l",
"https://www.facebook.com/shensimon/posts/pfbid02bAqRr79VuMeb5w1Dx5DXEi7BqebREtx9JmW4rPkCsksHtPvhdbwUxMd7ejtkKg97l",
"https://www.facebook.com/YahooHongKongNews/posts/pfbid02hN8uGtE2Eo5kDoeLpbMCxcd3ZR9fYyFVZWhmQoULiVN5TH1daYkaLmPQy1wZz336l",
"https://www.facebook.com/topick.hket/posts/pfbid0uUgktJqVq5rMQy2VaaKmZxY277eBJJJQiq8HrvNMrC3rHR1iS8gabnt1qnQv5zi4l",
"https://www.facebook.com/icable.news/posts/pfbid02paJW2u74xwxpCDW19HamF3oJBebtdxzvpXqFrUvtUK9UMnT42W9TdfQDu5cQv1tel",
"https://www.facebook.com/inmediahknet/posts/pfbid0vCWkVvuBPx5WBprc5bzhtFxpw4vBNmV55VNxk4bHSQVsc7cY3Quk9Gwt6DZym8JCl",
"https://www.facebook.com/mingpaoinews/posts/pfbid07xXq2NckY7CQY4mn3YLUiBijuakwTTm8fjqkXKHzdLfk2Kx1MzQYA4mcWxd8hW19l",
"https://www.facebook.com/now.comNews/posts/pfbid02zXhKUqtfDHBMLf3G5XXVqNizFCbvDzxyFrs5gNqjfe39uwghXuyu6pDSNYazUMsHl",
"https://www.facebook.com/mingpaoinews/posts/pfbid06uozk8VCKWmhgeNNbMNfGGaGyuFhWmoJAq5soSQqGCR4c2jcpnWxWfUgdKzFMQ76l",
]
    #"https://www.facebook.com/bbcnewstrad/posts/pfbid0gjEoGodpYYPtW2fLKguFQciEUtd9twYdq9uUcVWDDfM9jxcZZe28cVutu1QG9jJdl",
    for url in urls:
        comments(url)
