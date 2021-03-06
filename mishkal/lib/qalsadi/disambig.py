﻿#!/usr/bin/python
# -*- coding=utf-8 -*-

#------------------------------------------------------------------------
# Name:        dconst.py
# Purpose:     Arabic lexical analyser constants used for disambiguation
# before analysis
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-----------------------------------------------------------------------
"""
A class to remove ambiguation in text analysis 
"""

import qalsadi.disambig_const as dconst 
import naftawayh.wordtag
class Disambiguator:
    """
    A class to remove ambiguation in text analysis 
    """
    def __init__(self,):
        self.tagger = naftawayh.wordtag.WordTagger();

    def disambiguate_words(self, word_list, tag_list):
        """
        Disambiguate some word according to tag guessing to reduce cases.
        return word list with dismbiguate.
        @param word_list: the given word lists.
        @type word_list: unicode list.
        @param tag_list: the given tag lists, produced by naftawayh
        @type tag_list: unicode list.        
        @return: a new word list
        @rtype: unicode list 
        """
        # print u" ".join(word_list).encode('utf8');
        # print u" ".join(tag_list).encode('utf8');
    
        if len(word_list)==0 or len(word_list)!=len(tag_list):
            return word_list;
        else:
            newwordlist=[];
            wordtaglist=zip(word_list,tag_list);
            # print wordtaglist
            for i in range(len(wordtaglist)):
                currentword=wordtaglist[i][0]; 
                if i+1<len(wordtaglist):
                    nexttag=wordtaglist[i+1][1];
                    # if the current exists in disambig table,
                    # and the next is similar to the expected tag, 
                    # return vocalized word form
                    if self.is_ambiguous(currentword):
                        # test if expected tag is verb and 
                        if self.tagger.is_verb_tag(nexttag) and \
                        self.is_disambiguated_by_next_verb(currentword) :
                            currentword = \
                            self.get_disambiguated_by_next_verb(currentword);
                        elif self.tagger.is_noun_tag(nexttag) and \
                         self.is_disambiguated_by_next_noun(currentword):
                            currentword = \
                            self.get_disambiguated_by_next_noun(currentword);
                newwordlist.append(currentword);
            return newwordlist;

    def is_ambiguous(self, word):
        """ test if the word is an ambiguous case
        @param word: input word.
        @type word: unicode.
        @return : if word is ambiguous
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.has_key(word);

    def get_disambiguated_by_next_noun(self, word):
        """ get The disambiguated form of the word by the next word is noun.
        The disambiguated form can be fully or partially vocalized.
        @param word: input word.
        @type word: unicode.
        @return : if word is ambiguous
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.get(word, {}).get('noun', \
         {}).get('vocalized', word);


    def get_disambiguated_by_next_verb(self, word):
        """ get The disambiguated form of the word by the next word is a verb.
        The disambiguated form can be fully or partially vocalized.
        @param word: input word.
        @type word: unicode.
        @return : if word is ambiguous
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.get(word, {}).get('verb', \
        {}).get('vocalized', word);

    def is_disambiguated_by_next_noun(self, word):
        """ test if the word can be disambiguated if the next word is a noun
        @param word: input word.
        @type word: unicode.
        @return : if word has an disambiguated.
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.get(word, {}).has_key('noun');

    def is_disambiguated_by_next_verb(self, word):
        """ test if the word can be disambiguated if the next word is a verb
        @param word: input word.
        @type word: unicode.
        @return : if word has an disambiguated.
        @rtype: True/False.
        """
        return dconst.DISAMBIGUATATION_TABLE.get(word, {}).has_key('verb');


def mainly():
    """
    MAin test
    """
    text = u"أن السلام مفيد أن يركبوا"
    # tokenize the text
    wordlist = text.split(' ');
    # create the disambiguator instance
    disamb = Disambiguator();
    # tag the word list
    taglist = disamb.tagger.word_tagging(wordlist);
    newwordlist = disamb.disambiguate_words(wordlist, taglist);
    print u" ".join(newwordlist).encode('utf8'); 

if __name__ == "__main__":
    mainly()

