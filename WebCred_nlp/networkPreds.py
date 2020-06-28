import tensorflow as tf
import pickle as pkl
import requests
from dotenv import load_dotenv
import os
import json

from tensorflow.keras.preprocessing.sequence import pad_sequences

articlePath = "Articles.h5"
jobPath = "jobModel.h5"
sentimentPath = "Sentiment.h5"

articleTokenPath = "articlesTokenizer.pkl"
jobTokenPath = "jobTokenizer.pkl"
sentimentTokenPath = "sentimentTokenizer.pkl"

load_dotenv()
ReputationAPIKey = os.getenv('REP_API_TOKEN')

class prediction:
    def __init__(self):
        # load keras models from h5 and tokenizers

        self.articleModel = tf.keras.models.load_model(articlePath)
        self.articleTokenizer = pkl.load(open(articleTokenPath, 'rb'))

        self.jobModel = tf.keras.models.load_model(jobPath)
        self.jobTokenizer = pkl.load(open(jobTokenPath, 'rb'))

        self.sentimentModel = tf.keras.models.load_model(sentimentPath)
        self.sentimentTokenizer = pkl.load(open(sentimentTokenPath, 'rb'))

    def predictJob(self, jobTitle, departmentName, companyName, jobDescription, requirements):
        vocab_size = 1000
        embedding_dim = 24
        max_length = 100
        trunc_type='post'
        oov_tok='<OOV>'

        testStringSequence = self.jobTokenizer.texts_to_sequences([jobTitle + " " + departmentName + " " + companyName + " " + jobDescription + " " + requirements])
        paddedSequence = pad_sequences(testStringSequence, maxlen=max_length, truncating=trunc_type)
        prediction = self.jobModel.predict([paddedSequence])[0]
        isScam = False
        prob = 0
        if prediction[0] >= .5:
            prob = prediction[0]
        else:
            isScam = True
            prob = prediction[1]
        return (isScam, prob)

    def predictArticle(self, articleTitle):
        vocab_size = 1000
        embedding_dim = 16
        max_length = 30
        trunc_type='post'
        oov_tok='<OOV>'

        testStringSequence = self.articleTokenizer.texts_to_sequences([articleTitle])
        paddedSequence = pad_sequences(testStringSequence, maxlen=max_length, truncating=trunc_type)
        prediction = self.jobModel.predict([paddedSequence])[0]
        isFake = False
        prob = 0
        if prediction[0] >= .5:
            prob = prediction[0]
            isFake = True
        else:
            prob = prediction[1]
        return (isFake, prob)

    def predictSentiment(self, text):
        vocab_size = 10000
        embedding_dim = 16
        max_length = 140
        trunc_type='post'
        oov_tok='<OOV>'

        testStringSequence = self.sentimentTokenizer.texts_to_sequences([text])
        paddedSequence = pad_sequences(testStringSequence, maxlen=max_length, truncating=trunc_type)
        prediction = self.jobModel.predict([paddedSequence])[0]
        isPositive = True
        prob = prediction[0]
        if prediction[0] <= .5:
            isPositive = False
            prob = 1 - prediction[0]
        return (isPositive, prob)

    def domainReputation(self, url):
        rawReq = requests.get(url = "https://domain-reputation.whoisxmlapi.com/api/v1?apiKey={APIKey}&domainName={Domain}".format(APIKey = ReputationAPIKey, Domain=url))
        score = json.loads(rawReq.text).get("reputationScore")
        warnings = json.loads(rawReq.text).get("testResults")[0].get("warnings")
        return (score, warnings)


#object = prediction()
#print(object.predictArticle("America leaves Paris Climate Accords"))
