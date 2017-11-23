import unidecode
from nltk import LancasterStemmer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity, stopwords
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.tokenize import TweetTokenizer

# NLTK stuff
tweet_tokenizer = TweetTokenizer()
stopwords = sorted(stopwords.words('spanish') + ['rt'])
stemmer = LancasterStemmer()

# Regex stuff
regex_url = re.compile('((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?')
regex_ht_mn = re.compile('(#|@)[\w]*')
regex_spaces = re.compile('[ ]+')
regex_nonword = re.compile('[\W]+')
regex_repeated_ch = re.compile(r'(\w*)(\w)\2(\w*)')
regex_ch = r'\1\2\3'

# Feature stuff
def get_words_in_tweets(tweets):
    all_words = []
    for words in tweets:
      all_words.extend(words[0])
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def remove_repeated_chars(word):
    repl_word =	regex_repeated_ch.sub(regex_ch, word)
    if repl_word !=	word:
        return remove_repeated_chars(repl_word)
    else:
        return repl_word

# Tweet loading and cleaning
wrong = 0
with open('neg.txt', 'r',encoding='utf8') as f:
    negtweets = []
    for line in f.readlines():
        tweet = line.replace('\n','')
        # Removal of URLs, hashtags and mentions
        tweet_regex = regex_spaces.sub(' ', regex_ht_mn.sub('', regex_url.sub('', tweet))).lower()
        # Removal of caps and accents
        tweet_raw = unidecode.unidecode(tweet_regex).lower()
        tokens = [
            remove_repeated_chars(stemmer.stem(t))
            for t in tweet_tokenizer.tokenize(tweet_regex) if not t in stopwords and not regex_nonword.match(t)
            ]
        negtweets.append(([tokens,'neg']))

with open('pos.txt', 'r',encoding='utf8') as f:
    postweets = []
    for line in f.readlines():
        tweet = line.replace('\n','')
        # Removal of URLs, hashtags and mentions
        tweet_regex = regex_spaces.sub(' ', regex_ht_mn.sub('', regex_url.sub('', tweet))).lower()
        # Removal of caps and accents
        tweet_raw = unidecode.unidecode(tweet_regex).lower()
        tokens = [
            remove_repeated_chars(stemmer.stem(t))
            for t in tweet_tokenizer.tokenize(tweet_regex) if not t in stopwords and not regex_nonword.match(t)
            ]
        postweets.append(([tokens,'pos']))

#Separar en training y test sets
neglength = len(negtweets)
poslength = len(postweets)

trainingtweets = postweets[poslength//4:]+negtweets[neglength//4:]
testingtweets = postweets[:poslength//4]+negtweets[:neglength//4]
word_features = get_word_features(get_words_in_tweets(trainingtweets))


# Splitting tweets by category between training and test sets

print('Size of sets:')
print('Train: {0}'.format(len(trainingtweets)))
print('Test: {0}'.format(len(testingtweets)))
print()

# Classifier training
trainer = NaiveBayesClassifier.train
sentim_analyzer = SentimentAnalyzer()

train_set = nltk.classify.apply_features(extract_features, trainingtweets)
test_set = nltk.classify.apply_features(extract_features, testingtweets)
classifier = sentim_analyzer.train(trainer, train_set)

# Classifier validation
for key, value in sorted(sentim_analyzer.evaluate(test_set).items()):
    print('{0}: {1}'.format(key, value))

# Storing classifier and words
with open('trainer.pickle', 'wb') as f:
    pickle.dump(classifier, f)

with open('words.txt', 'w') as f:
    for word in word_features:
        f.write(word + '\n')