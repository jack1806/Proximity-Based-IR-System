import PyPDF2
import numpy as np
import csv

from DocumentSearch import DocumentSearch
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

TEXT_STORE_LOCATION = "scrap_data"
DATA_STORE_LOCATION = "dataset"
WORDS_DATA_LOCATION = "words_data"
CLICKS_LOCATION = "clicks.txt"
PDF_INDEX_LOCATION = "pdfindex.txt"
VOCA_LOCATION = WORDS_DATA_LOCATION+"/vocabulary"

punctuations = ['(', ')', ';', ':', '[', ']', ',', '.', "'s", "-", "*"]
stop_words = stopwords.words('english')

doc = DocumentSearch()
allFiles = doc.search("pdf")
done = 0
total_words = 0
clicks = []
indexes = [[], []]
vocab = []

for i in allFiles:
    pdf = open(i, 'rb')
    reader = PyPDF2.PdfFileReader(pdf)
    text = ""
    n = reader.numPages
    for j in range(n):
        obj = reader.getPage(j)
        text += obj.extractText()
    tokens = word_tokenize(text, 'english')

    words = [word.lower() for word in tokens if not word.lower() in stop_words and not word.lower() in punctuations]

    unique_elements, count_elements = np.unique(words, return_counts=True)

    np.asarray((unique_elements, count_elements))

    index_elements = []
    writeData = [[a for a in unique_elements]]

    indexes[0].append(str(allFiles.index(i)))
    indexes[1].append(i)

    for j in unique_elements:
        # index_elements.append([indexes for indexes, value in enumerate(words) if value == j])
        writeData.append([j, count_elements[list(unique_elements).index(j)], [z for z, val in enumerate(words) if val == j]])
        total_words += count_elements[list(unique_elements).index(j)]
        vocab.append(j)

    with open(WORDS_DATA_LOCATION+"/"+str(allFiles.index(i))+".csv", 'w') as words_data_file:
        writer = csv.writer(words_data_file)
        writer.writerows(writeData)

    clicks.append("1")

    scraped = open(TEXT_STORE_LOCATION+"/"+str(allFiles.index(i)), 'w')
    scraped.write(i+"\n"+("\n".join(words)))
    scraped.close()
    done += 1
    print("Progress ", done, "/", len(allFiles))

with open(VOCA_LOCATION, 'w') as w:
    w.write("\n".join(vocab))

with open(PDF_INDEX_LOCATION, 'w') as w:
    w.write(" ".join(indexes[0])+"\n"+" ".join(indexes[1]))

with open(CLICKS_LOCATION, 'w') as w:
    w.write(" ".join(clicks))

with open(WORDS_DATA_LOCATION+"/total", 'w') as w:
    w.write(str(total_words))
