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

        self.script_dir = os.path.dirname(os.path.abspath(__file__))             # gets absolute path of this file, then gets direcory
        self.icon_path = os.path.join(self.script_dir, "resources", "icon.ico")       # Icon in the resources folder
        self.csv_path = os.path.join(self.script_dir, "resources", "book1.csv")        # CSV in the resources folder

        ####### Setting up application

        self.root = root
        self.aspect_ratio = 9/16

        self._setup_window()

        self._setup_icon()

        ####### Initialize arrays for CSV reading

        self._init_data()

        ####### Reading CSV

        self.load_csv_data()

        ####### Creating widgets and containers

        self.current_index = random.randint(0, len(self.english_words)-1)     # set up index

        self.create_widgets()
        
        ####### Creating background
        
        self.setup_background()

    ####### Defining other functions

    # Defining function to set up the window

    def _setup_window(self):
        self.root.title("Translator")
        # self.root.minsize(300, int(300 / self.aspect_ratio))  # Enforce minimum size
        initial_width = 400
        initial_height = int(initial_width / self.aspect_ratio)
        self.root.geometry(str(initial_width) + "x" + str(initial_height))
        self.root.bind("<Configure>", self._fix_aspect_ratio)
        self._resize_active = False

    #User starts resizing window
    #<Configure> event fires
    #_fix_aspect_ratio() is called
    #Inside _fix_aspect_ratio:
    #Checks if event.widget != self.root or self._resize_active → continues
    #Sets self._resize_active = True (LOCK)
    #Unbinds the <Configure> event (temporarily stops listening)
    #Applies new geometry with geometry()
    #Schedules _enable_resize_checking() to run after 10ms
    #10ms later:
    #_enable_resize_checking() executes:
    #Sets self._resize_active = False (UNLOCK)
    #Rebinds <Configure> to _fix_aspect_ratio

    def _fix_aspect_ratio(self, event):

        if event.widget != self.root or self._resize_active:       # indicating that fixing aspect ratio definition only occurs on the main window and when Resize is already being processed
            return

        new_width = event.width
        new_height = int(new_width / self.aspect_ratio)


        # this can create an infinite loop: User resizes window → `<Configure>` event → `geometry()` changes size → Another `<Configure>` event → `geometry()` changes size → ... (∞ loop)
        # to avoid this we fix the size the moment the event is finished and the size of the window is different from the original size
        if (event.height != new_height):
            # Temporarily disable the handler to prevent recursion
            self._resize_active = True
            self.root.unbind("<Configure>")
            self.root.geometry(str(new_width) + "x" + str(new_height))
            self.root.after(10, self._enable_resize_checking)  # Delay resize

    def _enable_resize_checking(self):
        self._resize_active = False
        self.root.bind("<Configure>", self._fix_aspect_ratio)

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
        self.arabic_words = []

    # Define CSV loading data

    def load_csv_data(self):
        try:
            with open(self.csv_path, mode = 'r', encoding='utf-8') as file:     # mode = 'r' indicate that the file is being read # with ensures that the file gets closed at the end of the block # encoding utf-8 to read arabic letters
                csv_reader = csv.DictReader(file)                               # DictReader reads the file as a dictionary (takes into account headers)
                for row in csv_reader:
                    self.tags.append(row['tag'])
                    self.word_types.append(row['word_type'])
                    self.english_words.append(row['english'])
                    self.arabic_latin_words.append(row['arabic_latin'])
                    self.arabic_words.append(row['arabic'])
                    
        except:
            print("CSV file not found - using sample data")     # putting sample data if there is a problem when reading the CSV
            self.english_words = ["Hello", "Goodbye", "Thank you"]
            self.arabic_latin_words = ["Marhaba", "Ma3a el salam", "Shokran"]
            
            self.tags = ["مرحبا", "", ""]
            self.word_types = ["", "", ""]
            self.arabic_words = ["", "", ""]

    # Define widget creation

    def create_widgets(self):

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)

        # English word as a label

        self.word_label = tk.Label(self.root, text=self.english_words[self.current_index], font=("Arial", 15), bg="lightblue")
        self.word_label.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")    # sticky sets the limits of cell, sticking the widget to the limits. nsew are coordinates, north south east west

        # toggle boolean counter
        self.show_is_visible = False

        # Translation as a label

        self.translation_label = tk.Label(self.root, text=self.arabic_latin_words[self.current_index], font=("Arial", 15), bg="white")
        self.translation_label.grid(row=1, column=0, padx=10, pady=20, sticky="nsew")
        self.translation_label.grid_remove()
        
        # Translation in arabic as a label

        self.arabic_translation_label = tk.Label(self.root, text=self.arabic_words[self.current_index], font=("Arial", 15), bg="white")
        self.arabic_translation_label.grid(row=2, column=0, padx=10, pady=20, sticky="nsew")
        self.arabic_translation_label.grid_remove()

        # Entry for written arabic word

        self.word_entry = tk.Entry(self.root, width=20, font=("Arial", 15), justify="center")
        self.word_entry.grid(row=3, column=0, padx=10, pady=20, sticky="ew")
        self.word_entry.focus_set()  # putting cursor in entry box by default
        self.word_entry.bind("<Return>", self.binding_enter)   # clicking enter while typing in the entry box is the same as clicking on check

        # English word as a label

        self.word_type_label = tk.Label(self.root, text=self.word_types[self.current_index], font=("Arial", 15), bg="lightblue")
        self.word_type_label.grid(row=0, column=1, padx=10, pady=20, sticky="nsew") 
        
        # button for show translation

        self.button_show_hide = tk.Button(self.root, text="Show", font=("Arial", 15), command=self.toggle_answer)
        self.button_show_hide.grid(row=1, column=1, padx=10, pady=20, sticky="nsew")
        
        # button for check word

        self.button_check = tk.Button(self.root, text="Check", font=("Arial", 15), command=self.check_word)
        self.button_check.grid(row=2, column=1, padx=10, pady=20, sticky="nsew")

        # button for next word

        self.button_next = tk.Button(self.root, text="Next", font=("Arial", 15), command=self.next_word)
        self.button_next.grid(row=3, column=1, padx=10, pady=20, sticky="nsew")

    # Define word update functions for buttons

    def next_word(self):
        # updating index
        self.current_index = random.randint(0, len(self.english_words)-1)
        
        # updating labels
        self.word_label.config(text=self.english_words[self.current_index])   # Update label text
        self.word_type_label.config(text=self.word_types[self.current_index]) # Update type label text
        self.translation_label.config(text=self.arabic_latin_words[self.current_index])  # Update translation label text
        self.arabic_translation_label.config(text=self.arabic_words[self.current_index])  # Update arabic translation label text

        # Removing show labels
        self.show_is_visible = False
        self.translation_label.grid_remove()
        self.arabic_translation_label.grid_remove()
        self.button_show_hide.config(text="Show")
        
        # clearing entry
        self.word_entry.delete(0, tk.END)                            # clear word entry for next input
        self.word_entry.config(bg="white")                           # clear word entry for next input
        
        # reset button state
        self.button_check.config(state="normal")
        self.button_show_hide.config(state="normal")  

    # define checking entry
        
    def check_word(self):       
        user_input = self.word_entry.get().strip()
        correct_answer = self.arabic_latin_words[self.current_index].lower()
        if (user_input.lower() == correct_answer):
            self.word_entry.config(bg="lightgreen")
            self.button_check.config(state="disabled")
            if not self.show_is_visible:
                self.toggle_answer()     
            self.button_show_hide.config(state="disabled")  
        else:
            self.word_entry.config(bg="pink")
            
    # define toggling the answer labels

    def toggle_answer(self):
        if self.show_is_visible:
            self.translation_label.grid_remove()
            self.arabic_translation_label.grid_remove()
            self.button_show_hide.config(text="Show")
        else:
            self.arabic_translation_label.grid()
            self.translation_label.grid()
            self.button_show_hide.config(text="Hide")
        self.show_is_visible = not self.show_is_visible
        
    # Defining the binding to Enter key ependng on the status of the entry, whether correct or not
        
    def binding_enter(self, event=None):     # Adding event in case Enter key on keyboard is clicked. It has to be set equal to None, because otherwise an error gets called when clicking on the button instead of typing enter, since the event is undefined otherwise
        if self.button_check.cget("state") == "disabled":   # 
            self.next_word()
        else:
            self.check_word()
           
    # Defining background setup
    
    def setup_background(self):
        try:
            self.background_path = os.path.join(self.script_dir, "resources", "image.png")
            self.bg_image = PhotoImage(file=self.background_path)
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()
        except Exception as e:
            print("Background not loaded: " + str(e))
     

