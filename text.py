# -*- coding: iso-8859-1 -*-

'''
Created on 13.2.2015

@author: iggymiggy
'''

import string
from time import localtime, strftime

class Text(object):
    
    def __init__(self):
        self.transformations = {}
        #Diccionario of keywords, values as answers
        self.keywords = {}
        #keys = synonyme of keyword; value = keyword
        self.syno = {}
               
    def get_transformations(self, input):
        current_line = ''
        try:
            current_line = input.readline()
            while current_line:
                current_line = current_line.strip()
                current_line = current_line.lower()
                current_line = current_line.split(":")
                if len(current_line) == 2 and current_line[0] != '' and current_line[1] != '':
                    current_line[0] = current_line[0].strip()
                    current_line[1] = current_line[1].strip()
                    self.transformations[current_line[0]] = current_line[1]
                current_line = input.readline()
        except IOError:
            print "ERROR reading file transform.txt"
        return self.transformations
    '''
    Transform the words
    '''
    def transform(self, input, transformations):
        for sana_idx in range(0, len(input)):
            lower_word = string.lower(input[sana_idx])
            
            #Special case: before "are" must be you, otherwise doesn't use transform,
            #for example: you are -  they are            
            if sana_idx >0 and lower_word == "are":
                low_word_previous = string.lower(input[sana_idx-1])                           
                if low_word_previous == "they":
                    continue
            #Special case: before you like, hate,love etc...
            #i like you --> you like me
            me_list = ["eat","see", "hear","include", "including", "like", "hate", "love", "at", "to", "tell", "told", "want", "in", "on", "about", "above",
                       "after", "against", "alongside", "amid", "of", "behind", "below", "between", "by", "for",
                       "into", "onto", "over", "under", "underneath", "with", "without"]
            if sana_idx >0 and lower_word == "you":
                low_word_previous = string.lower(input[sana_idx-1])   
                if low_word_previous in me_list:
                    input.insert(sana_idx, "me")
                    input.pop(sana_idx+1)
                    continue
            if lower_word in transformations:
                transformed = transformations[lower_word]
                #i --> I
                if transformed == "i":
                    transformed = string.upper(transformed)
                input.insert(sana_idx, transformed)
                input.pop(sana_idx+1)
        return input
    
    def transformations(self):
        return self.transformations

    def keywords(self):
        return self.keywords_one
    
    def syno(self):
        return self.syno
    
    '''
    Read keywords and save them to dictionary
    '''
    def get_keywords(self, input):
        try:
            current_lohko = ""
            current_line = input.readline()
            while current_line:
                current_line = current_line.strip()
                if len(current_line)!=0 and current_line[0] == "#":
                    current_lohko = ""
                    for kirjain in range(1, len(current_line)):
                        current_lohko = current_lohko + current_line[kirjain]
                    if not self.keywords.has_key(current_lohko):
                        self.keywords[current_lohko]= []
                    current_line = input.readline()
                    continue
                elif len(current_line) == 0:
                    current_line = input.readline()
                    continue
                elif len(current_line)!=0 and current_line[0] == "\n":
                    current_line = input.readline()
                    continue
                else:
                    if current_line not in self.keywords[current_lohko]:
                        self.keywords[current_lohko].append(current_line)
                    current_line = input.readline()
                    continue
            return self.keywords
        except IOError:
            print "ERROR reading file ai.txt"
            
    def get_synonymes(self, input):
        try:
            current_lohko = ""
            current_line = input.readline()
            #Loop until end of the file
            while current_line:
                current_line = current_line.strip()
                #If keyword
                if len(current_line)!=0 and current_line[0] == "#":
                    current_lohko = ""
                    for kirjain in range(1, len(current_line)):
                        current_lohko = current_lohko + current_line[kirjain]
                    current_line = input.readline()
                    continue
                #empty
                elif len(current_line) == 0:
                    current_line = input.readline()
                    continue
                elif len(current_line)!=0 and current_line[0] == "\n":
                    current_line = input.readline()
                    continue
                #If synonyme
                else:
                    if current_line not in self.syno:
                        self.syno[current_line] = current_lohko
                    current_line = input.readline()
                    continue
            return self.syno
        except IOError:
            print "ERROR reading file syno.txt"
            
    '''
    Write conversation to text file
    1. parameter: file to be write
    2. parameter: user input
    3. parameter: answer
    4. parameter: name of the patience
    '''
    def write_file(self, output, user_input, shrink_response):
        try:
            if output == None:
                return
            #Beginning of conversation, writing time
            elif user_input == None and shrink_response == None:
                for i in range(0, 20):
                    output.write("------")
                time = strftime("%a, %d %b %Y %H:%M:%S - Session started", localtime())
                output.write("\n\n"+time+"\n")
            #End of conversation, only the answerd to be written
            elif user_input == None:
                output.write("\nHome psychiatrist: " + shrink_response+ "\n\n\n")
                time = strftime("%a, %d %b %Y %H:%M:%S - Session ended\n", localtime())
                output.write(time)
                for i in range(0, 20):
                    output.write("------")
                output.write("\n\n")
            #Normal conversation
            else:
                output.write("\nHome psychiatrist: " + shrink_response+ "\n")
                output.write("Patience: "+user_input)
                output.write("\n")
        except IOError:
            print "Error appending file sessions.txt"
  
