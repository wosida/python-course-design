import requests
from bs4 import BeautifulSoup
import csv
import jieba
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import random
import time
from multiprocessing import Pool
from fake_useragent import UserAgent

jieba.setLogLevel(jieba.logging.INFO)  # 设置jieba的日志等级,避免jieba分词时出现乱码
ua = UserAgent()  # User-Agent池

ip_pool = ['183.95.80.102:8080',
           '123.160.31.71:8080',
           '115.231.128.79:8080',
           '166.111.77.32:80',
           '43.240.138.31:8080',
           '218.201.98.196:3128',
           ]


def top250_crawer(_url, _sum):
    """
    爬取豆瓣电影top250的电影信息
    :param _url: 豆瓣电影top250的url
    :param _sum: 当前爬取的电影数量
    :return: 电影信息列表
    """

    # 设置随机user-agent，防止被封

    response = requests.get(_url, headers={'User-Agent': ua.random})
    soup = BeautifulSoup(response.text, 'html.parser')

    movie_info_list = []

    movie_items = soup.find_all('div', class_='item')
    i = _sum + 1
    for item in movie_items:
        print('正在爬取第{}条数据'.format(i))
        alltitle = item.find_all('span', class_='title')  # 正标题
        title = alltitle[0].text  # 正标题
        if len(alltitle) > 1:  # 如果title存在两个则表明存在副标题
            english_title = alltitle[1].text.split('/')[1].replace('\xa0', '')  # 英文标题
        else:
            english_title = '无'

        rating = item.select_one('.rating_num').text
        data = item.select('.bd p')[0].text.split('\n')
        year = data[2].replace(' ', '').split('/')[0].replace('\xa0', '')
        country = data[2].replace(' ', '').split('/')[1].replace('\xa0', '')
        _type = data[2].replace(' ', '').split('/')[2].replace('\xa0', '')
        director_and_protagonist = data[1].replace(' ', '').split('/')[0].replace('\xa0', '')
        official_link = item.find('a')['href']

        # 添加到电影信息列表
        movie_info_list.append({
            'Title': title,
            'English Title': english_title,
            'Type': _type,
            'Country': country,
            'Year': year,
            'Director and protagonist': director_and_protagonist,
            'Rating': rating,
            'Official Link': official_link
        })

        i += 1

    return movie_info_list


