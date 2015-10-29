'''
Created on 13.2.2015

@author: iggymiggy
'''
import sys
from user import User
from text import Text
from random import choice
import string

MEMORY_LENGTH = 40

class Shrink(object):
    
    def __init__(self):
        
        self.answer = ""
        self.name = ""
        self.dunno = []
        self.responses = []
        self.idx_dunno = 0
        self.begin_bool = False
        self.useful_part_string = ""
        self.keyword_string = ""
        self.response_from_list = ""
        self.first_list = ['Hello dear! Tell me your name, please.', 'Welcome! What is your name?', 
                  "Finally you arrived! And you're name is?", "Hi! I don't remember you. Please tell me your name.",
                  "Hello! Tell me your name, please.", "Hello! What is your name?"]
        self.user_end_list = ['Good bye', 'good bye','Goodbye' , 'Bye Bye', 'goodbye', 'bye bye', 'byebye', 'bye', 'Bye bye', 'Good night', 
                     'good night']
    
    def get_response_from_list(self):
        return self.response_from_list
    
    def add_name(self, name):
        self.name = name
        
    def get_name(self):
        return self.name
    
    def get_useful_part(self):
        return self.useful_part_string
    
    def get_keyword(self):
        return self.keyword_string
        
    def get_response(self):
        return self.answer
    
    '''
    Find a keyword from the input.
    1. parameter is a input as an array
    2. paramater is a keywords as an dictionary
    3. paramater es sinonymes as an dictionary
    4. parameter es original input as a string
    Return array, which first element is a beginning index of keyword, 
    second element is a ending element of keyword and third element is a keyword
    '''
    def find_keyword(self, input, keywords, syno, original_input):
    
        idx_array = []
        #Find keywords longer than one single word
        for key in keywords:
            key_lower = string.lower(key)
            key_array = key.split()
            if len(key_array) >1:
                original_input_lower = string.lower(original_input)
                keyword_idx = original_input_lower.find(key_lower)
                if keyword_idx !=-1:
                    #Find indices of keyword
                    break_loop = False
                    for sana in range(0, len(input)):
                        if break_loop:
                            break
                        lower_sana = string.lower(input[sana])
                        if lower_sana == key_array[0]:
                            whole_key = True
                            for word_in_key in range(1, len(key_array)):
                                input_word = string.lower(input[sana+word_in_key])
                                if key_array[word_in_key] != input_word:
                                    whole_key = False
                                    break_loop = True
                            if whole_key:
                                idx_array.append(sana)
                                idx_array.append(len(key_array)+sana-1)
                                idx_array.append(key)
                                self.keyword_string = idx_array[2]
                                return idx_array
        #Find synonymes longer than one word
        for synonyme in syno:
            synonyme_lower = string.lower(synonyme)
            synonyme_array = synonyme.split()
            if len(synonyme_array) >1:
                original_input_lower = string.lower(original_input)
                synonyme_idx = original_input_lower.find(synonyme_lower)
                if synonyme_idx !=-1:
                    #Find indices of synonyme
                    break_loop = False
                    for sana in range(0, len(input)):
                        if break_loop:
                            break
                        lower_sana = string.lower(input[sana])
                        if lower_sana == synonyme_array[0]:
                            whole_synonyme = True
                            for word_in_synonyme in range(1, len(key_array)):
                                input_word = string.lower(input[sana+word_in_synonyme])
                                if synonyme_array[word_in_synonyme] != input_word:
                                    whole_synonyme = False
                                    break_loop = True
                            if whole_synonyme:
                                idx_array.append(sana)
                                idx_array.append(len(synonyme_array)+sana-1)
                                idx_array.append(syno[synonyme])
                                self.keyword_string = synonyme
                                return idx_array
        
        #Find one-word length keyword
        for word in range(0,len(input)):
            if string.lower(input[word]) in keywords:
                if string.lower(input[word]) == "what":
                    if word ==0:
                        idx_array.append(word)
                        idx_array.append(word)
                        idx_array.append(input[word])
                else:
                    idx_array.append(word)
                    idx_array.append(word)
                    idx_array.append(input[word])
                    self.keyword_string = idx_array[2]
                    return idx_array
            if string.lower(input[word]) in syno and syno[string.lower(input[word])] in keywords:
                if string.lower(input[word]) in syno and syno[string.lower(input[word])] == "what" and word !=0:
                    continue             
                idx_array.append(word)
                idx_array.append(word)
                idx_array.append(syno[string.lower(input[word])])
                self.keyword_string = input[word]
                return idx_array
        self.keyword_string = ""
        return idx_array
       
    '''
    Return useful part to be connected to answers
    1. parameter input as a string
    2. keyword list
    3. dictionary of transformation words
    '''
    def useful_part(self, input, keys_array, transformations):
        self.useful_part_string = ""
        useful_part = []
        if keys_array == []:
            useful_part =""
            return useful_part
        else:
            for sana in range(keys_array[0], len(input)):
                if input[sana] != "##cut##":
                    useful_part.append(input[sana])
                    self.useful_part_string = self.useful_part_string+ " " + input[sana]
                else:
                    break
        #transformation:
        self.useful_part_string = self.useful_part_string.strip()
        useful_part = Text().transform(useful_part, transformations)
        useful_part_string = ""
        for sana in range(0, len(useful_part)):
            if useful_part[sana][0] in string.punctuation:
                useful_part_string = useful_part_string.strip()
            useful_part_string = useful_part_string + useful_part[sana] + " "
        useful_part_string = useful_part_string.strip()
        return useful_part_string
    
    '''
    Save useful parts to memory to be used later
    '''
    def memory(self, useful_part, keywords, transformations, syno, input, keys_array, original_input):
        #If useful part is longer than two words
        if useful_part != "" and useful_part != [] and len(useful_part.split())>2:
            #Remove "that" if it is a keyword, to avoid "that that" in answer
            if keys_array[2] == "that":
                useful_part2 = ""
                for letter in range(5, len(useful_part)):
                    useful_part2 = useful_part2 +useful_part[letter]
                useful_part = useful_part2
            useful_part_found = False
            #Check if already exists useful part
            for part in range(0,len(self.dunno)):
                if len(self.dunno) >0 and self.dunno[part].find(useful_part) != -1:
                    useful_part_found = True
                    break
            #Add new useful part if it doesn't exist already 
            if useful_part_found == False:
                if keys_array[2] != "what":
                    #List of answers incluiding useful part
                    memory_list = [self.get_name()+ ", you mentioned earlier that " + useful_part + ". Do you have something else to add?", 
                                   "Earlier in our conversation you said that " + useful_part+ ". Tell me more.",
                                   self.get_name()+ ", when you said that "+ useful_part+ ". Did you really mean that?",
                                   "You told me that "+ useful_part+ ". " + self.get_name()+ ", were you serious?",
                                   "Did you mean it, when you said that "+ useful_part+"?",
                                   "Earlier you said that "+ useful_part + ". Are you sure? I wouldn't say that "+ useful_part+ ".",
                                   "A while back you said that " + useful_part+ ". What do you think I think of that?",
                                   "A while back you said that " + useful_part+". Tell me more "+ self.get_name() +".",
                                   "Does that have anything to do with the fact that "+useful_part+"?"]
                else:
                    memory_list = ["You asked " + useful_part + ". What did you really want to know?",
                                   "You recently asked me "+ useful_part + ". Do you still want to know?"]
                response = choice(memory_list)
                self.dunno.append(response)
            
            #Find place to cut input and add ##cut##
            cut = -1
            for word in range(keys_array[1]+1, len(input)):
                cut = word
                if input[word] == "##cut##":
                    break
                cut = word
            #Find if there still is something interesting in the input after first
            #useful part founded
            if cut !=-1 and len(input) > cut+1:
                input2= []
                for word in range(cut+1, len(input)):
                    input2.append(input[word])
                keys_array2 = self.find_keyword(input2, keywords, syno, original_input)
                useful_part2 = self.useful_part(input2, keys_array2, transformations)
                self.memory(useful_part2, keywords, transformations, syno, input2, keys_array2, original_input)
                    
 
    '''
    Check if the answer has been used lately
    '''
    def check_response(self, response, response_list):
        response_tmp = response
        while len(self.responses) > MEMORY_LENGTH:
            self.responses.pop()
        if response in self.responses:
            response_idx = self.responses.index(response)
            number = 0
            while number<len(response_list):
                #next response on the list
                next_idx = (response_idx +1)% len(response_list)
                #choose the next one if it's not already used
                if response_list[next_idx] not in self.responses:
                    return response_list[next_idx]
                number = number+1
                response_idx= response_idx +1
            
            #If all the responses are already used, choose the next one on the 
            #list if it's different than last one
            if len(response_list)>0:
                response_idx = response_list.index(response_tmp)
                next_idx = (response_idx +1)% len(response_list)
                if self.responses[0] != response_list[next_idx]:
                    response = response_list[next_idx]
        return response
    
    '''
    Check if the conversation ends 
    '''
    def is_over(self, original_input):
        
        if (original_input in self.user_end_list) and self.begin_bool == True :
            return True
        else:
            return False
    '''
    Form the response of psychiatrist
    1.parameter = user input from method user_read
    2.parameter = keywords
    3.paramater = transformaations 
    4.parameter = synonymes
    5.parameter = original user input
    '''
    def response(self, input, keywords, transformations, syno, original_input):
        response_list = []
        response = ""
        
        #Beginning: ask the name of client
        if input == None and original_input=="":
            response = choice(self.first_list)
            self.answer = response
            self.begin_bool = False
            self.response_from_list = response
            self.keyword_string = "'PRE-DEFINED': asking name"
            return response
        
        #Look for the keyword
        keys_array = self.find_keyword(input, keywords, syno, original_input)
        if len(keys_array) >0 and keys_array[2] == "what" and input[keys_array[0]] == "what":
            self.keyword_string = "what"
        useful_part = self.useful_part(input, keys_array, transformations)
        self.memory(useful_part, keywords, transformations, syno, input, keys_array, original_input)
      
        #Question
        if User().is_question(original_input) and '##asking##' in keywords:
            if (len(keys_array)>0 and keys_array[2] != "what") or len(keys_array) == 0:
                response1 = choice(keywords['##asking##'])
                response = self.check_response(response1, keywords['##asking##'])
                self.response_from_list = response
                self.responses.insert(0,response)
                self.keyword_string = "?"
                self.answer = response
                return response

        #End of conversation
        if self.is_over(original_input) and self.get_response():
            end_list = ["See you " + self.get_name() +"!", "Bye bye " + self.get_name() +"!", 
                "Take care " + self.get_name() +"!", "Have a nice day " + self.get_name()+ "!",
                "Thank you "+ self.get_name()+ "!" + " That would be 150e. Have a good day!"]
            response = choice(end_list)
            self.answer = response
            self.response_from_list = response
            self.keyword_string = original_input
            self.useful_part_string = ""
            return response
            
        #First reaction after telling the name
        elif self.begin_bool == False:
            self.begin_bool = True
            start_list = ["Well " + self.get_name() + ", what would you like to talk about?", 
                  "Okey " + self.get_name() + ", why are you here?"]
            response=choice(start_list)
            self.response_from_list = response
            self.keyword_string = "'PRE-DEFINED': begining conversation"
            
        #Yelling
        elif User().is_yelling(original_input) and '##yelling##' in keywords:
            response1 = choice(keywords['##yelling##'])
            response = self.check_response(response1, keywords['##yelling##'])
            self.response_from_list = response
            self.responses.insert(0,response)
            self.keyword_string = "!"
            
        #Question mark
        elif User().is_question(original_input) and len(keys_array)>0 and keys_array[2] != "what" and '##asking##' in keywords:
            response1 = choice(keywords['##asking##'])
            response = self.check_response(response1, keywords['##asking##'])
            self.response_from_list = response
            self.responses.insert(0,response)
            self.keyword_string = "?"
            
        #Empty
        elif original_input =="" and '##empty##'in keywords:
            response1 = choice(keywords['##empty##'])
            response = self.check_response(response1, keywords['##empty##'])
            self.response_from_list = response
            self.responses.insert(0,response)
            self.keyword_string = "'EMPTY STRING'"
        
        #Normal answer    
        else:
            #Keyword
            if len(keys_array) > 0:
                keyword= keys_array[2]
                keyword = keyword.strip()
                keyword = string.lower(keyword)
                if keyword in keywords:
                    response_list = keywords[keyword]
                if len(response_list)>0:
                    response1 = choice(response_list)
                    response = self.check_response(response1, response_list)
                else:
                    if 'dunno' in keywords:
                        response1 = choice(keywords['dunno'])
                        response = self.check_response(response1, keywords['dunno'])
                        self.keyword_string = "Keyword found, but zero responses. Response taken from 'dunno'."
                    useful_part = original_input    
            #No keyword found
            else:
                #Responses in memory
                if len(self.dunno) >0 and (self.idx_dunno % 2) == 0:
                    response = choice(self.dunno)
                    self.dunno.remove(response)
                    self.keyword_string = "Keyword not found, response taken from memory."   
                #No responses ready in memory
                else:
                    if 'dunno' in keywords:
                        response1 = choice(keywords['dunno'])
                        response = self.check_response(response1, keywords['dunno'])
                        self.keyword_string = "Keyword not found, response taken from 'dunno'."
                    else:
                        response = "I dunno."
                        self.keyword_string = "Keyword not found, 'dunno' not found. "
                useful_part = original_input
                self.idx_dunno = self.idx_dunno +1
            self.response_from_list = response
            
            #If response has been found
            if response != "":
                self.responses.insert(0,response)
                star_idx = response.find('*')
                response_string = ""
                if star_idx != -1:
                    for kirjain in range(0,len(response)):
                        if response[kirjain] == "*":
                            response_string = response_string + " " + response[kirjain] + " "
                        else:
                            response_string = response_string + response[kirjain]
                    response_string = response_string.split()
                    for sana in range(0,len(response_string)):
                        if response_string[sana] == '*':
                            if sana >1 and response_string[sana-1][len(response_string[sana-1])-1] == '"':
                                previous_part = response_string[sana-1]
                                previous_array = []
                                for letter in range(0,len(previous_part)):
                                    previous_array.append(previous_part[letter])
                                previous_array.insert(len(previous_array)-1, " ")
                                previous_part = ""
                                for letter in range(0, len(previous_array)):
                                    previous_part = previous_part + previous_array[letter]
                                response_string.pop(sana-1)
                                response_string.insert(sana-1, previous_part)
                            response_string.pop(sana)
                            response_string.insert(sana, useful_part)
                            break
                    response = ""
                    for sana in range(0, len(response_string)):
                        #Remove space before signs
                        if response_string[sana][0] in string.punctuation:
                            response = response.strip()
                        if response_string[sana].find('"') != -1:
                            response = response+ response_string[sana]
                        else:
                            response = response+ response_string[sana] + " "
                    response = response.strip()
            #If response has not been found,i.e. memory is damaged or empty file or file missing. ai.txt
            else:
                response_list = ["My memory is corrupted. File ai.txt needs to be fixed. Please contact technical support.\n"+
                                 "Shut me down by typing bye.",
                                 "My ai.txt is corrupted. Please contact technical support.\n" +
                                 "Shut me down by typing bye.",
                                 "My brain is broken. Will you fix it? Do something to ai.txt file.\n"+
                                 "Shut me down by typing bye."]
                response = choice(response_list)
                self.response_from_list = response
        self.answer = response
        return response   

