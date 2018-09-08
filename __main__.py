from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

if __name__ == "__main__":
    query = input("Query : ")
    punctuations = ['(', ')', ';', ':', '[', ']', ',', '.', "'s", '-']
    stop_words = stopwords.words('english')
    tokens = word_tokenize(query, 'english')
    words = [word.lower() for word in tokens if not word.lower() in stop_words and not word.lower() in punctuations]
    print("\n".join(words))
