# twitter-sentiment-analysis
Sentiment Analysis implementation for Twitter using Python NLTK library

The scripts are to be run using Python 3.6.

In order for the Python scripts to work, the following packages must be installed:

NLTK

pprint

unidecode

This packages can be installed with the help of pip, included in Python.

The names of both corpus files can be edited in

Be aware that if you only have a single file for the corpus it must follow the following format:

P|I love eating at Burger King!

N|I dont like Burger King at all...

(P for positive, N for negative, one line per tweet).

If it follows this format, check splitcorpus.py and run it with the according file names, 
the final accepted format for the corpus is one file for all the positive tweets, 
one per line, and one file for all negative tweets, also one per line.

MongoDB was used for the storage of the corpus so it can be easily expanded by adding new documents (tweets)
to it. If you also wish to use MongoDB, simply create a new database and create two new collections in it, one 
for positive and one for negative tweets, you can also create a single collection with tweets in the format shown above and 
when you download the collections to execute the trainer run splitcorpus.py first.