def main(self, argv):
    
    try:
        
        if len(argv) > 2:
            sys.exit("Two many arguments.\n\nFirst argument is shrink.py\n\nSecond argument is optional file name if "+
                     "you want to save your conversation to a text file. For example file.txt\n")    
        shrink= Shrink()
        text = Text()
        user = User()
        ai = open('ai.txt', 'r')
        keywords = text.get_keywords(ai)
        transform_text = open('transform.txt', 'r')
        transformations = text.get_transformations(transform_text)
        synonymes = open('syno.txt', 'r')
        syno = text.get_synonymes(synonymes)
        ai.close()
        transform_text.close()
        synonymes.close()
        if len(argv) == 2:  
            test_file = open(argv[1], 'a')
        else:
            test_file = None
        text.write_file(test_file, None, None)
        first  = shrink.response(None, keywords, transformations, syno, "")
        name = raw_input(first+"\n")
        shrink.add_name(name)
        name_array = user.read(name)
        text.write_file(test_file, name, shrink.get_response())
        second = shrink.response(name_array, keywords, transformations, syno, name)
        print
        input = raw_input(second+"\n")
        text.write_file(test_file, input, shrink.get_response())
        while 1:
            if shrink.is_over(input) == True:
                input1 = user.read(input)
                shrink.response(input1, keywords, transformations, syno, user.get_input())
                print
                print shrink.get_response()
                text.write_file(test_file, None, shrink.get_response())
                break
            user.original_input(input)
            input1 = user.read(input)
            print
            shrink.response(input1, keywords, transformations, syno, user.get_input())
            print shrink.get_response()
            input = raw_input()
            text.write_file(test_file, input, shrink.get_response())
        test_file.close()
    except not SystemExit:
        print "Unexpected error:", sys.exc_info()[0]
        raise   
