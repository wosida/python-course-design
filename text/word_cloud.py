import jieba
jieba.setLogLevel(jieba.logging.INFO) # 设置jieba的日志等级,避免jieba分词时出现乱码
from wordcloud import WordCloud
import pandas as pd
import numpy as np
from PIL import Image

# 定义函数用于提取热词并生成词云图
def generate_wordcloud_and_save(filename, bg_image_path, output_excel):
    """
    生成词云图并保存
    :param filename:
    :param bg_image_path:
    :param output_excel:
    :return: None
    """
    text = open(filename, 'r', encoding='utf-8').read()

    # 使用jieba分词
    words = jieba.lcut(text)
    words_freq = {}
    for word in words:
        if len(word) > 1:  # 只保留长度大于1的词
            words_freq[word] = words_freq.get(word, 0) + 1

    # 生成词云图
    wc = WordCloud(font_path="simsun.ttc", background_color='white', mask=np.array(Image.open(bg_image_path).convert('L')))
    wc.generate_from_frequencies(words_freq)

    # 存储词云图
    wc.to_file("D:/pythonProject/wordcloud/wordcloud_{}.png".format(filename.split('/')[3].split('.')[0]))
    print(filename.split('/')[3].split('.')[0], "词云图已保存！")

    # 获取排名前五的热词内容和出现次数
    top_words = sorted(words_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    top_words_df = pd.DataFrame(top_words, columns=['热词内容', '出现次数'])

    # 存储至Excel表格
    top_words_df.to_excel(output_excel, index=False)
    print(filename.split('/')[3].split('.')[0], "热词已保存！")



