import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


f = open('chatbot.txt','r',errors = 'ignore')

raw = f.read()
raw = raw.lower()

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw)       #converts to a list of sentences
word_tokens = nltk.word_tokenize(raw)       #converts to a list of words

print(sent_tokens[:2])

lemmer = nltk.stem.WordNetLemmatizer() #wordnet is a semantically-oriented English dict in NLTK

#Pre-processing raw data

def lem_tokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens] 
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def lem_normalize(text):
    return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

#Keyword matching

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey", "how you doing?")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

#Generating a response


def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=lem_normalize)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf == 0):
        robo_response = robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag = True
print("ROBO: My name is Robo. I will answer your queries about anything. If you want to exit, type Bye!")
while(flag == True):
    user_response = input()
    user_response = user_response.lower()
    if(user_response != 'bye'):
        if(user_response == 'thanks' or user_response == 'thank you'):
            flag = False
            print("ROBO: You are welcome..")
        else:
            if(greeting(user_response) != None):
                print("ROBO: "+greeting(user_response))
            else:
                print("ROBO: ", end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag = False
        print("ROBO: Bye! take care..")
