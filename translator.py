import tkinter as tk            # required to make application
import random     
import os               # os.path allows to construct a cross-platform path  
import csv            
from tkinter import PhotoImage  # required to import images like background

class TranslatorApp:
    
    def __init__(self, root):
        
        """
        Initialize the translator application.
        
        Arguments:
            root (tk.Tk): Main application window
        """
        
        ####### Establishing paths

        script_dir = os.path.dirname(os.path.abspath(__file__))             # gets absolute path of this file, then gets direcory
        self.icon_path = os.path.join(script_dir, "resources", "icon.ico")       # Icon in the resources folder
        self.csv_path = os.path.join(script_dir, "resources", "data.csv")        # CSV in the resources folder

        ####### Setting up application

        self.root = root
        self.aspect_ratio = 1/2
        self._setup_window()
                        
        self._setup_icon()
                
        ####### Initialize arrays for CSV reading
        
        self._init_data()
        
        ####### Reading CSV
        
        self.load_csv_data()
        
        ####### Creating widgets and containers
               
        self.current_index = random.randint(0, len(self.english_words)-1)     # set up index
        
        self.create_widgets()
             
        
    
    ####### Defining other functions
    
    # Defining function to set up the window
    
    def _setup_window(self):
        self.root.title("Translator")
        initial_width = 300
        initial_height = int(initial_width / self.aspect_ratio)
        self.root.geometry(str(initial_width) + "x" + str(initial_height))
        self.root.bind("<Configure>", self._fix_aspect_ratio)
        
    # Defining function to fix aspect ratio
    
    def _fix_aspect_ratio(self, event):
        if event.widget == self.root:       # indicating this only occurs on the main window
            new_width = event.width
            new_height = int(new_width / self.aspect_ratio)
            
            
            # this can create an infinite loop: User resizes window → `<Configure>` event → `geometry()` changes size → Another `<Configure>` event → `geometry()` changes size → ... (∞ loop)
            # to avoid this we fix the size the moment the event is finished and the size of the window is different from the original size
            if ((event.width, event.height) != (new_width, new_height)):
                self.root.geometry(str(new_width) + "x" + str(new_height))  
    
    # Defining internal function: icon setup
        
    def _setup_icon(self):
        try:
            self.root.iconbitmap(self.icon_path)
        except:
            print("Icon file not found - using default icon")   

    # Defining internal function: internal data structures to be used
    
    def _init_data(self):
        self.tags = []               # initializing arrays to get appended from csv file
        self.word_types = []
        self.english_words = []
        self.arabic_latin_words = []
    
    # Define CSV loading data
    
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
                   
    # Define widget creation                
    
    def create_widgets(self):
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # English word as a label
        
        self.word_label = tk.Label(self.root, text=self.english_words[self.current_index], bg="lightblue")
        self.word_label.grid(row=0, column=0)
        
        # Entry for written arabic word
        
        self.word_entry = tk.Entry(self.root, width=40)
        self.word_entry.grid(row=1, column=0)      
        
        # button for check word 
        
        self.button_check = tk.Button(self.root, text="Check", command=self.check_word)
        self.button_check.grid(row=0, column=1)  
        
        # button for next word 
        
        self.button_next = tk.Button(self.root, text="Next", command=self.next_word)
        self.button_next.grid(row=1, column=1)     
    
    # Define word update functions for buttons
    
    def next_word(self):
        self.current_index = random.randint(0, len(self.english_words)-1)   
        self.word_label.config(text=self.english_words[self.current_index])  # Update label text
        self.word_entry.delete(0, tk.END)                            # clear word entry for next input
        self.word_entry.config(bg="white")                           # clear word entry for next input
        
    def check_word(self):
        user_input = self.word_entry.get().strip()
        correct_answer = self.arabic_latin_words[self.current_index].lower()
        if (user_input.lower() == correct_answer):
            self.word_entry.config(bg="lightgreen")
        else:
            self.word_entry.config(bg="pink")

####### Creating and calling application
   
if __name__ == "__main__":      # this is true when the script is ran directly, i.e. python .\translator.py. It's fine if this is built as an .exe
    root = tk.Tk()              # Tk() is the constructor for the top-level window
    app = TranslatorApp(root)   
    root.mainloop()             # the event loop is required to keep the window open, otherwise it would instanteneouslyclose
        


####### To add elsewhere for background

"""
def setup_background(self):
    # Optional background setup
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        background_path = os.path.join(script_dir, "resources", "image2.png")
        self.bg_image = PhotoImage(file=background_path)
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()
    except Exception as e:
        print(f"Background not loaded: {e}")
"""


"""
remaining checklist:
1. constant aspect ratio
2. checking if we can hide labels
3. checking if we can either hide or grey out buttons
4. maximizing size of containers and depending on size of frame/window and matching size of text, or centering them in cells
5. adding new labels and buttons for remaining csv columns
6. adding front page to select word tags (Implement word categories/filtering)
7. adding background
8. setting enter as "Check"
9. mprove the visual design
"""


