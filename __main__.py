import csv
from DocumentSearch import DocumentSearch
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

TEXT_STORE_LOCATION = "scrap_data"
DATA_STORE_LOCATION = "dataset"
WORDS_DATA_LOCATION = "words_data"


def proxy_dist(a, b):
    return float(1)/(abs(a**2-b**2))


def main_search(m_words, m_data, w_count):
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
                    m_score += float(m_data[m_data[0].index(m_words[m_i])+1][1])/w_count
                if m_words[m_i+1] in m_data[0]:
                    m_score += float(m_data[m_data[0].index(m_words[m_i+1])+1][1])/w_count
    elif words[0] in m_data[0]:
        m_score += float(m_data[m_data[0].index(words[0])+1][1])/w_count
    return m_score


if __name__ == "__main__":
    query = input("Query : ")
    punctuations = ['(', ')', ';', ':', '[', ']', ',', '.', "'s", '-']
    stop_words = stopwords.words('english')
    tokens = word_tokenize(query, 'english')
    words = [word.lower() for word in tokens if not word.lower() in stop_words and not word.lower() in punctuations]
    print("\n".join(words))

    doc = DocumentSearch()
    csvFiles = doc.search("csv")
    dic = {}

    with open(WORDS_DATA_LOCATION+"/total", 'r') as w:
        words_count = int(w.readline())

    for csvData in csvFiles:
        with open(csvData) as f:
            reader = csv.reader(f)
            data = [list(d) for d in reader]
            # print(data)
            score = main_search(words, data, words_count)
            if score in dic:
                dic[score].append(csvData)
            else:
                dic[score] = [csvData]

    rank = 1
    for i in sorted(dic.keys(), reverse=True):
        for j in dic[i]:
            if rank > 5:
                if input("Next 5 ?") == "Y":
                    rank = 1
                    continue
                else:
                    break
            with open(j.replace(WORDS_DATA_LOCATION, TEXT_STORE_LOCATION).replace(".csv", "")) as final:
                loc = final.readline()
            print(rank, "->", loc, i)
            rank += 1
