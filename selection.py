import requests
from multiprocessing import Pool

BIG = '!Wh55ta8qt028Wlpe81r07ce++UESxkny8bfrfoakthtlsMmQQVux3qeuXyqg1U1v0HpTNHUDp3oiSx4='
JSESSIONID = 'D08C14C554C424233DF94B522C255C8E'


def function(id):
    url = f"http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=202320242{id}&xkzy=&trjf="
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Content-Type': 'application/json; charset=utf-8',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'Host': 'csujwc.its.csu.edu.cn',
        'Referer': 'http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/comeInBxqjhxk',
        'xtbz': 'cloud',
        'Cookie': 'BIGipServero5E8DA9Hppp9PO46RpPJdw=' + BIG + '; JSESSIONID=' + JSESSIONID,
        'Sec-Ch-Ua-Platform': "Windows",
    }
    response = requests.get(url, headers=headers)
    while response.status_code == 200:
        if response.json()['success']:
            print("选课成功！")
            return True
        else:
            print(f"{id}选课失败...")
            return False
    else:
        print(f"API异常:\n{response.text}")


def process_course(course_id):
    while not function(course_id):
        # 一直尝试，直到课程选择成功
        pass


if __name__ == "__main__":
    # 课程ID列表，尝试选择课程
    course_ids = [
        "018750",
        "018752",
        "018774",
        "018769",
        "018772",
        "018768",
        "018776",
        "018773",
        "018770",
        "018763",
        "018335",
        "018301"
    ]
    # 使用进程池来并行处理多个课程
    with Pool(processes=len(course_ids)) as pool:
        pool.map(process_course, course_ids)
