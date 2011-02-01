'''
File: Week03Assignment-noKeys.py
last revised: 31 January 2011
author: Melissa Rice (UWNetID: mlrice)
warning: You will need your own API keys to run this... 
         Please apply for an API key at http://thesaurus.altervista.org/mykey for the thesaurus API
         or use the key 'test_only' in which case 'peace' is the only word you can get synonyms for.
         Please apply for an API key at https://code.google.com/apis/console/#welcome for google translate.

purpose: Mashup assignment: write an application which accesses information
         from two web APIs and combines the data. This script uses a thesaurus
         API to get word synonyms for a selected word and then uses the google
         translate API to translate these to another language and back to the
         original language. Words that translate back to the originally selected
         word are reported as translations of that word, while other words are
         reported separately. The target language may be anything supported by
         google translate. The source language must be supported both by google
         translate and the altervista thesaurus site.
'''

import sys
import urllib, urllib2
import json


class TranslationToolClass(object):
    '''TranslationToolClass creates an object which assists with translating words by providing
    translations of the original word, from the source language to the target language, as well
    as translations of synonyms of the original word to assist with the selection of a translation
    with the closest desired meaning.
    
    constructor: translator = TranslationToolClass(sourceLanguage='en',targetLanguage='es')
    getting synonyms: synonymList = GetSynonyms(word,language)
                      if no language is given the sourceLanguage for the translator is used.
    translating just one word: translation = GetOneTranslation(word,languagePair)
    translating word and synonyms: translation = translator.GetTranslations(word)
    '''
    thesaurusBaseURL = 'http://thesaurus.altervista.org/thesaurus'
    thesaurusAPIkey = None
    googleTranslateBaseURL = 'https://ajax.googleapis.com/ajax/services/language/translate?'
    googleAPIkey = None
    
    def __init__(self,sourceLanguage='en',targetLanguage='es'):
        if sourceLanguage == 'en':
            self.thesaurusLanguage = 'en_US'
        else:
            self.thesaurusLanguage = sourceLanguage
        self.sourceLanguage = sourceLanguage
        self.targetLanguage = targetLanguage
        self.forwardLanguagePair = "%s|%s" % (sourceLanguage,targetLanguage)
        self.backwardLanguagePair = "%s|%s" % (targetLanguage,sourceLanguage)
        if TranslationToolClass.thesaurusAPIkey == None:
            print "Please apply for an API key at http://thesaurus.altervista.org/mykey"
            print "or use the key 'test_only' in which case 'peace' is the only word you can get synonyms for."
            sys.exit(1)
        if TranslationToolClass.googleAPIkey == None:
            print "Please apply for an API key at https://code.google.com/apis/console/#welcome"
            sys.exit(1)
        
    def GetSynonyms(self,word,language=None):
        if language == None:
            language = self.thesaurusLanguage
        allSynonyms = [word]            
        baseURL = TranslationToolClass.thesaurusBaseURL
        version = "v1"
        key = TranslationToolClass.thesaurusAPIkey
        output = "json"
        URL = "%s/%s?word=%s&language=%s&key=%s&output=%s " % (baseURL,version,word,language,key,output) 
        try:
            result = json.load(urllib2.urlopen(URL))
        except Exception, err:
            print "Error getting synonyms from thesaurus.altervista.org: ", err 
            print "Proceeding with just the original word."
            return allSynonyms
        try:
            responseList = result['response']
        except Exception, err:
            print "Error parsing the json response from thesaurus.altervista.org: ", err
            print "Proceeding with just the original word."
            return allSynonyms
        for synonymGroup in responseList:
            synonyms = synonymGroup['list']['synonyms'].split("|")
            for synonym in synonyms:
                synonym = synonym.lower()
                if synonym != None and "antonym" not in synonym:
                    allSynonyms.append(synonym)
        print "Found %s synonyms for %s: %s" % (len(allSynonyms),word,repr(allSynonyms))
        return allSynonyms
    
    def GetOneTranslation(self,word,languagePair):
            urlDetails = urllib.urlencode({
                'v':1.0,
                'ie': 'UTF8', 
                'q': word.encode('utf-8'),
                'langpair':languagePair})
            translateURL = TranslationToolClass.googleTranslateBaseURL + urlDetails
            try:
                response = urllib2.urlopen(translateURL)
            except Exception, err:
                print "Error getting a translation from google translate: ", err
                print "Skipping this word."
                return None
            try:
                result = json.loads(response.read())
            except Exception, err:
                print "Error getting json response from google translate: ", err
                print "Skipping this word."
                return None
            try:
                translation = result['responseData']['translatedText']
            except Exception, err:
                print "Error parsing json response from google translate: ", err
                print "Skipping this word."
                return None
            return translation
        
    def GetTranslations(self,originalWord):
        wordList = self.GetSynonyms(originalWord) 
        translationList = []
        synonymDict = {}
        print "Checking translations for %s:" % originalWord
        for word in wordList:
            translation = self.GetOneTranslation(word,self.forwardLanguagePair)
            if translation == None:
                continue                
            backTranslation = self.GetOneTranslation(word,self.backwardLanguagePair)
            if backTranslation == None:
                continue
            backTranslation = backTranslation.lower()
            print "    %s ===> %s ===> %s" % (word,translation,backTranslation)
            if backTranslation == originalWord:
                translationList.append(translation)
            else:
                synonymDict[backTranslation] = translation
        print "========================================================="
        print "Best Translations for %s:" % originalWord
        for word in translationList:
            print "    ", word
        print "========================================================="
        print "Translations for Similar Meanings:"
        for (word,translation) in synonymDict.items():
            print "    %s   [%s]" % (translation,word)
        return (translationList,synonymDict)
                
        
if __name__ == '__main__':
    word = u'peace'
    translator = TranslationToolClass(sourceLanguage='en',targetLanguage='es')
    translation = translator.GetTranslations(word)
    
    
        