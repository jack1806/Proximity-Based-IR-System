#!/usr/bin/python3

import csv
import nltk
import time
import sys
# from autocorrect import spell
from DocumentSearch import DocumentSearch
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

TEXT_STORE_LOCATION = "scrap_data"
DATA_STORE_LOCATION = "dataset"
WORDS_DATA_LOCATION = "words_data"
CLICKS_LOCATION = "clicks.txt"
PDF_INDEX_LOCATION = "pdfindex.txt"


def get_prior(text):
    lst = ['NN', 'NNS', 'NNP', 'NNPS', 'FW', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBP', 'VBN', 'VBP', 'VBZ', 'PRP', 'DT', 'IN', 'CD', 'EX', 'LS', 'MD', 'PDT', 'POS', 'PRP$', 'RP', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB']
    lst.reverse()
    tagged = nltk.pos_tag(text)
    list1 = []
    for gp_i in tagged:
        gp_j = (lst.index(gp_i[1])+1)/len(lst)
        list1.append(str(gp_j))
    return list1


def proxy_dist(a, b):
    return float(1)/(abs(a-b)**2)


def click_prob(a):
    return float(a)/(a+1)


def main_search(m_words, m_data, w_count, prior):
    m_score = float(0)
    if len(words) > 1:
        for m_i in range(len(m_words)//2):
            if m_words[m_i] in m_data[0] and m_words[m_i+1] in m_data[0]:
                ind1 = m_data[m_data[0].index(m_words[m_i])+1][2]
                ind2 = m_data[m_data[0].index(m_words[m_i+1])+1][2]
                ind1 = list(map(int, ind1[1:-1].split(",")))
                ind2 = list(map(int, ind2[1:-1].split(",")))
                for m_a in ind1:
                    for m_b in ind2:
                        m_score += proxy_dist(m_a, m_b)
            else:
                if m_words[m_i] in m_data[0]:
                    m_score += float(m_data[m_data[0].index(m_words[m_i])+1][1])*float(prior[m_i])/w_count
                if m_words[m_i+1] in m_data[0]:
                    m_score += float(m_data[m_data[0].index(m_words[m_i+1])+1][1])*float(prior[m_i+1])/w_count
    elif words[0] in m_data[0]:
        m_score += float(m_data[m_data[0].index(words[0])+1][1])/w_count
    return m_score


if __name__ == "__main__":

    doc = DocumentSearch()
    csvfiles = doc.search("csv")
    dic = {}
    indexes = [[], []]

    with open(PDF_INDEX_LOCATION, 'r') as w:
        indexes[0] = w.readline().split(" ")
        indexes[1] = w.readline().split(" ")

    with open(CLICKS_LOCATION, 'r') as clicksfile:
        clicks = list(map(int, clicksfile.readline().split(" ")))

    with open(WORDS_DATA_LOCATION+"/total", 'r') as w:
            words_count = int(w.readline())

    # print(sys.argv)
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1::])
    else:
        query = input("Query : ")

    start_time = time.time()

    # f_query = ""
    # for i in query.split():
    #     f_query += spell(i)+" "
    # query = f_query

    print(query)

    punctuations = ['(', ')', ';', ':', '[', ']', ',', '.', "'s", '-']
    stop_words = stopwords.words('english')
    tokens = word_tokenize(query, 'english')
    words = [word.lower() for word in tokens if not word.lower() in stop_words and not word.lower() in punctuations]

    word_weights = get_prior(words)

    if words:
        # print(" ".join(words))
        # print(" ".join(word_weights))

        for csvData in csvfiles:
            with open(csvData) as f:
                reader = csv.reader(f)
                data = [list(d) for d in reader]
                # print(data)
                score = main_search(words, data, words_count, word_weights)*click_prob(clicks[int(csvData.split("/")[-1].split(".")[0])])
                if score in dic:
                    dic[score].append(csvData)
                else:
                    dic[score] = [csvData]

        total_time_taken = time.time() - start_time

        rank = 1
        header_format = "%5s %15s %8s"
        result_format = "%5d %15.9f"
        print("Search finished in about %3.2f seconds..." % total_time_taken)
        final_arrays = []
        print(header_format % ("Rank", "Weight", "Name"))
        for i in sorted(dic.keys(), reverse=True):
            if i > float(0):
                for j in dic[i]:
                    with open(j.replace(WORDS_DATA_LOCATION, TEXT_STORE_LOCATION).replace(".csv", "")) as final:
                        loc = final.readline()
                    final_arrays.append(loc)
                    print((result_format % (rank, i)+"\t"+loc.split("/")[-1]).strip("\n"))
                    # print(rank, "->", loc.split("/")[-1])
                    rank += 1
        pdf_choose = int(input("Click the rank number of the pdf :"))
        choosen_name = final_arrays[pdf_choose-1].strip("\n")
        choosen_index = int(indexes[0][indexes[1].index(choosen_name)])
        print("Index of choosen is", choosen_index)
        clicks[choosen_index] += 1

        with open(CLICKS_LOCATION, 'w') as w:
            w.write(" ".join([str(i) for i in clicks]))

    else:
        print("Error")
