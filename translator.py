import tkinter as tk            # required to make application
import random
import os               # os.path allows to construct a cross-platform path
import csv
from tkinter import PhotoImage  # required to import images like background

class TagSelector:
    
    def __init__(self, root, start_app, tag_path):
        
        """
        Set up front page for the set of tags to be used for this application.

        Arguments:
            root (tk.Tk): Main application window
            start_app   : self.setup_initialization to initialize the application after the tags are chosen
        """
        
        self.root = root
        
        self.start_app = start_app
        self.tag_path = tag_path
        
        # self.frame = tk.Frame(root, bg='')  # bg='' makes sure the frame has no background
        # self.frame.grid(row=0, column=0, sticky="nsew")   
        # self.frame.pack(fill='both', expand=True)   
        
        # Create a main frame with fixed propagation
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        
        self.main_frame.pack_propagate(False)
        
        # Create a canvas with scrollbar
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.inner_frame = tk.Frame(self.canvas)
        
        # Configure canvas scrolling
        self.inner_frame.bind("<Configure>", self._inner_frame_bind)
        
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # self.frame.grid_columnconfigure(0, weight=1)
        # self.frame.grid_rowconfigure(0, weight=1)
        
        self.setup_widgets()
    
    # Define function to setup up load_tags button, check buttons for every tag, and a test button for debugging purposes
    def setup_widgets(self):
        # Button to load tags into app
        self.button_load_tags = tk.Button(
            self.inner_frame, 
            text="Load Tags", 
            font=("Arial", 15), 
            fg="white",                     # text color
            bg="#e20004",                   # background color
            activebackground="#c32834",     # when hovered or clicked
            activeforeground="white",       # text color when clicked
            relief="raised",                # border style: "flat", "raised", "sunken", "ridge", "groove"
            bd=5,                           # border width
            command=self.return_to_app 
        )
        # self.test.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
        self.button_load_tags.pack(padx=50, pady=50, anchor='w') 
        
        # Getting the list of unique tags through load_tags
        self.tags = self.load_tags()
        
        # initializing tag_vars as a dictionary which will take a unique tag as a key and the "variable" (boolean object) as its associated variable
        self.tag_vars = {}
        
        for tag in self.tags:
            value = None
            if tag == "1: most frequent":
                value = True
            variable = tk.BooleanVar(value=value)
            tk.Checkbutton(self.inner_frame, var=variable, text=tag, font=("Arial", 15)).pack(padx=50, pady=2, anchor='w')
            self.tag_vars[tag] = variable
        
        self.test = tk.Button(
            self.inner_frame, 
            text="test", 
            font=("Arial", 15), 
            fg="white",                     # text color
            bg="#e20004",                   # background color
            activebackground="#c32834",     # when hovered or clicked
            activeforeground="white",       # text color when clicked
            relief="raised",                # border style: "flat", "raised", "sunken", "ridge", "groove"
            bd=5,                           # border width
            command=self.test 
        ).pack()
    
    # Define test function for debugging purposes
    def test(self):
        print(self.tag_vars)
        for tag in self.tags:
            print(self.tag_vars.get(tag).get())    
        
    # Define function to get list of unique tags 
    def load_tags(self):
        tags = set()    # set() returns a list or array of unique tag values
        with open(self.tag_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file) 
            for row in csv_reader:
                tags.add(row.get('tag'))
        return tags     
    
    # Define function destroying the whole frame while recalling the main application frame with the selected tags
    def return_to_app(self):
        selected_tags = []
        for tag in self.tag_vars:
            if self.tag_vars.get(tag).get():
                selected_tags.append(tag)
        self.main_frame.destroy()
        self.start_app(selected_tags)
    
    def _inner_frame_bind(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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
        
        ####### Setting up window and icon
        
        self._setup_window()
        self._setup_icon()
        
        self.fullscreen_boolean = False
        self.root.attributes("-fullscreen", self.fullscreen_boolean)  # Fullscreen mode
        
        self.root.bind("<Escape>", self.escape_fullscreen)
        self.root.bind("<F11>", self.toggle_fullscreen)
        
        ####### Creating background
        
        self.setup_background()
        
        TagSelector(self.root, self.setup_initialization, self.csv_path)
        
    def escape_fullscreen(self, event=None):
        self.fullscreen_boolean = False
        self.root.attributes("-fullscreen", self.fullscreen_boolean)

    def toggle_fullscreen(self, event=None):
        if not self.fullscreen_boolean:
            self.root.attributes("-fullscreen", True)
        else:
            self.root.attributes("-fullscreen", False)
        self.fullscreen_boolean = not self.fullscreen_boolean
          
    def setup_initialization(self, selected_tags):

        ####### Defining tags selected in TagSelector
        self.selected_tags = selected_tags
        print(self.selected_tags)
        
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
            if hasattr(self, 'bg_label'):
                self.bg_label.place_configure(relwidth=1, relheight=1)
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
                    if (row.get('tag') in self.selected_tags) or (not self.selected_tags):  # 2 conditions: if tag is in the selected tag, or if nothing cosem choose everything
                        self.tags.append(row.get('tag'))
                        self.word_types.append(row.get('word_type'))
                        self.english_words.append(row.get('english'))
                        self.arabic_latin_words.append(row.get('arabic_latin'))
                        self.arabic_words.append(row.get('arabic'))
                    
        except:
            print("CSV file not found - using sample data")     # putting sample data if there is a problem when reading the CSV
            self.english_words = ["Hello"] * 3
            self.arabic_latin_words = ["Marhaba"] * 3
            self.tags = ["1: most frequent"] * 3
            self.word_types = ["P"] * 3
            self.arabic_words = ["مرحبا"] * 3

    # Define widget creation
    def create_widgets(self):

        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=2)
        self.root.grid_rowconfigure(2, weight=2)
        self.root.grid_rowconfigure(3, weight=2)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)

        # English word as a label
        self.word_label = tk.Label(self.root, text=self.english_words[self.current_index], font=("Arial", 15), bg="lightblue", wraplength = 200)
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
        self.button_show_hide = tk.Button(
            self.root, 
            text="Show", 
            font=("Arial", 15), 
            fg="white",                     # text color
            bg="#e20004",                   # background color
            activebackground="#c32834",     # when hovered or clicked
            activeforeground="white",       # text color when clicked
            relief="raised",                # border style: "flat", "raised", "sunken", "ridge", "groove"
            bd=5,                           # border width
            command=self.toggle_answer
        )
        self.button_show_hide.grid(row=1, column=1, padx=10, pady=20, sticky="nsew")
        
        # button for check word
        self.button_check = tk.Button(
            self.root, 
            text="Check", 
            font=("Arial", 15), 
            fg="white", 
            bg="#18a5c0", 
            activebackground="#0085b0", 
            activeforeground="white", 
            relief="raised", 
            bd=5, 
            command=self.check_word
        )
        self.button_check.grid(row=2, column=1, padx=10, pady=20, sticky="nsew")

        # button for next word
        self.button_next = tk.Button(
            self.root, 
            text="Next", 
            font=("Arial", 15), 
            fg="white", 
            bg="#f7a23a", 
            activebackground="#fc8424", 
            activeforeground="white", 
            relief="raised", 
            bd=5, 
            command=self.next_word
        )
        self.button_next.grid(row=3, column=1, padx=10, pady=20, sticky="nsew")
        
        # button for return to tag selector
        self.button_tag_selector = tk.Button(
            self.root, 
            text=self.tags[self.current_index], 
            font=("Arial", 15), 
            fg="white", 
            bg="#383328", 
            activebackground="#706653", 
            activeforeground="white", 
            relief="raised", 
            bd=5, 
            command=self.return_to_tag_selector
        )
        self.button_tag_selector.grid(row=4, column=0, columnspan=2, padx=80, pady=30, sticky="nsew") #  columnspan=2 puts it accross multiple columns

    # Define word update functions for buttons
    def next_word(self):
        # updating index
        self.current_index = random.randint(0, len(self.english_words)-1)
        
        # updating labels
        self.word_label.config(text=self.english_words[self.current_index])   # Update label text
        self.word_type_label.config(text=self.word_types[self.current_index]) # Update type label text
        self.translation_label.config(text=self.arabic_latin_words[self.current_index])  # Update translation label text
        self.arabic_translation_label.config(text=self.arabic_words[self.current_index])  # Update arabic translation label text
        self.button_tag_selector.config(text=self.tags[self.current_index])
        
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
            
    # define returning to tag selector
    def return_to_tag_selector(self):
        self.children = self.root.winfo_children()  # returns a list of all child widgets in a parent widget, here inside of root
        for widget in self.children:
            if widget != self.bg_label:
                widget.destroy()
        TagSelector(self.root, self.setup_initialization, self.csv_path)
        if hasattr(self, 'bg_label'):
            self.bg_label.lower()
    
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
1.  constant aspect ratio // DONE
2.  checking if we can hide labels // DONE
3.  checking if we can either hide or grey out buttons // DONE
    --> Wanted behaviour: 
        --> when success after check (in check_word) (done)
        --> grey check button (in check_word) (done)
        --> click on show (unless already showing aka if text is hide) (in check_word) (done)
        --> grey show button (hide by then) (in check_word) (done)
        --> change event bind Enter to Next button (done)
        --> change states of button back to normal after hitting next (in next_word) (done)
        --> revert bind event Enter to check button (done)
 
4.  maximizing size of containers and depending on size of frame/window and matching size of text, or centering them in cells// DONE
5.  adding new labels and buttons for remaining csv columns // DONE
6.  adding front page to select word tags (Implement word categories/filtering) // DONE
7.  adding background // DONE
8.  setting enter as "Check" // DONE
9.  Improve the visual design // DONE
10. Developping this as an .exe
11. Developping this as an Android application
12. Listing Requirements for tool
13. Developping testing procedure for tool
14. Developping CI/CD for tool for each release
"""