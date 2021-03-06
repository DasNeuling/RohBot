import string

import spacy
from rake_nltk import Rake

nlp = spacy.load('en')


def matchUtterance(userText, sampleUtterance):
    charsToRemove = string.punctuation.replace('%', '')
    userText = ''.join(ch for ch in userText if ch not in charsToRemove)
    sampleUtterance = ''.join(ch for ch in sampleUtterance if ch not in charsToRemove)

    userText = userText.lower()
    sampleUtterance = sampleUtterance.lower()

    userWords = userText.split()
    utterWords = sampleUtterance.split()

    lenDiff = len(userWords) - len(utterWords)

    # If user input is shorter, don't match
    if (lenDiff < 0):
        return False

    for startOffset in range(lenDiff + 1):
        skip = False
        for i, matchWord in enumerate(utterWords):
            userWord = userWords[i + startOffset]
            if (matchWord != '%s' and matchWord != userWord):
                skip = True
                break
            # if i == len(utterWords) - 1:
        if not skip:
            return True
    return False


def filterKeywords(str, removeWords=string.punctuation):
    r = Rake()
    r.extract_keywords_from_text(str.decode('utf-8'))
    phrases = r.get_ranked_phrases()
    phrases = [p for p in phrases if p not in removeWords]
    return phrases


def filterKeyword(str, removeWords=string.punctuation):
    r = Rake()
    r.extract_keywords_from_text(str.decode('utf-8'))
    phrases = r.get_ranked_phrases()
    phrases = [p for p in phrases if p not in removeWords]
    if len(phrases) == 0:
        return None
    return phrases[0]


def extractEntity(sentence, entity, removeWords=[]):
    """

    :param sentence:
    :param entity: See https://spacy.io/api/annotation#named-entities for a full list of entities types.
    :param removeWords:
    :return:
    """
    doc = nlp(unicode(sentence, 'utf-8'))
    wordsToRemove = [word.lower() for word in removeWords]
    entities = [ent.text for ent in doc.ents if ent.label_ == entity and ent.text.lower() not in wordsToRemove]
    return entities


def extractEntities(sentence, entities, removeWords=[]):
    doc = nlp(unicode(sentence, 'utf-8'))
    wordsToRemove = [word.lower() for word in removeWords]
    entities = [ent.text for ent in doc.ents if ent.label_ in entities and ent.text.lower() not in removeWords]
    return entities


def extractAllEntities(sentence, removeWords=[]):
    doc = nlp(unicode(sentence, 'utf-8'))
    wordsToRemove = [word.lower() for word in removeWords]
    entities = [(ent.text, ent.label_) for ent in doc.ents if ent.text.lower() not in removeWords]
    return entities