def introduce_and_short_review_crawer(filename):
    """
    爬取每部电影的简介和影评
    :param filename: csv文件名
    :return: 简介和影评列表
    """
    f = open(filename, 'r', encoding='utf-8')
    reader = csv.reader(f)
    url_list = []
    movie_info_list = []
    i = 1
    next(reader)
    for row in reader:
        url_list.append(row[-1])
    headers = {}
    # 爬取简介
    for _url in url_list:
        print('正在爬取电影简介和短评：{}'.format(i))
        # 设置随机user-agent，防止被封
        headers['User-Agent'] = ua.random
        headers['Cookie'] = 'bid=ss37xYushw0; douban-fav-remind=1; ll="118267"; _pk_id.100001.4cf6=2eedd59af45dc654.1686487432.; __yadk_uid=l1seDqEegIyLffyF3o2DBZJDHZNMjQS6; __gads=ID=112169f716b29dfc-221cb2297bd900b0:T=1675148592:RT=1686487437:S=ALNI_MZ_ADQYJRzn4S-JXbCu970CYgQ-ug; __gpi=UID=00000bb19aaa6a4e:T=1675148592:RT=1686487437:S=ALNI_MbKtgWMJ2_y4vJUfbbzAga_KYG-Ww; _vwo_uuid_v2=D525C0995AD6A63E36BA3B90916EABAFB|2e5b8311049575f6f6c090036a6ee251; viewed="27028517"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.27722; dbcl2="277226680:29VMkWO28EE"; ck=ffMv; __utmc=30149280; __utmc=223695111; frodotk_db="fa4f3d51b3b9024eeeedb7f51b2b06ea"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1705329523%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; __utma=30149280.1695083539.1675148594.1705327011.1705329523.25; __utmz=30149280.1705329523.25.20.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1585939636.1686487433.1705327011.1705329523.23; __utmz=223695111.1705329523.23.17.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0'

        response = requests.get(_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 简介
        if soup.find('span', class_='all hidden') is not None:
            introduce = ''.join(soup.find('span', class_='all hidden').text.split())
        else:
            introduce = ''.join(soup.find('span', property="v:summary").text.split())
        # 影评,爬取前10条短评
        short_review = ''.join(soup.find('div', class_='comment').find('span', class_='short').text.split())
        movie_info_list.append({
            '简介': introduce,
            '短评': short_review
        })
        i += 1
    return movie_info_list


def wordcloud_to_introduce_and_review(filename, num):
    """
    对简介和影评进行词云分析
    :param filename: csv文件名
    :param num: 分析电影数量
    :return: None
    """
    f = open(filename, 'r', encoding='utf-8')
    reader = csv.reader(f)
    next(reader)
    introduce_and_review_list = []
    # 读取前num部电影的简介和影评
    for i in range(num):
        introduce_and_review_list.append(next(reader))
    # 对简介和影评进行词云分析
    j = 1
    for movie_introduce_and_review in introduce_and_review_list:
        text = movie_introduce_and_review[0] + movie_introduce_and_review[1]
        # 使用jieba分词
        words = jieba.lcut(text)
        words_freq = {}
        for word in words:
            if len(word) > 1:
                words_freq[word] = words_freq.get(word, 0) + 1
        # 生成词云图
        wc = WordCloud(font_path="simsun.ttc", background_color='white',
                       mask=np.array(Image.open('background.jpg').convert('L')))
        wc.generate_from_frequencies(words_freq)
        # 存储词云图
        wc.to_file("D:/pythonProject/movie_cloud/movie_cloud_{}.png".format(j))
        j += 1


def reviews_crawer(filename, begin, end):
    """
    爬取每部电影的影评
    :param begin:
    :param filename: csv文件名
    :param end: 爬取电影数量
    :return:  None
    """
    # 爬取每部电影的简介和影评
    f = open(filename, 'r', encoding='utf-8')
    reader = csv.reader(f)
    url_list = []
    i = begin + 1
    next(reader)
    for row in reader:  # 电影的url
        url_list.append(row[-1])
    moviereviews_url_list = []  # 所有电影所有影评url列表
    for (_url) in url_list:
        moviereviews_url_list.append(_url + 'reviews')

    headers = {
        'User-Agent': ua.random,
        'Cookie': 'bid=ss37xYushw0; douban-fav-remind=1; ll="118267"; _pk_id.100001.4cf6=2eedd59af45dc654.1686487432.; __yadk_uid=l1seDqEegIyLffyF3o2DBZJDHZNMjQS6; __gads=ID=112169f716b29dfc-221cb2297bd900b0:T=1675148592:RT=1686487437:S=ALNI_MZ_ADQYJRzn4S-JXbCu970CYgQ-ug; __gpi=UID=00000bb19aaa6a4e:T=1675148592:RT=1686487437:S=ALNI_MbKtgWMJ2_y4vJUfbbzAga_KYG-Ww; _vwo_uuid_v2=D525C0995AD6A63E36BA3B90916EABAFB|2e5b8311049575f6f6c090036a6ee251; viewed="27028517"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.27722; dbcl2="277226680:29VMkWO28EE"; ck=ffMv; __utmc=30149280; __utmc=223695111; frodotk_db="fa4f3d51b3b9024eeeedb7f51b2b06ea"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1705329523%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; __utma=30149280.1695083539.1675148594.1705327011.1705329523.25; __utmz=30149280.1705329523.25.20.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1585939636.1686487433.1705327011.1705329523.23; __utmz=223695111.1705329523.23.17.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0'
    }
    proxies = {}
    reviews = []

    # 爬取
    for moviereviews_url in moviereviews_url_list[begin:end]:
        print('正在爬取电影影评：{}'.format(i) + time.strftime(" %Y-%m-%d %H:%M:%S", time.localtime()))
        # 随机选择user-agent和ip,防止被封
        headers['User-Agent'] = ua.random
        proxies['http'] = random.choice(ip_pool)
        time.sleep(random.randint(2, 4))
        response1 = requests.get(moviereviews_url, headers=headers)  # , proxies=proxies)
        if response1.status_code == 403:
            print('ip被封')
            break
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        # 影评
        all_review_html = soup1.find_all('div', class_='main-bd')[:10]  # 包含前十个影评herf的html块

        single_review_urls = []  # 十个影评的url列表

        for review_html in all_review_html:
            single_review_urls.append(review_html.a['href'])
        print(single_review_urls)

        for single_review_url in single_review_urls:
            headers['User-Agent'] = ua.random
            proxies['http'] = random.choice(ip_pool)
            time.sleep(random.randint(2, 4))
            response2 = requests.get(single_review_url, headers=headers)  # , proxies=proxies, )
            if response2.status_code == 403:
                print('ip被封')
                break
            soup2 = BeautifulSoup(response2.text, 'html.parser')
            # 影评
            if soup2.find('div', class_='review-content clearfix') is not None:
                review = ''.join(soup2.find('div', class_='review-content clearfix').text.split())
                reviews.append(review)
        # 保存影评
        with open('D:/pythonProject/reviews.txt', 'a', encoding='utf-8') as f:
            if f is None:
                print('文件打开失败')
            for review in reviews:
                f.write(str(moviereviews_url_list.index(moviereviews_url)) + ':' + str(review))
                f.flush()
                f.write('\n')
                f.flush()
        i += 1
        reviews.clear()
    f.close()


url = 'https://movie.douban.com/top250'

'遍历10页数据，250条结果'
if __name__ == '__main__':
    # 爬取豆瓣电影top250的电影信息
    _sum = 0
    movie_info = []
    for an in range(10):
        if _sum == 0:
            movie_info.extend(top250_crawer(url, _sum))
            _sum += 25
        else:
          page = '?start=' + str(_sum) + '&filter='
          new_url = url + page
          movie_info.extend(top250_crawer(new_url, _sum))
          _sum += 25

    # 写入csv文件
    with open('top250_movies.csv', 'w', newline='', encoding='utf-8') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=['Title', 'English Title', 'Type', 'Country', 'Year',
                                                     'Director and protagonist', 'Rating', 'Official Link'])

        writer.writeheader()
        for movie in movie_info:
            writer.writerow(movie)
    # 爬取每部电影的简介和短评
    movie_info_introduce_and_review = introduce_and_short_review_crawer('top250_movies.csv')
    # 写入csv文件
    with open('introduce_and_shortreview_part.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['简介', '短评'])
        writer.writeheader()
        for movie in movie_info_introduce_and_review:
            writer.writerow(movie)
    # 对简介和短评进行词云分析
    wordcloud_to_introduce_and_review('introduce_and_shortreview.csv', 10)

    # 爬取每部电影的影评
    # 多进程爬取,排序,去重
    pool = Pool(processes=10)
    for i in range(10):
        pool.apply_async(reviews_crawer, ('top250_movies.csv', i * 5, (i + 1) * 5))
    pool.close()
    pool.join()
    # 对多进程爬取后的影评进行去重
    with open('D:/pythonProject/reviews.txt', 'r', encoding='utf-8') as f:
        reviews = f.readlines()
        reviews = list(set(reviews))
    with open('D:/pythonProject/reviews.txt', 'w', encoding='utf-8') as f:
        for review in reviews:
            f.write(review)
            f.flush()
    # 排序
    with open('D:/pythonProject/reviews.txt', 'r', encoding='utf-8') as f:
        reviews = f.readlines()
        reviews.sort(key=lambda x: int(x.split(':')[0]))
    with open('D:/pythonProject/reviews.txt', 'w', encoding='utf-8') as f:
        for review in reviews:
            f.write(review)
            f.flush()
    # 单进程爬取
    reviews_crawer('top250_movies.csv', 0, 10)
