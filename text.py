from text import split_chapter, word_cloud
import re

if __name__ == '__main__':
    output_filenames = split_chapter.split_chapter("D:\pythonProject\天龙八部第1章.txt", 5)
    for (filename) in output_filenames:
        print(filename)

    for filename in output_filenames:
        bg_image_path = "D:/pythonProject/background.jpg"  # 自行选择的背景图片路径
        output_excel = "D:/pythonProject/top_words/top_words_{}.xlsx".format(filename.split('/')[3].split('.')[0])
        word_cloud.generate_wordcloud_and_save(filename, bg_image_path, output_excel)

    # 手动选取的4个热词分别是：司空玄、龚光杰、少女、钟灵
    # 利用正则表达式匹配这4个热词在”天龙八部第1章“中出现的次数
    with open("D:\pythonProject\天龙八部第1章.txt", 'r', encoding='utf-8') as file:
        text = file.read()
        print("司空玄出现次数：", len(re.findall("司空玄", text)))
        print("龚光杰出现次数：", len(re.findall("龚光杰", text)))
        print("少女出现次数：", len(re.findall("少女", text)))
        print("钟灵出现次数：", len(re.findall("钟灵", text)))