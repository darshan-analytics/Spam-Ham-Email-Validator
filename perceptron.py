import io
import operator
import os
import string
import nltk
import random
import math
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords



count_ham_files = len(os.listdir("train/ham/"))
count_spam_files = len(os.listdir("train/spam/"))
total_no_of_files = count_ham_files + count_spam_files
tokenizer = RegexpTokenizer("[a-zA-Z]+")
x = [os.path.join(r, file) for r, d, f in os.walk("train\\spam") for file in f]

    # print(x)
y = [os.path.join(r, file) for r, d, f in os.walk("train\\ham") for file in f]

    # print(y)

training_files = y + x


stemmer = SnowballStemmer("english")

p = [os.path.join(r, file) for r, d, f in os.walk("test\\spam") for file in f]

# print(x)
q = [os.path.join(r, file) for r, d, f in os.walk("test\\ham") for file in f]
ham_test = q
spam_test = p

ham_files = y
spam_files = x

#result_list2 =[]

flag = 0

stopword = set(stopwords.words('english'))

def predict_all_weights(w, input_file, filter_stopwords):
    phi = create_features(input_file, filter_stopwords)
    result = predict_one(w, phi)
    #print(result)
    return result


def create_features(x, flag):
    phi = {}
    words = x.split()
    for word in words:
        #print(word)
        '''
        if word in string.punctuation and (1 or stopword)
        print(okay)
        '''
        if word in string.punctuation or (flag and word in stopword):
            continue

        if word not in phi:
            phi[word] = 0
        phi[word] += 1
    return phi




def predict_one(weight_map, phi):
    score = 0
    for name, value in phi.items():
        if name in weight_map:
            score += value * weight_map[name]
    if score >= 0:
        return 1
    return -1


def weight_maps(w, data, flag):
    data = data.split()
    #print(data)
    for _data in data:
        if _data in string.punctuation or (flag and _data in stopword) :
            continue
        if _data not in w:
            w[_data] = 0
    return w

def update_weights(w, phi, y, res, eta):
    for name, value in phi.items():
        w[name] += value * (y-res) * eta


weight_map = {}


def perceptron_with_stopwords():
    training_set = os.getcwd() + '/train' #current directory with train data
    dir = os.listdir(training_set)
    weight_map ={}
    for i in range(0,20):
        eta = random.uniform(0.08, 0.2)
        iter = random.randrange(0,20)



        for _directory in dir:
                url = training_set + '/' + _directory
                filelist = os.listdir(url)
                for file in filelist:
                    with io.open(url + '/' + file, 'r', encoding='latin1') as fp:
                        content = fp.read()
                        for word in content:

                            word = content.lower()

                            content = word

                        weight_map = weight_maps(weight_map, content, 0)
                        for _it in range(iter):

                            phi = create_features(content, 0)
                            check_result = predict_one(weight_map, phi)
                            if check_result != _directory == 'spam':
                                update_weights(weight_map, phi, 1, check_result, eta)
                for file in filelist:
                    with io.open(url + '/' + file, 'r', encoding='latin1') as fp:
                        content = fp.read()
                        for word in content:
                            word = content.lower()
                            content = word

                        weight_map = weight_maps(weight_map, content, 0)
                        for _it in range(iter):

                            phi = create_features(content, 0)
                            check_result = predict_one(weight_map, phi)
                            if check_result != _directory == 'ham':
                                update_weights(weight_map, phi, -1, check_result, eta)

        result_list = []
        test_set = os.getcwd() + '/test'
        dir = os.listdir(test_set)
        for _directory in dir:

                url = test_set + '/' + _directory
                filelist = os.listdir(url)
                for file in filelist:

                    if _directory == 'spam':
                        targeted_output = 1

                    else:
                        _directory = 'ham'
                        targeted_output = -1

                    with io.open(url + '/' + file, 'r', encoding='latin1') as fp:
                        content = fp.read()
                        for word in content:
                            word = content.lower()
                            content = word
                        result = predict_all_weights(weight_map, content, 0)
                        result_list.append(1 if result == targeted_output else 0)

        accuracy = float(result_list.count(1)) / float(total_no_of_files) * 100


        print('%2f' % accuracy)






def perceptron_without_stopwords():
    training_set = os.getcwd() + '/train'
    dir = os.listdir(training_set)
    weight_map ={}
    flag =1

    for i in range(0, 20):
        eta = random.uniform(0.08, 0.2)
        iter = random.randrange(0, 20)



        for _directory in dir:
            url = training_set + '/' + _directory
            filelist = os.listdir(url)
            for file in filelist:
                with io.open(url + '/' + file, 'r', encoding='latin1') as fp:
                    content = fp.read()
                    for word in content:
                        word = content.lower()
                        content
                    for word in content:
                        if word in string.punctuation or (flag and word in stopword):
                            word = content.lower()

                            content = word

                    weight_map = weight_maps(weight_map, content, 1)
                    for _it in range(iter):

                        phi = create_features(content, 1)
                        check_result = predict_one(weight_map, phi)
                        if check_result != _directory == 'spam':
                            update_weights(weight_map, phi, 1, check_result, eta)
            for file in filelist:
                with io.open(url + '/' + file, 'r', encoding='latin1') as fp:
                    content = fp.read()
                    for word in content:
                        if word in string.punctuation or (flag and word in stopword):
                            word = content.lower()

                            content = word
                    weight_map = weight_maps(weight_map, content, 1)
                    for _it in range(iter):

                        phi = create_features(content, 1)
                        check_result = predict_one(weight_map, phi)
                        if check_result != _directory == 'ham':
                            update_weights(weight_map, phi, -1, check_result, eta)

        result_list = []
        test_set = os.getcwd() + '/test'
        dir = os.listdir(test_set)
        for _directory in dir:

            url = test_set + '/' + _directory
            filelist = os.listdir(url)
            for file in filelist:

                if _directory == 'spam':
                    correct_op = 1

                else:
                    _directory = 'ham'
                    correct_op = -1

                with io.open(url + '/' + file, 'r', encoding='latin1') as fp:
                    content = fp.read()
                    for word in content:
                        if word in string.punctuation or (flag and word in stopword):

                            word = content.lower()

                            content = word
                    result = predict_all_weights(weight_map, content, 1)
                    result_list.append(1 if result == correct_op else 0)

        accuracy = float(result_list.count(1)) / float(total_no_of_files) * 100


        print('%2f' %accuracy)




print('Accuracy with stopwords:')
out = perceptron_with_stopwords()




print('Accuracy without stopwords:')
out2 = perceptron_without_stopwords()


