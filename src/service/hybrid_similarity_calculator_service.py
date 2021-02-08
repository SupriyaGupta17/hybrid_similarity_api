"""
    hybrid_similarity_calculator_service.py
    ~~~~~~
    Created By : Pankaj Suthar
"""

import math
import re
from collections import Counter

import nltk
import scipy
from inoutlogger.decorators import in_out_log
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from resourceprovider import ResourceProvider

from src.exception.application_exception import ApplicationException


class HybridSimilarityCalculatorService:
    """Hybrid Similarity Calculator Service"""

    def __init__(self):
        self.WORD = re.compile(r"\w+")

    @in_out_log()
    def calculate_similarity(self, f_sentence, s_sentence, option) -> float:
        """
        Calculate Similarity Score
        :param f_sentence: first sentence
        :param s_sentence: second sentence
        :param option: option which similarity algorithm to use
        :return: float
        """
        logger = ResourceProvider.get_resource("logger")

        sentence1 = self.preprocess_sentence(f_sentence)
        sentence2 = self.preprocess_sentence(s_sentence)
        if option == "bert":
            similarity = self.sementic_bert(sentence1, sentence2)
        elif option == "cos":
            similarity = self.cosine_similarity(sentence1, sentence2)
        elif option == "jac":
            similarity = self.jaccard_similarity(sentence1, sentence2)
        elif option == "lev":
            similarity = self.levenshteinDistance(sentence1, sentence2)
        elif option == "h1":
            similarity = self.hybrid1(sentence1, sentence2)
        elif option == "h2":
            similarity = self.hybrid2(sentence1, sentence2)
        else:
            logger.exception("Invalid [Option], selected [{}]".format(option))
            raise ApplicationException("Invalid [option]. Please select bert,cos,jac or lev", 400)
        logger.info(
            "Similarity Score for sentence \n Sentence 1 - [{}] and \n Sentence 2 - [{}] for \n Option -  [{}] is \n "
            "Score - [{}]".format(
                f_sentence,
                s_sentence, option, str(
                    similarity)))
        return similarity

    @in_out_log()
    def preprocess_sentence(self, text):
        """
        Pre Process Sentence
        :param text: Input Text
        :return: Formatted Text
        """
        # Remove Stop Words
        tokens = word_tokenize(text)
        tokens_without_sw = [word.lower() for word in tokens if not word in stopwords.words()]

        # Lemetize
        tokens_lemetize = [nltk.stem.WordNetLemmatizer().lemmatize(word) for word in tokens_without_sw]

        # Join Sentence
        filtered_sentence = (" ").join(tokens_lemetize)
        return filtered_sentence

    @in_out_log()
    def sementic_bert(self, sentence1, sentence2):
        model = ResourceProvider.get_resource("model")
        sentence1_embeddings = model.encode(sentence1)
        sentence2_embeddings = model.encode(sentence2)
        distances = scipy.spatial.distance.cdist([sentence1_embeddings], [sentence2_embeddings], "cosine")[0]
        return 1 - distances[0]

    # Cosine Similarity
    @in_out_log()
    def cosine_similarity(self, sentence1, sentence2):

        def get_cosine(vec1, vec2):
            intersection = set(vec1.keys()) & set(vec2.keys())
            numerator = sum([vec1[x] * vec2[x] for x in intersection])

            sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
            sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
            denominator = math.sqrt(sum1) * math.sqrt(sum2)

            if not denominator:
                return 0.0
            else:
                return float(numerator) / denominator

        def text_to_vector(text):
            words = self.WORD.findall(text)
            return Counter(words)

        vector1 = text_to_vector(sentence1)
        vector2 = text_to_vector(sentence2)

        cosine = get_cosine(vector1, vector2)
        return cosine

    # Jaccard Similarity
    @in_out_log()
    def jaccard_similarity(self, sentence1, sentence2):

        list1 = sentence1.split()
        list2 = sentence2.split()

        intersection = len(list(set(list1).intersection(list2)))
        union = (len(list1) + len(list2)) - intersection
        if union == 0:
            return 0
        else:
            return float(intersection) / union

    # Levenshtien Distance
    @in_out_log()
    def levenshteinDistance(self, s1, s2):

        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2 + 1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        dist = distances[-1]
        l = max(len(s1), len(s2))
        if l == 0:
            return 0
        else:
            return float(l - dist) / float(l)

    @in_out_log()
    def hybrid1(self, s1, s2):

        bert = self.sementic_bert(s1, s2)
        cos = self.cosine_similarity(s1, s2)

        return float((3 * bert + cos) / 4)

    @in_out_log()
    def hybrid2(self, s1, s2):

        bert = self.sementic_bert(s1, s2)
        cos = self.cosine_similarity(s1, s2)
        jac = self.jaccard_similarity(s1, s2)
        lev = self.levenshteinDistance(s1, s2)

        return float((3 * bert + cos + jac + lev) / 7)
