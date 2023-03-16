# coding=utf-8
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import threading


class ZhiHui:

    # 遇见错误退出
    def exit_def(self):
        print ("执行退出函数")
        self.driver.quit()
        exit()

    # 登录方法
    def login(self):
        # 账号
        username = input("请输入账号：")
        # 密码
        passwd = input("请输入密码：")
        #　登录的链接
        url = "https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin"
        # 进入链接
        self.driver.get (url)

        # 使用js代码进行输入账号密码
        self.driver.execute_script ('document.getElementById("lUsername").value="{}"'.format (username))
        self.driver.execute_script ('document.getElementById("lPassword").value="{}"'.format (passwd))

        # 定位到输入密码的输入框，然后模拟键盘进行回车登录
        self.driver.find_element_by_id('lPassword').send_keys(Keys.ENTER)

        # 判断登录按钮是否消失，没有消失就证明没有登录成功
        try:
            WebDriverWait(self.driver,3).until_not(EC.presence_of_element_located((By.XPATH, '//*[@id="f_sign_up"]/div/span')))
            print("登录成功")
        except Exception:
            print("登录失败")
            self.exit_def()

    # 检查视频状态
    def course_status(self):
        chapter = self.driver.find_elements_by_xpath('//li[starts-with(@class,"clearfix video")]')
        # 匹配clearfix video开头的元素也就是每个视频，，因为正在播放的视频类名是‘clearfix video current_play’ 否则会少匹配一个视频
        len_chapter = int(len(chapter))
        # 获取到本课程有多少视频以方便判断是否全部看完
        n = 0
        for i in chapter:
            try:
                # 在chapter的基础上进行选择
                i.find_element_by_xpath('.//b[@class="fl time_icofinish"]')
                n += 1
            except:
                print("检查到没有看完的章节")
                time.sleep (2)
                # 如果检测到没有看的视频，就去点击他
                click = i.find_element_by_xpath('.//div[@class="fl cataloguediv-c"]/span')
                time.sleep(2)
                ActionChains(self.driver).click(click).perform()
                break
            # 不管try有没有异常都查看一遍是否全部看完了，看完了执行into函数
            finally:
                if n == len_chapter:
                    print("本课程已经全部学完")
                    self.driver.find_element_by_class_name('back').click()
                    self.into()

    # 获取课程名  课程进度  在学课程
    def various_names(self):


        # 显式等待 查找这个路径
        WebDriverWait (self.driver, timeout=10).until (EC.presence_of_element_located ((By.XPATH, '//div[@id="sharingClassed"]/div[2]/ul')))
        try:
            # 课程名称等信息在这个基础路径下 然后去遍历ul
            base_xpath = self.driver.find_elements_by_xpath ('//div[@id="sharingClassed"]/div[2]/ul')
            num = 1

            for i in base_xpath:
                # 获取课程名称
                name = i.find_element_by_xpath ('.//div[@class="courseName"]').get_attribute ("textContent")

                # 获取在学
                attending_school = i.find_element_by_xpath ('.//span[@class="name"]').get_attribute ("textContent")

                # 获取进度
                process_num = i.find_element_by_xpath ('.//span[@class="processNum"]').get_attribute ("textContent")

                print (str (num) + " 课程名称：" + name + "\n在学：" + attending_school + "\n进度：" + process_num)
                print ("-" * 50)
                num += 1
        except:
            print ("获取课程名称等操作失败")
            self.exit_def ()

    # 关闭我知道了和学前须知
    def into(self):
        num = input ("选择想要开始的课程：")
        try:
            # 进入课程
            self.driver.find_element_by_xpath ('//div[@id="sharingClassed"]/div[2]/ul[' + num + ']/div/dl/dt/div[1]').click ()
        except:
            print ('选择课程失败')
            self.into()

        # 关闭我知道了 显式等待 在timeout规定的时间内查找有没有你想要的元素，0.5S 查找一次 可以使用poll_frequency=5 调整查找频率
        try:
            element = WebDriverWait (self.driver, timeout=5).until (EC.presence_of_element_located ((By.XPATH, '/html/body/div[1]/div/div[6]/div/div[3]/span/button/span')))
            element.click ()
            print ("关闭我知道了成功")
        except:
            print ("点击我知道了失败")

        # 关闭学前须知
        try:
            element = WebDriverWait (self.driver, timeout=5).until (
                EC.presence_of_element_located ((By.XPATH, '/html/body/div[1]/div/div[7]/div[2]/div[1]/i')))
            element.click ()
            print ("关闭学前须知成功")
        except:
            print ("点击学前必读失败")

    # 获取总时间以及当前章节
    def time_chapter(self):
        time.sleep (5)
        try:
            print ("-" * 50)
            # 总时间
            total_time = self.driver.find_element_by_xpath ('//span[@class="duration"]').get_attribute ('textContent')
            # 章节
            chapter = self.driver.find_element_by_id ("lessonOrder").get_attribute ('textContent')
            print ("正在观看：" + chapter + " 本节视频总时长：" + total_time)
        except:
            print ("获取时间以及正在看的章节失败")

    # 设置画质倍速
    def set(self):
        try:
            time.sleep(2)
            self.driver.execute_script (
                'document.querySelector("#vjs_container > div.controlsBar > div.definiBox > div > b.line1bq.switchLine").click()')  # 设置流畅
            print ("设置流畅成功")
        except:
            print ("设置流畅失败")

        # 设置倍速
        try:
            time.sleep (2)
            self.driver.execute_script (
                'document.querySelector("#vjs_container > div.controlsBar > div.speedBox > div > div.speedTab.speedTab10").click()')  # 1.25倍
            print ("设置1.25倍成功")
        except:
            print ("设置1.25倍失败")

    # 检测习惯分
    def custom_points(self):
        print ("检测习惯分中")
        while True:
            time.sleep (5)
            try:
                # 显示等待判断有没有习惯分提示
                WebDriverWait (self.driver, timeout=True, poll_frequency=5).until(EC.presence_of_element_located ((By.XPATH, '//*[@id="app"]/div/div[8]/div/div[1]/button'))).click ()
                self.driver.execute_script ('document.querySelector("#playButton").click()')  # 点击播放
                print ("关闭习惯分提示成功")
            except:
                pass

    # 检测弹窗
    def Close_Popup(self):
        print ("弹窗检测中")
        while True:
            try:
                # 显示等待查找弹窗，有弹窗就点击第一个不管对错然后确定
                WebDriverWait (self.driver, timeout=True, poll_frequency=10).until (EC.presence_of_element_located ((By.CLASS_NAME, "topic-item"))).click ()
                self.driver.find_element_by_xpath ('/html/body/div[1]/div/div[7]/div/div[3]/span/div').click ()  # 点击关闭
                time.sleep (2)
                self.driver.execute_script ('document.querySelector("#playButton").click()')  # 点击播放
                print ("关闭弹窗成功")
            except:
                pass

    # 检测下一集
    def next(self):

        while True:
            time.sleep (10)  # 10秒检测一次
            # 获取总时间
            total_time = self.driver.find_element_by_xpath ('//*[@id="vjs_container"]/div[10]/div[4]/span[2]').get_attribute ('textContent')
            # 获取当前时间
            current_time = self.driver.find_element_by_xpath ('//*[@id="vjs_container"]/div[10]/div[4]/span[1]').get_attribute ('textContent')
            print ("\r当前时间：{}".format (current_time), end="", flush=True)
            # 如果总时间等于当前时间就是看完了，
            if current_time == total_time:
                print ('本节视频播放完成，正在播放下一节')
                try:
                    time.sleep(3)
                    # 检查视频状态找下一个没有看完的视频
                    self.course_status()
                    # 找到后进行画质倍速的设置
                    self.set ()
                    # 获取章节总时间
                    self.time_chapter ()
                except:
                    print ("点击下一节失败")

    # 启动线程
    def thread(self):
        custom = threading.Thread (target=self.custom_points)
        poput = threading.Thread (target=self.Close_Popup)
        next = threading.Thread (target=self.next)
        # 开始检测习惯分
        custom.start ()
        # 开始检测弹窗
        poput.start ()
        # 开始检测下一节
        next.start ()

    def __init__(self):

        options = EdgeOptions()
        options.add_argument ('--mute-audio')
        # 静音

        prefs = {"": ""}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option ("prefs", prefs)
        # 关闭密码保护

        options.add_experimental_option("excludeSwitches",["enable-automation"])
        # 开发者模式

        try:
            self.driver = webdriver.Edge(r'D:\edgedriver\msedgedriver.exe', options=options)
            print("浏览器启动成功")
            print("-"*50)
        except:
            print("浏览器启动失败")

    # 实现主要逻辑
    def run(self):
        self.login ()
        # 登录
        self.various_names ()
        # 获取各种名称
        self.into ()
        # 进入课程
        self.course_status ()
        # 检查视频状态
        self.time_chapter ()
        # 获取总时间以及章节
        self.set ()
        # 设置画质速度
        self.thread ()
        # 启动线程


if __name__ == '__main__':
    zhihui = ZhiHui ()
    zhihui.run ()