####### Creating and calling application

if __name__ == "__main__":      # this is true when the script is ran directly, i.e. python .\translator.py. It's fine if this is built as an .exe
    root = tk.Tk()              # Tk() is the constructor for the top-level window
    app = TranslatorApp(root)
    root.mainloop()             # the event loop is required to keep the window open, otherwise it would instanteneouslyclose






####### for later

"""
remaining checklist:
1. constant aspect ratio // DONE
2. checking if we can hide labels // DONE
3. checking if we can either hide or grey out buttons // DONE
    --> Wanted behaviour: 
        --> when success after check (in check_word) (done)
        --> grey check button (in check_word) (done)
        --> click on show (unless already showing aka if text is hide) (in check_word) (done)
        --> grey show button (hide by then) (in check_word) (done)
        --> change event bind Enter to Next button (done)
        --> change states of button back to normal after hitting next (in next_word) (done)
        --> revert bind event Enter to check button (done)
 
4. maximizing size of containers and depending on size of frame/window and matching size of text, or centering them in cells// DONE
5. adding new labels and buttons for remaining csv columns // DONE
6. adding front page to select word tags (Implement word categories/filtering)
7. adding background // DONE
8. setting enter as "Check" // DONE
9. Improve the visual design
"""

# The position requires a Bachelor’s degree in Software Engineering, Computer Science, or a related field and eight
# (8) years of experience in the job offered or in an acceptable alternate occupation.
# Alternately, will accept a Master’s degree in Software Engineering, Computer Science,
# or related field and six (6) years of experience in the job offered or in an acceptable alternate occupation.
# The position requires five (5) years of experience with the following: Manual testing;
# QA tools, such as Selenium, Appium, Zephyr, Applitools, or test rail and strategies, such as BDD or TDD;
# Agile and Scrum methodology; and Test automation architecture and methodologies.  The position requires four
# (4) years of experience with CI/CD Pipeline environment.  20% domestic travel required.