# -*- coding: utf-8 -*-
import codecs
import jieba
from gensim.models import word2vec
import logging
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def processing(resources, resources_fenci_result, ChSentiment_file, ChSentiment_result):
    #对用来扩充情感词典的语料进行分词处理，将处理结果存入resources_fenci_result文档里
    f1 = codecs.open(resources)
    f2 = codecs.open(resources_fenci_result, 'a')
    lines = f1.readlines()  # 读取全部内容
    for line in lines:
        line.replace('\t', '').replace('\n', '').replace(' ', '').replace('(','')
        seg_list = jieba.cut(line, cut_all=False)
        f2.write(" ".join(seg_list))

    f1.close()
    f2.close()

    #对HowNet词典里的词语进行预处理，将处理结果存入ChSentiment_result文档里
    f3 = codecs.open(ChSentiment_file)
    f4 = codecs.open(ChSentiment_result, 'a')
    lines = f3.readlines()  # 读取全部内容
    for line in lines:
        f4.write(line.replace('\n','')+" ")

    f3.close()
    f4.close()

def dictionary_expansion(resources_fenci_result, Dic_path, n):
    """
    :param Dic_path:（填入'ChDic/positiveSort.txt'或者'ChDic/negativeSort.txt'）
           n:情感词典扩充循环迭代次数（本项目设置为8）
    :return:
    """
    # 主程序
    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus(resources_fenci_result)  # 加载语料
    model = word2vec.Word2Vec(sentences, size=200)  # 训练skip-gram模型，默认window=5

    print model
    i = 0
    for i in xrange(0,n): #设置情感词典扩充的循环迭代次数为n
        with codecs.open(Dic_path,'r') as f:
            for word in f.readlines():
                try:
                    # 计算某个词的相关词列表
                    word = '美國'
                    print "和"+ word+ "相关度由高到低的10个词有：\n"
                    similar_list = model.most_similar(word , topn=10)  # 取前10个相关程度较高的词组成列表
                    for item in similar_list:
                        # with open('item', 'a') as f1:
                        #     f1.write(item[0])
                        # print item[0], item[1]
                    # print"-----\n"
                        with codecs.open(Dic_path,'a') as f:
                            f.write(item[0]+'\n') #将计算得到的相关词依次加入情感词典中
                except:
                    continue
        i += 1
        print "循环迭代次数为"+ str(i)
        if i == n:
             break


def dictionary_filter(dic_path, HWDic,ChSentiment_result, word): #利用HowNet词典对扩充后的情感词典进行筛选

    with codecs.open(HWDic) as f:
        for HWword in f.readlines():
            #如果在HowNet词典中含有该词，但相似度小于0.5,则将该词剔除
            if word == HWword:
                print word
                # 计算word和HWword的相似度/相关程度,如果小于0.5,则将其从情感词典里剔除
                try:
                    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
                    sentences = word2vec.Text8Corpus(ChSentiment_result)  # 加载语料
                    model = word2vec.Word2Vec(sentences, size=200)  # 训练skip-gram模型，默认window=5
                    similarity = model.similarity(word, HWword)
                except KeyError:
                    similarity = 0
                print word + "和" + HWword+u"的相似度为：", similarity
                if similarity <0.5:
                    dic_path.remove(word)
            #如果在HowNet词典中不含该词，则视此词为新词保留
            else:
                continue


if __name__ == '__main__':
    resources = "resources"
    resources_fenci_result = "resources_fenci_result"
    ChSentiment_file = "ChSentiment"
    dic_path = 'ChDic/positiveSort.txt'
    ChSentiment_result = "ChSentiment_result"

    processing(resources, resources_fenci_result, ChSentiment_file, ChSentiment_result)
    dictionary_expansion(resources_fenci_result, dic_path, 8)
    with codecs.open(dic_path) as f:
        for word in f.readlines():
            dictionary_filter(f.readlines(), ChSentiment_file, ChSentiment_result, word)