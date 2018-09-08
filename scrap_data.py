import PyPDF2
import textract

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

punctuations = ['(', ')', ';', ':', '[', ']', ',', '.', "'s", '-']
stop_words = stopwords.words('english')

pdf = open("dataset/15147_split_1.pdf", 'rb')

#txt = open("15147_split_1", 'a')

reader = PyPDF2.PdfFileReader(pdf)
text = ""

n = reader.numPages
for i in range(n):
    obj = reader.getPage(i)
    text += obj.extractText()
tokens = word_tokenize(text, 'english')
words = [word.lower() for word in tokens if not word.lower() in stop_words and not word.lower() in punctuations]
print(words)
