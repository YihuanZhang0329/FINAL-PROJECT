# -*- coding: utf-8 -*-

import pickle

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0
        
    def get_total_words(self):
        return self.total_words
        
    def get_msg_size(self):
        return self.total_msgs
        
    def get_msg(self, n):
        return self.msgs[n]
        
    def add_msg(self, m):
        self.msgs.append(m)
        self.total_msgs += 1
        
    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)
    
    '''
    def indexing(self, m, l):
        words = m.split()
        self.total_words += len(words)
        for wd in words:
            self.index[wd] = self.index.get(wd, []) + [l] 
    #### Alternatively, the following also works
#        for wd in words:
#            try:
#                self.index[wd]+= [l]
#            except KeyError:
#                self.index[wd] = [l]
                                   
    def search(self, term):
        msgs = []
        if term in self.index.keys():
            indices = self.index[term]
            msgs = [(i, self.msgs[i]) for i in indices]
        return msgs
    '''

     #More Improvements:
    #This should be added below the Class Index
    def normalize(self, word):
        roman_set=set(["I.", "II.", "III.", "IV.", "V.", "VI.", "VII.", "VIII.", "IX.", "X.",
                     "XI.", "XII.", "XIII.", "XIV.", "XV.", "XVI.", "XVII.", "XVIII.", "XIX.", "XX."])
        #the roman_set can only contain limited number of roman numerals, but this code will be valid for now
        if word in roman_set:
            return word
        else:
            return word.rstrip('.,:?!\'"')
        
    def indexing(self,m,l):
        lst =m.split()
        words= set()
        for word in lst:
            words.add(self.normalize(word))
        for word in words:
            if word not in self.index:
                self.index[word]=[l]
            else:
                self.index[word].append(l)
            self.total_words+=1
        return self.total_words, self.index
    
    def search(self, term):
        phrase = [self.normalize(w) for w in term.split()]
        result = []

        for i, msg in enumerate(self.msgs):  # 正确遍历每一条消息
            words = [self.normalize(w) for w in msg.split()]
            for j in range(len(words) - len(phrase) + 1):
                if words[j:j+len(phrase)] == phrase:
                    result.append((i, msg))
                    break
        return result


class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()
        
        # load poems
    def load_poems(self):
        lines = open(self.name, 'r').readlines()
        for l in lines:
            self.add_msg_and_index(l.rstrip())
    
    def get_poem(self, p):
        p_str = self.int2roman[p] + '.'
        p_next_str = self.int2roman[p+1] + '.'
        temp = self.search(p_str)
        if temp:
            [(go_line, m)] = temp
        else:
            return []
        # in case of wrong number
        poem = []
        end = self.get_msg_size()
        while go_line < end:
            this_line = self.get_msg(go_line)
            if this_line == p_next_str:
                break
            poem.append(this_line)
            go_line += 1
        # poem = "\n".join(poem)
        return poem
    
if __name__ == "__main__":
    sonnets = PIndex("AllSonnets.txt")
    p3 = sonnets.get_poem(3)
    print(p3)
    s_love = sonnets.search("love")
    print(s_love)
