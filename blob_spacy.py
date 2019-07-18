from textblob import TextBlob
import pandas as pd, numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# import warnings
# from sklearn import metrics
import spacy
# import pickle
from tqdm import tqdm

#import spacy_simple


def spacy_model():
    nlp = spacy.load("en_vectors_web_lg")
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    return nlp


def textblob_sentencizer(text):
    blob = TextBlob(text)
    return [sent for sent in blob.sentences]


def get_target_sentence(context,target_id):
    return(context[target_id])


def spacy_sentence(text, nlp):
    return nlp(text)

def similarity(context, question):
    similarity = []
    for sent in context:
        similarity.append(sent.similarity(question))
    return similarity


def target_sentence(context, answer):
    idx = -1
    for id, c in enumerate(context):
        if answer in c.text:
            idx = id
            break
    return idx


def predict(similarity, context):
    index = similarity.index(max(similarity))
    return index, context[index]


def find_answer_sentence(context, question):
    nlp = spacy_model()
    context = textblob_sentencizer(context)
    similarity = []
    question = spacy_sentence(question, nlp)
    for c in context:
        x = spacy_sentence(c.string, nlp)
        similarity.append(x.similarity(question))
    print(similarity)
    idx, sent = predict(similarity,context)
    return idx, sent


def find_answer_sentence_train(context, question, answer, nlp):
    context = spacy_sentence(context, nlp)
    similarity = []
    question = spacy_sentence(question, nlp)
    target = -1
    sentences = [s for s in context.sents if not s.text.isspace()]
    for yy, sent in enumerate(sentences):
        similarity.append(sent.similarity(question))
        if answer in sent.text:
            target = yy
    id, sent = predict(similarity,context)
    return id, target


def main():
    # df = pd.read_pickle("/Users/mjeong/PycharmProjects/machine-comprehension/spacy-simple/initial_dataset.pkl")
    # context = df['context']
    # question = df['question']
    # answer = df['answer_text']
    # correct = 0
    # nlp = spacy_model()
    # for index in tqdm(range(len(context))):
    #     predict, target = find_answer_sentence_train(context[index], question[index], answer[index], nlp)
    #     if predict == target:
    #         correct += 1
    # print(correct/len(context))

    context = "In 1085, Guadalajara was retaken by the Christian forces of Alfonso VI ." \
              " The chronicles say that the Christian army was led by Alvar Fanez de Minaya, one of the lieutenants  of El Cid." \
              " From 1085 until the Battle of Las    Navas de Tolosa in 1212, the city suffered wars against the Almoravid and the Almohad Empires." \
              " In spite of the wars, the Christian population could definitely settle down in the area thanks to the repopulation with people from the North  who received their first fuero in 1133 from Alfonso VII." \
              "In 1219, the king Fernando III gave a new fuero to the city .During the reign of Alfonso X of Castile, the protection of the king allowed the city to develop its economy by protecting merchants and allowing markets."
    # target sentence is sentence 3
    question = "How many empires attacked Guadalajara?"
    ixx, sent = find_answer_sentence(context, question)
    print(sent)

    context = "Robotics is an interdisciplinary branch of engineering and science that includes mechanical engineering, electrical engineering, computer science, and others. " \
              "Robotics deals with the design, construction, operation, and use of robots, as well as computer systems for their control, sensory feedback, and information processing. " \
              "These technologies are used to develop machines that can substitute for humans." \
              " Robots can be used in any situation and for any purpose, but today many are used in dangerous environments (including bomb detection and de-activation), manufacturing processes, or where humans cannot survive." \
              " Robots can take on any form but some are made to resemble humans in appearance. " \
              "This is said to help in the acceptance of a robot in certain replicative behaviors usually performed by people." \
              " Such robots attempt to replicate walking, lifting, speech, cognition, and basically anything a human can do."
    # target sentence is sentence 7, but the similarity thinks the answer is sentence 5 understandably
    question = "What do robots that resemble humans attempt to do?"
    #question = "What does the physics engine allow for?"
    # question = "How many empires attacked Guadalajara?"
    ixx, sent = find_answer_sentence(context, question)
    print(sent)

    context = "Kerbal Space Program (KSP) is a space flight simulation video game developed and published by Squad for Microsoft Windows, OS X, Linux, PlayStation 4, Xbox One, with a Wii U version that was supposed to be released at a later date." \
              " The developers have stated that the gaming landscape has changed since that announcement and more details will be released soon." \
              " In the game, players direct a nascent space program, staffed and crewed by humanoid aliens known as \"Kerbals\"." \
              " The game features a realistic orbital physics engine, allowing for various real-life orbital maneuvers such as Hohmann transfer orbits and bi-elliptic transfer orbits."
    # target sentence is sentence 4
    question = "What does the physics engine allow for?"
    ixx, sent = find_answer_sentence(context, question)
    print(sent)


if __name__ == '__main__':
    main()

