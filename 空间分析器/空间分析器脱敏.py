from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import os
import json
from selenium.webdriver.common.keys import Keys
from datetime import datetime  # 获取年份 其实可以替代time
import re
from matplotlib import pyplot as plt
import pyautogui as auto
import numpy as np
import random
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
import cv2
import pandas as pd
from PIL import Image
import jieba
import collections
from wordcloud import WordCloud
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import calendar

# 后续：
# 爬取最常点赞的人 ok 5.4
# 预测下一次几点发说说


class QQSpider(object):
    """
    破解滑块验证码
    爬取目标空间信息
    测试用例是用**********爬取**********的空间
    需要对方为自己好友且空间对自己可见
    好像有置顶说说的时候会报错
    """

    def __init__(self):
        """
        初始化
        """
        os.makedirs('./csvs', exist_ok=True)
        os.makedirs('./image/', exist_ok=True)
        os.makedirs('./jsons/', exist_ok=True)
        os.makedirs('./results/', exist_ok=True)
        sns.set_theme(style="darkgrid", font='SimHei', font_scale=1.4)
        plt.rcParams['figure.figsize'] = (12.0, 8.0)
        self.sign = '空间分析器 By.L1_Sta2'
        self.target = auto.prompt(
            text='请输入要爬取的人的账号', title = self.sign, default='**********')  # '**********'
        if self.csv_is_exist():
            cho = auto.confirm(
                text='是否需要更新数据', title=self.sign, buttons=['是', '否'])
            if cho == '是':
                pass
            else:
                return
        self.url = "https://user.qzone.qq.com/" + self.target + "/main"
        self.driver = webdriver.Edge(r'D:\edgedriver\msedgedriver.exe')
        self.driver.implicitly_wait(5)
        self.num = auto.prompt(text='登录账号', title=self.sign,
                               default='**********')  # '**********'
        self.password = auto.password(
            text='输入密码', title=self.sign, default='12345678', mask='$')# 需要改

    @staticmethod
    def webdriverwait_send_keys(dri, element, value):
        """
        driver 等待元素 输入内容
        """
        WebDriverWait(dri, 10, 5).until(lambda dr: element).send_keys(value)

    @staticmethod
    def webdriverwait_click(dri, element):
        """
        显式等待 点击
        """
        WebDriverWait(dri, 10, 5).until(lambda dr: element).click()

    @staticmethod
    def get_postion(otemp, oblk):
        """
        判断缺口位置
        """
        target = cv2.imread(otemp, 0)
        template = cv2.imread(oblk, 0)
        temp = 'temp.jpg'
        targ = 'targ.jpg'
        cv2.imwrite(temp, template)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        target = abs(255 - target)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        template = cv2.imread(temp)
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)
        return x, y

    @staticmethod
    def get_track(distance):
        """
        模拟轨迹 假装是人在操作
        distance:
        """
        v = 100
        t = 0.2
        tracks = []
        mid = distance * 7 / 8
        # 到达mid值开始减速
        distance += 10  
        # 先滑过一点，最后再反着滑动回来
        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = random.randint(2, 4)  # 加速运动
            else:
                a = -random.randint(3, 5)  # 减速运动
            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))
            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t
        # 反着滑动到大概准确位置
        for i in range(4):
            tracks.append(-random.randint(2, 3))
        for i in range(4):
            tracks.append(-random.randint(1, 3))
        return tracks

    @staticmethod
    def urllib_download(imgurl, imgsavepath):
        """
        下载图片
        imgurl: 图片url
        imgsavepath: 存放地址
        """
        from urllib.request import urlretrieve
        urlretrieve(imgurl, imgsavepath)

    def main(self):
        """
        主流程
        滑块验证码
        爬取空间
        """
        # 以下为验证码部分###################################
        driver = self.driver
        driver.maximize_window()
        # 全屏
        driver.get(self.url)
        driver.switch_to.frame('login_frame')
        # switch 到 登录frame

        # 以下键入账号密码###########################
        switch_method = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[9]/a[1]')
        self.webdriverwait_click(driver, switch_method)
        # 点击账号密码登录
        click_keyi_username = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/div[1]/div[3]/form/div["
                                                            "1]/div/input")
        self.webdriverwait_send_keys(driver, click_keyi_username, self.num)
        time.sleep(2)
        password = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[5]/div/div[1]/div[3]/form/div[2]/div[1]/input')
        self.webdriverwait_send_keys(driver, password, self.password)
        time.sleep(2)
        login_button = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[5]/div/div[1]/div[3]/form/div[4]/a/input')
        # 登录
        self.webdriverwait_click(driver, login_button)
        time.sleep(1)
        # 以上键入账号密码#############################

        time.sleep(0.5)
        # 切换到滑块frame
        try:
            driver.switch_to.frame("tcaptcha_iframe")
            bk_block = driver.find_element(
                By.XPATH, r'/html/body/div/div[3]/div[2]/div[1]/div[2]/img')  # 大图
            web_image_width = bk_block.size
            web_image_width = web_image_width['width']
            bk_block_x = bk_block.location['x']

            slide_block = driver.find_element(
                By.XPATH, '/html/body/div/div[3]/div[2]/div[1]/div[3]/img')  # 小滑块
            slide_block_x = slide_block.location['x']

            bk_block = driver.find_element(
                By.XPATH, r'/html/body/div/div[3]/div[2]/div[1]/div[2]/img').get_attribute('src')
            # 大图 url
            slide_block = driver.find_element(
                By.XPATH, r'/html/body/div/div[3]/div[2]/div[1]/div[3]/img').get_attribute('src')
            # 小滑块 图片url
            slid_ing = driver.find_element(
                By.XPATH, r'/html/body/div/div[3]/div[2]/div[2]/div[2]/div[1]')  # 滑块

            
            # 允许已经存在文件夹
            self.urllib_download(bk_block, './image/bkBlock.png')
            self.urllib_download(slide_block, './image/slideBlock.png')
            # 保存截图到image文件夹下
            time.sleep(0.5)
            img_bkblock = Image.open('./image/bkBlock.png')
            real_width = img_bkblock.size[0]
            width_scale = float(real_width) / float(web_image_width)
            position = self.get_postion(
                './image/bkBlock.png', './image/slideBlock.png')
            real_position = position[1] / width_scale
            real_position = real_position - (slide_block_x - bk_block_x)
            track_list = self.get_track(real_position + 4)

            while True:
                '''这里最开始准备尝试反复登录'''
                ActionChains(driver).click_and_hold(
                    on_element=slid_ing).perform()  # 点击鼠标左键，按住不放
                time.sleep(0.2)
                # 拖动元素
                for track in track_list:
                    ActionChains(driver).move_by_offset(
                        xoffset=track, yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）
                    time.sleep(0.002)
                # ActionChains(driver).move_by_offset(xoffset=-random.randint(0, 1), yoffset=0).perform()   # 微调，根据实际情况微调
                time.sleep(1)
                # 释放鼠标
                ActionChains(driver).release(on_element=slid_ing).perform()
                time.sleep(2)
                try:
                    driver.find_element(
                        By.XPATH, '# /html/body/div[1]/div[1]/ul')
                    print('登录成功')
                    break
                except:
                    auto.alert(text='如果已经进入空间，请确定\n如果未通过验证码，请手动通过\n如果出现环境异常，请先于客户端登录,再等下次验证码无法通过后手动点击头像登录\n登录完成后进入空间点击确定，开始爬虫',
                            title='空间分析器 by.L1_Sta2', button='OK')
                    break
                    # driver.quit() os.startfile(auto.prompt(text = '请输入qq的绝对路径', title='空间分析器 By.L1_Sta2',default =
                    # 'D:\qq\Bin\QQScLauncher.exe')) time.sleep(1) pg.typewrite('**********', 0.1) pg.press('tab')
                    # pg.typewrite('**********', 0.1) pg.press('enter') driver.get(self.url)
        except:
            auto.alert(text='可能没有拖块验证码或者是需要手机验证码,请手动登录后点击ok',button='OK')
        # 以上为验证码部分############################

        # 以下为爬虫部分##############################
        driver.switch_to.window(driver.current_window_handle)
        time.sleep(2)
        cnt = int(driver.find_element(
            By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div/div/ul/li[2]/a/strong').get_attribute('textContent'))
        # 根据总条数计算大概所需时间
        need_time = cnt*3/8
        print(f'共有{cnt}条说说 预计用时{need_time}s\n八成是偏长的\n以后的版本当中会用机器学习预测')
        # 测试当中800条大概300s 不一定准确 大部分时候都会偏长
        driver.switch_to.frame('QM_Feeds_Iframe')

        saysay = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/ul')
        # 找到所有说说
        singal_say = saysay.find_elements(By.XPATH, 'li')
        # print(len(sinal_say))
        i = 1
        n = len(singal_say)
        ls = {}
        start = time.time()
        endtime = time.time()
        time_xpath = 'div[1]/div[4]/div[2]/span'
        info_xpath = 'div[2]/div/div[1]'
        like_xpath = 'div[3]/div[3]/div[2]'
        try:
            while endtime - start < need_time:  # 设置爬取时间
                while i < n:
                    now_xpath = f'/html/body/div[1]/div[1]/ul/li[{i}]'
                    now_say_say = driver.find_element(By.XPATH, now_xpath)
                    # 找到了每个说说的框架
                    # /html/body/div[1]/div[1]/ul/li[i]/div[1]/div[4]/div[2]/span
                    # 时间在的xpath完整路径
                    time1 = now_say_say.find_element(
                        By.XPATH, time_xpath).get_attribute('textContent')
                    info = now_say_say.find_element(
                        By.XPATH, info_xpath).get_attribute('textContent')
                    if i <= 50:
                        like_ls = now_say_say.find_elements(
                            By.XPATH, like_xpath)
                        for each in like_ls:
                            ls2 = (re.findall(
                                r'/\d{6,12}', str(each.get_attribute('innerHTML'))))
                    else:
                        ls2 = []
                    info += (''.join(ls2))
                    if not ('年' in time1):
                        time1 = str(datetime.now().year) + '年' + time1
                    ls[time1] = info
                    i += 1
                    print(f'正在爬取第{i}条说说, 总用时{time.time() - start :.2f}s')
                # 没有了就执行翻页
                driver.find_element(
                    By.XPATH, '/html/body').send_keys(Keys.PAGE_DOWN)
                driver.find_element(
                    By.XPATH, '/html/body').send_keys(Keys.PAGE_DOWN)
                n = len(saysay.find_elements(By.XPATH, 'li'))
                endtime = time.time()
        except:
            print('异常退出或已经爬取到底，数据已保存')
            print(f'退出前爬取至第{i}条说说')
            print(f'退出的内容\"{info}\",日期{time1}')
            
            with open(f"./jsons/{self.target}.json", "w") as f:
                f.write(json.dumps(ls, ensure_ascii=True,
                                   indent=4, separators=(',', ':')))
        # 以上为爬虫部分#######################################
        # 执行完毕 保存
        print(f'{endtime - start :.2f}s爬取时间结束，对{i}条说说进行保存')

        with open(f'./jsons/{self.target}.json', "w") as f:
            f.write(json.dumps(ls, ensure_ascii=True,
                               indent=4, separators=(',', ':')))

        print(f'所有数据如下\n{ls}')
        driver.quit()
        return ls
        # 以上为爬虫部分

    def csv_is_exist(self):
        """
        判断数据是否存在
        """
        return (f'{self.target}空间数据集.csv') in os.listdir(r'./csvs')

    def ls_to_csv(self):
        """
        将已经保存的json数据转为csv
        """
        with open(f'./jsons/{self.target}.json', 'r') as file:
            data = json.load(file)
            # 获取保存的键值对
        date_ = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日', ' '.join(data.keys()))
        time_ = re.findall(r'\d{2}:', ' '.join(
            data.keys()))  # 去掉后面的\d{2}这样只匹配时间
        single_ls = []
        array_ = []
        # print(date_, time_)
        for x, i in enumerate(date_):
            # 对日期切分
            year, month, day = i.replace(
                '年', '-').replace('月', '-').replace('日', '').split('-')
            week_day = calendar.weekday(int(year), int(month), int(day))
            single_ls.append(year)
            single_ls.append(month)
            single_ls.append(day)
            single_ls.append(week_day+1)
            # 星期数比原来少1
            single_ls.append(int(time_[x][:-1]))
            single_ls.append(list(data.values())[x].strip())
            single_ls.append(re.findall(
                r'/\d{6,12}', list(data.values())[x].strip()))
            array_.append(single_ls)
            single_ls = []
        data = pd.DataFrame(
            array_, columns=['year', 'month', 'day', 'week_day', 'time', 'saying', 'like'])
        # print(array_)
        data.to_csv(f'./csvs/{self.target}空间数据集.csv', index=False)

    def most_time_in_year(self):
        '''
        绘制每年最常发说说的时间段的函数(时间段-月份)
        '''
        data = self.data
        for year in data['year'].unique():
            yearly_data = data[data['year'] == year]
            yearly_data = yearly_data
            # print(yearly_data)
            ls = []
            for month in sorted(yearly_data['month'].unique()):
                ls.append((yearly_data[yearly_data['month'] == month])[
                          'time'].mode().values[0])

            # print(ls)
            label = str(year)
            plt.plot(sorted(yearly_data['month'].unique()), ls, label=label)
        plt.xticks(range(1, 13))
        plt.xlabel('月份/月')
        plt.yticks(range(24))
        plt.ylabel('时间段(左端点)/时')
        plt.legend()
        plt.grid(linestyle='--', color='y')
        plt.title('最常发说说的时间段')
        f = plt.gcf()
        plt.show()
        f.savefig(f'./results/{self.target}年份时间段.jpg')

    def most_year(self):
        """
        绘制饼图，展示哪一年说说总数最多
        """
        print('数据如下：')
        data = self.data = pd.read_csv(f'./csvs/{self.target}空间数据集.csv', header=0)
        ls = {}
        for i in data['year'].unique():
            ls[i] = len(data[data['year'] == i])
        for i in ls.keys():
            print(f'{i}年共发了{ls[i]}条说说,占比{ls[i]/sum(ls.values())*100 :.2f}%')
        plt.pie(ls.values(), labels=ls.keys(), startangle=90, autopct='%1.2f%%')
        plt.legend()
        plt.title('每年说说数量')
        f = plt.gcf()
        plt.show()
        f.savefig(f'./results/{self.target}饼图.jpg')

    def most_week_day_in_year(self):
        """
        绘制每年最常发说说的时间段的函数(时间段-星期)
        """
        data = self.data
        for year in data['year'].unique():
            yearly_data = data[data['year'] == year]
            yearly_data = yearly_data
            # print(yearly_data)
            ls = []
            for week_day in sorted(yearly_data['week_day'].unique()):
                ls.append((yearly_data[yearly_data['week_day'] == week_day])[
                          'time'].mode().values[0])

            # print(ls)
            label = str(year)
            plt.plot(sorted(yearly_data['week_day'].unique()), ls, label=label)
        plt.xticks(range(1, 8))
        plt.xlabel('星期')
        plt.yticks(range(24))
        plt.ylabel('时间段(左端点)/时')
        plt.legend()
        plt.grid(linestyle='--', color='y')
        plt.title('最常发说说的时间段')
        f = plt.gcf()
        plt.show()
        f.savefig(f'./results/{self.target}星期时间段.jpg')

    def most_times_each_month(self):
        """
        每月说说次数柱形图
        """
        data = self.data
        max_lenth = 0
        width = 0.18
        mid = width * 6 / 2
        add_width = 0
        for year in data['year'].unique():
            yearly_data = data[data['year'] == year]
            yearly_data = yearly_data
            label = str(year)
            lenth = []
            ls_month = []
            for month in sorted(yearly_data['month'].unique()):
                ls_month.append(month + add_width - mid)
                lenth.append(len(yearly_data[yearly_data['month'] == month]))
                max_lenth = max(max_lenth, len(
                    yearly_data[yearly_data['month'] == month]))
            plt.bar(ls_month, lenth, label=label, width=width)
            add_width += width
        plt.yticks(range(0, max_lenth + 1, 5))
        plt.xticks(range(1, 13))
        plt.title('每月发说说次数')
        plt.xlabel('月份/月')
        plt.ylabel('次数/次')
        plt.legend()
        plt.grid(linestyle='--')
        f = plt.gcf()
        plt.show()
        f.savefig(f'./results/{self.target}每月数量.jpg')

    def word_cloud(self):
        """
        统计空间词频并绘制词云
        """
        data = self.data
        word = ''.join(map(str, (data['saying'].values)))
        # print(word)
        chinese = jieba.lcut(
            ''.join(re.findall(r'[\u4e00-\u9fa5]', word)), cut_all=True)
        ch_fre = collections.Counter(chinese)
        # print(ch_fre)
        stop_ls = {'啊啊啊', '相册', '自来', '今天', '就是', '还是', '个人', '真的', '一天', '不知', '可以', '哈哈哈', '自小', '什么', '来自',
                   '一个', '全文', '展开', '查看', '照片', '视频', '上传', '小米', '手机', '不会', '不是', '没有', '自己', '你们', '已经', '不要', '来自'}
        for i, v in ch_fre.items():
            # en_fre[translater.translate(i, dest='en', src='zh-CN').text] = v
            if i in stop_ls or len(i) == 1:
                ch_fre[i] = -1
        ch_fre = dict(ch_fre.most_common(50))
        # mask = np.array(Image.open('./image/abc.png'))
        wc = WordCloud(
            font_path="C:\Windows\Fonts\STHUPO.TTF",  # 这里要注意啦
            max_words=100,
            width=1440,
            height=1440,
            # mask=mask,
            background_color='white',
        )
        word_cloud = wc.generate_from_frequencies(ch_fre)
        word_cloud.to_file(f"./results/{self.target}词云.jpg")
        plt.imshow(word_cloud)
        plt.axis("off")
        plt.show()

    def pre_most_time_each_month(self):
        """
        对每个月发说说时间段进行分析
        若回归准确度较高会进行线性回归
        """
        x = self.data['month'].astype(int).tolist()
        y = self.data['time'].astype(int).tolist()
        now_data = pd.DataFrame({"month": x, "time": y})
        ls = {}
        col = sorted(now_data['month'].unique())
        for i in col:
            ls[i] = (now_data[now_data['month'] == i])['time'].values.tolist()
        ls = pd.DataFrame.from_dict(ls, orient='index').T
        # print(ls.describe())
        ls.boxplot()
        plt.title('每月发说说时间段箱式图')
        plt.xlabel('月份/月')
        plt.ylabel('时间段(左端点)/点')
        plt.show()
        des = ls.describe().fillna(0)
        # print(des)
        flag = 0
        for i in des.index:
            r, p = (stats.pearsonr(
                (des.loc[i].index.tolist()), des.loc[i].values.tolist()))
            if p < 0.05:
                if r > 0:
                    print(f"{i}和月份存在显著正相关关系,相关系数r={r :.3f}")
                else:
                    print(f"{i}和月份存在显著负相关关系,相关系数r={r :.3f}")
                x = np.array(col).reshape(-1, 1)
                y = np.array(des.loc[i].values.tolist()).reshape(-1, 1)
                # print(x, y)
                clf1 = LinearRegression()
                clf1.fit(x, y)
                y_l = clf1.predict(x)  # 线性回归预测值

                # 非线性回归
                # 根据degree的值转换为相应的多项式（非线性回归）
                ployfeat = PolynomialFeatures(degree=5)
                x_p = ployfeat.fit_transform(x)
                clf2 = LinearRegression()
                clf2.fit(x_p, y)
                plt.plot(x, y_l, label="线性回归")
                plt.scatter(x, y, label="实际值")
                plt.plot(x, np.matmul(x_p, clf2.coef_.reshape(
                    6, 1)) + clf2.intercept_, label="非线性回归")
                plt.legend()
                plt.xlabel('月份/月')
                plt.ylabel(i)
                plt.title(f'{i}值的拟合效果')
                f = plt.gcf()
                plt.show()
                f.savefig(f'./results/{self.target}{i}回归拟合.jpg')
                print("{}和月份线性回归方程为: y = {:.3f} + {:.3f}x".format(i,
                      clf1.intercept_[0], clf1.coef_[0, 0]))
                print("{}和月份非线性回归曲线方程为 y = {:.3f}+{:.3f}x+{:.3f}x^2+{:.3f}x^3+{:.3f}x^4+{:.3f}x^5".format(i, clf2.intercept_[
                      0], clf2.coef_[0, 1], clf2.coef_[0, 2], clf2.coef_[0, 3], clf2.coef_[0, 4], clf2.coef_[0, 5]))
                print(f"P={p:.3f},可以认为变量之间相关关系显著")

                flag = 1
            else:
                print(f"P={p:.3f},可以认为{i}和月份不存在显著线性相关关系。")
        else:
            if flag == 0:
                print('无有相关关系的数据,无法进行线性回归和预测')
        print('count可以进行非线性回归')
        i = 'count'
        x = np.array(col).reshape(-1, 1)
        y = np.array(des.loc[i].values.tolist()).reshape(-1, 1)
        # print(x, y)
        clf1 = LinearRegression()
        clf1.fit(x, y)
        y_l = clf1.predict(x)  # 线性回归预测值
        # 非线性回归
        ployfeat = PolynomialFeatures(degree=5)  # 根据degree的值转换为相应的多项式（非线性回归）
        x_p = ployfeat.fit_transform(x)
        clf2 = LinearRegression()
        clf2.fit(x_p, y)
        plt.plot(x, y_l, label="线性回归")
        plt.scatter(x, y, label="实际值")
        plt.plot(x, np.matmul(x_p, clf2.coef_.reshape(6, 1)) +
                 clf2.intercept_, label="非线性回归")
        plt.legend()
        plt.xticks(col)
        plt.grid(linestyle='--')
        plt.xlabel('月份')
        plt.title('每月说说数量和月份关系的回归拟合图')
        plt.ylabel('说说条数')
        f = plt.gcf()
        plt.show()
        f.savefig(f'./results/{self.target}非线性回归.jpg')
        # print("{}和月份线性回归方程为: y = {} + {}x".format(i, clf1.intercept_[0],clf1.coef_[0,0]))
        print("{}和月份非线性回归曲线方程为 y = {:.3f}+{:.3f}x+{:.3f}x^2+{:.3f}x^3+{:.3f}x^4+{:.3f}x^5".format(i,
              clf2.intercept_[0], clf2.coef_[0, 1], clf2.coef_[0, 2], clf2.coef_[0, 3], clf2.coef_[0, 4], clf2.coef_[0, 5]))

    def most_like(self):
        """
        打印最常点赞的人
        """
        data = data = pd.read_csv(f'./csvs/{self.target}空间数据集.csv', header=0)
        try:
            ls = []
            most_ = (collections.Counter("".join(data['like'].values.tolist()).replace(
                '/', '').replace('[', '').replace(']', '').split(',')))
            most_ = dict(most_.most_common(1))
            qq = (list(most_.keys())[0])
            times = (list(most_.values())[0])
            print(f'\n最常给您点赞的人是{qq}\n在最近的说说中共给您点赞{times}次！')
        except:
            print('版本已经更新,请更新数据以获取最多点赞人！')


if __name__ == '__main__':
    an = QQSpider()
    # 以下是很久之后修改的 可能出现问题
    try:
        ls = an.main()
        an.ls_to_csv()
    except:
        an.ls_to_csv()
    # 以上是很久之后修改的 可能出现问题
    '''
    5.2日作者注
    这里是修改了提醒更新和登录的顺序，检索到本地文件先会提醒更新
    如果不更新则会在init当中直接结束，就不会打开浏览器和进行之后的设置
    所以后续使用main()函数就会报错 这时用异常捕获可以直接跳过
    5.5日作者注
    这样会导致无法在main当中debug
    '''
    an.most_year()
    an.most_like()
    an.most_time_in_year()
    an.most_week_day_in_year()
    an.most_times_each_month()
    an.word_cloud()
    an.pre_most_time_each_month()