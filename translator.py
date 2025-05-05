import tkinter as tk            # required to make application
import random       
import csv            
from tkinter import PhotoImage  # required to import images like background

import os               # os.path allows to construct a cross-platform path

class TranslatorApp:
    def __init__(self, root):
        
        ####### Establishing paths

        script_dir = os.path.dirname(os.path.abspath(__file__))             # gets absolute path of this file, then gets direcory
        self.icon_path = os.path.join(script_dir, "resources", "icon.ico")       # Icon in the resources folder
        self.csv_path = os.path.join(script_dir, "resources", "data.csv")        # CSV in the resources folder

        ####### Setting up application

        self.root = root
        self.root.title("Translator")
        self.root.geometry("400x400")
        
        # setting up icon
        
        try:
            self.root.iconbitmap(self.icon_path)
        except:
            print("Icon file not found - using default icon")
            
        ####### Initialize arrays for CSV reading

        self.tags = []               # initializing arrays to get appended from csv file
        self.word_types = []
        self.english_words = []
        self.arabic_latin_words = []
              
        ####### Reading CSV
        
        # function to read CSV
        
        def load_csv_data(self):
            try:
                with open(self.csv_path, mode = 'r') as file:    # mode = 'r' indicate that the file is being read # with ensures that the file gets closed at the end of the block
                    csv_reader = csv.DictReader(file)       # DictReader reads the file as a dictionary (takes into account headers)
                    for row in csv_reader:
                        self.tags.append(row['tag'])
                        self.word_types.append(row['word_type'])
                        self.english_words.append(row['english'])
                        self.arabic_latin_words.append(row['arabic_latin'])
            except:
                print("CSV file not found - using sample data")     # putting sample data if there is a problem when reading the CSV
                self.english_words = ["Hello", "Goodbye", "Thank you"]
                self.arabic_latin_words = ["Marhaba", "Ma3a el salam", "Shokran"]

        # loading the CSV data

        self.load_csv_data()
                     
        ####### Initialize widgets and containers
        
        # index
        
        self.current_index = random.randint(0, len(self.english_words)-1)
        
        # Define the creation of all GUI widgets
        
        def create_widgets(self):
            self.word_label = tk.Label(self.root, text=self.english_words[self.index], bg="lightgreen")
            self.word_label.pack()
            

        
        
  



####### Update widgets

def next_word():
    index = random.randint(0, len(english_words)-1)   
    label1.config(text=english_words[index])  # Update label text
    
def check_word():
    word_input = word_entry.get().strip()
    if (word_input.lower() == 1):
        
    
    
####### Labels and containters

button_next = tk.Button(root, text="Next", command=next_word)
button_next.pack()

word_entry = tk.Entry(root, width=30)
word_entry.pack()


# Load the image
""" background_path = os.path.join(script_dir, "resources", "image2.png") 
bg_image = PhotoImage(file=background_path) """

# Create a label for the background
""" bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Covers the entire window """


####### Creating application

root = tk.Tk()          # Tk() is the constructor for the top-level window



root.mainloop()         # the event loop is required to keep the window open, otherwise it would instanteneouslyclose