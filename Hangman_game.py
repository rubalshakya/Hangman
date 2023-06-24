from images import hangman_images
import random
import re
from english_words import get_english_words_set

class Hangman:
    def __init__(self):
        # self.dictionary_file_path = dictionary_file_path
        self.attempted_letter = []
        self.failed_letters = []
    
            
    def load_dict(self):
        self.dictionary = list(get_english_words_set(['web2'], lower=True))
        
    ##################################################################################################################
    ###################################         For Player           #################################################
    ##################################################################################################################
                         
    def Initial_Display_word(self):
        self.hidden_indexes = random.sample(range(self.word_length),self.word_length//2)
        self.hidden_letters = "".join([self.secret_word[i] for i in self.hidden_indexes])
        
        displayed_index = [i for i in range(self.word_length) if i not in self.hidden_indexes]
        self.displayed_letters = "".join([self.secret_word[i] for i in displayed_index])
        
        
        word_in_list = list(self.secret_word)
        for i in self.hidden_indexes:
            word_in_list[i]="_"
        self.word_to_display = "".join(word_in_list)
        self.Display_word()
        
        
    def Display_word(self):
        # print("-"*80)
        # print("Word: ",self.word_to_display)
        # print(f"attempts Remaining: {self.attempts}")
        # print(hangman_images[7-self.attempts])
        
        return {"Remaining_attempts":self.attempts,"image":hangman_images[11-self.attempts],"game_status":"on","secret_word":self.secret_word,"display_word":" ".join(list(self.word_to_display))}

        
    def play(self):
        self.load_dict()
        self.attempts = 7
        self.secret_word = random.choice(self.dictionary)
        self.word_length = len(self.secret_word)
        self.Initial_Display_word()
        return {"Remaining_attempts":self.attempts,"image":hangman_images[7-self.attempts],"game_status":"on","secret_word":self.secret_word,"display_word":" ".join(list(self.word_to_display))}
        
    def guess_letter(self,guessed_letter):
        if guessed_letter in self.hidden_letters:
            index = self.hidden_letters.index(guessed_letter)
            index_to_be_replaced = self.hidden_indexes[index]
            self.word_to_display = self.word_to_display[:index_to_be_replaced]+guessed_letter+self.word_to_display[index_to_be_replaced+1:]
  
            li_word = list(self.hidden_letters)
            del li_word[index]
            self.hidden_letters = "".join(li_word)
            del self.hidden_indexes[index]
            # print()
            
            if self.hidden_letters:
                return {"image":hangman_images[7-self.attempts],"Remaining_attempts":self.attempts,"game_status":"on","secret_word":self.secret_word,"display_word":" ".join(list(self.word_to_display))}
                
            else:
                return {"image":hangman_images[7-self.attempts],"Remaining_attempts":self.attempts,"game_status":"win","secret_word":self.secret_word,"display_word":" ".join(list(self.word_to_display))}
                # print(f"Hurray! You have guessed the word: {self.secret_word}")

        else:
            # print()
            self.attempts -=1
            if self.attempts>0:
                return {"image":hangman_images[7-self.attempts],"Remaining_attempts":self.attempts,"game_status": "on","secret_word":self.secret_word,"display_word":" ".join(list(self.word_to_display))}
            else:
                return {"image":hangman_images[7-self.attempts],"Remaining_attempts":self.attempts,"game_status":"lose","secret_word":self.secret_word,"display_word":" ".join(list(self.word_to_display))}
                # print(hangman_images[7-self.attempts])
                # print("#"*80)
                # print(f"You lost! The word was: {self.secret_word}")
                # print("#"*80)
                
    ##################################################################################################################
    ###################################         For Computer         #################################################
    ##################################################################################################################

    def play_comp(self):
        self.load_dict()
        self.attempts = 7
        self.secret_word = random.choice(self.dictionary)
        self.word_length = len(self.secret_word)
        self.Initial_Display_word_comp()


    def Initial_Display_word_comp(self):
        self.hidden_indexes = random.sample(range(self.word_length), 1 + self.word_length // 2)
        self.hidden_letters = "".join(self.secret_word[i] for i in self.hidden_indexes)
        self.word_to_display = "".join("_" if i in self.hidden_indexes else char for i, char in enumerate(self.secret_word))
        self.Display_word_comp()

  
    def Display_word_comp(self):
        print("-"*80)
        print("Word: "," ".join(list(self.word_to_display)))
        print(f"Attempts Remaining: {self.attempts}")
        print(hangman_images[7-self.attempts])
        
        self.word_dict = self.get_filter_dict(self.word_to_display)
        self.guess_letter_comp(self.possible_letter())
        
    def get_filter_dict(self,secret_word):
#         clean_word
        word = secret_word.replace("_",".")

#         Filter by length
        self.word_dict = [word_ for word_ in self.dictionary if len(word_)==self.word_length]

#         filter by RE module
        new_dict=[]
        for word_ in self.word_dict:
            matched_word = re.match(word,word_)
            if matched_word:
                new_dict.append(word_)
        self.word_dict = new_dict
        return self.word_dict


    def possible_letter(self):
#        return percentage of words in 'dictionary' that contain the value of Alpha:
        def get_percent_alpha(Alpha):
            percentage = len([word for word in self.word_dict if Alpha in word])/len(self.word_dict)*100
            return percentage
        
#        To get list of unique alphabets from dictionary:
        dict_string = "".join(self.word_dict)
        list_alphabets = []
        for alpha in dict_string:
            if alpha not in list_alphabets:
                list_alphabets.append(alpha)
#        calculate percentage of each alphabet present in dictionary :
        Percentage_words_contains_alpha = {}
        for alpha in list_alphabets:
            Percentage_words_contains_alpha[alpha]= get_percent_alpha(alpha)

#        sort dictionary in Descending order of percentage:
        Percentage_words_contains_alpha = dict(sorted(Percentage_words_contains_alpha.items(),key=lambda x: x[1],reverse=True)) 
        self.list_of_possible_letters_1 = [word for word in Percentage_words_contains_alpha.keys()]
        
        self.list_of_possible_letters_2 = []
        for index_ in self.hidden_indexes:
            for word_ in self.word_dict:
                if word_[index_] not in self.list_of_possible_letters_2:
                    self.list_of_possible_letters_2.append(word_[index_])

        self.final_possible_letters = [i for i in self.list_of_possible_letters_1 if i in self.list_of_possible_letters_2]

        for i in self.final_possible_letters:
            if i not in self.failed_letters:
                self.letter_to_attempt = i
                break
        self.attempted_letter.append(self.letter_to_attempt)
        print(f"attempted letter: {self.letter_to_attempt}")
        return self.letter_to_attempt

            
        
        

    def guess_letter_comp(self,guessed_letter):
        
        if guessed_letter in self.hidden_letters:
            index = self.hidden_letters.index(guessed_letter)
            index_to_be_replaced = self.hidden_indexes[index]
            self.word_to_display = self.word_to_display[:index_to_be_replaced]+guessed_letter+self.word_to_display[index_to_be_replaced+1:]

            li_word = list(self.hidden_letters)
#             remove the right guessed letter from hidden_letters list
            del li_word[index]
            self.hidden_letters = "".join(li_word)
#             remove the right guessed letter's index from hidden_letters list
            del self.hidden_indexes[index]
                            
            if self.hidden_letters:
                self.Display_word_comp()
            else:
                print(f"Computer has guessed the word: {self.word_to_display}")
        else:
            self.failed_letters.append(guessed_letter)
            self.attempts -=1
            if self.attempts>0:
                self.Display_word_comp()
            else:
                print(f"Computer lost! Word was : {self.secret_word}")

        
        

               