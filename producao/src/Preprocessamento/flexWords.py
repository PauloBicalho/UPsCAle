#################################################################
#                 generateVectorRepresentation.py               #
#################################################################

# -*- coding: utf-8 -*-
import sys
import re

TABLE  = {
    "oes":"ao",
    "agens":"agem",
    "ades":"ade",
    "entos":"ento",
    "ismos":"ismo",
    "ivos":"ivo",
    "oras":"or",
    "ora":"or",
    "ores":"or",
    "ada":"ado",
    "adas":"ado",
    "ados":"ado",
    "antes":"ante",
    "entes":"ente",
    "eis":"el",
    "ais":"al",
    "os":"o",
    "as":"a",
    "es":"e",   
    "ais":"al",  
    "nhas":"nha", 
    "nhos":"nho",
    "uns":"um" 
}
MAXLEN = 5

def flexWords(word):
    sf = sm = adj = adv = desc = subst = 0

    patterLen = len(word);
    if(patterLen > MAXLEN):
        patterLen = MAXLEN
    
    # verifica casamento com padrao maior
    while(patterLen > 0):
        if word[len(word)-patterLen:len(word)] in TABLE:
            return word[0:len(word)-patterLen] + TABLE[word[len(word)-patterLen:len(word)]]
        patterLen -= 1
    
    # nao modificou 
    return word
    
