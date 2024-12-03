# 根据电影的简介和评论，对电影进行分类
import csv
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import hamming_loss
import warnings
warnings.filterwarnings("ignore")
jieba.setLogLevel(jieba.logging.INFO)

# 读取简介和短评数据
f = open('introduce_and_shortreview.csv', 'r', encoding='utf-8')
reader = csv.reader(f)
next(reader)
movie = []
for row in reader:
    txt = row[0] + row[1]
    movie.append(txt)
f.close()
# 读取影评
f = open('reviews_new.txt', 'r', encoding='utf-8')
reviews = f.readlines()
f.close()
# 除去reviews列表中的空行
reviews = [review for review in reviews if review != '\n']
print(len(reviews))
# reviews中的每10条影评合并为一个字符串，加入到movie列表的相应元素中，形成新的movie列表
for i in range(0, len(reviews), 10):
    movie[i // 10] += ''.join(reviews[i:i + 10])
print(len(movie))
print(movie[0])
# 读取标签数据
f = open('top250_movies.csv', 'r', encoding='utf-8')
reader = csv.reader(f)
next(reader)
labels = []
for row in reader:
    labels.append(row[2])
f.close()
# 标签进行分词
labels = [[word for word in jieba.cut(label)] for label in labels]
# 向量化
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(movie)
print(X.shape)
# 标签二值化
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(labels)
# 打印标签
print(mlb.classes_)
# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)
# 多标签分类，使用SVC，采用OneVsRestClassifier策略
classifier = OneVsRestClassifier(SVC(kernel='linear', probability=True))
# 训练
classifier.fit(X_train, y_train)
# 预测
y_pred = classifier.predict(X_test)

# 评估
print("精确率:", precision_score(y_test, y_pred, average='samples'))
print("召回率:", recall_score(y_test, y_pred, average='samples'))
print("F1值:", f1_score(y_test, y_pred, average='samples'))
print("汉明损失:", hamming_loss(y_test, y_pred))

# 测试新的电影简介
print("请输入新的电影简介:")
new_synopsis = input()
new_vector = vectorizer.transform([new_synopsis])
# 更改阈值
predicted_labels = (classifier.predict_proba(new_vector) >= 0.15).astype(int)
print(predicted_labels)
print("预测的电影类型为:", mlb.inverse_transform(predicted_labels))
