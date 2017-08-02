# -*- coding: utf-8 -*-

"""
Created: Aug 1, 2017
Author: Haozhe

This file extacts the keywords from a patient's description and prints
out the corresponding expressions stored in our dictionary

NOTE: Use Python 3.5 to run
"""

import ahocorasick
import json
import codecs

class Match:
    def __init__(self):
        self.ac = ahocorasick.Automaton()

    def load(self, fileName):
        # Create a trie that stores all symptoms
        result = []
        # Read the file in utf-8 to display Chinese characters
        inputData = codecs.open (fileName, 'r', 'utf-8')
        for line in inputData:
            currContent = json.loads(line)
            sym = currContent.get("symptoms")
            tuples = sym.items()
            for eachTuple in tuples:
                if eachTuple[0] not in result:
                    result.append(eachTuple[0])
                    self.ac.add_word(eachTuple[0], eachTuple[0])
    
    def match(self, description):
        # Process the description, removing adverbs and punctuations
        advFile = codecs.open ('Adverbs.json', 'r', 'utf-8')
        adv = json.load(advFile)
        for eachAdv in adv:
            description = description.replace(eachAdv, "")
        for punc in ["，","。","？","！", "、"," "]:
            description = description.replace(punc, "")
    
        # ac_match takes place here
        self.ac.make_automaton()
        result = []
        for end_index, symptom in self.ac.iter(description):
            result.append(symptom + " ")
        # Return a string format 
        return ''.join(str(x) for x in result)

if __name__ == '__main__':
    matcher = Match()
    matcher.load('disease_symptom.json')
    res = matcher.match(input(u'请输入症状描述: '))
    print(res)
