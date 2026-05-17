from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
import backend as pdc

print("Program Initialised...")

root = Tk()
root.title("Procedural Document Compiler")
root.geometry("600x500")
root.minsize(width=600,height=500)
root.grid_columnconfigure(0,weight=1)
root.grid_columnconfigure(1,weight=1)
root.grid_columnconfigure(2,weight=1)
root.grid_columnconfigure(3,weight=1)
root.grid_rowconfigure(4,weight=1)

# Template chooser

# Current template
ttk.Label(root, text="Current chosen template:").grid(row=1,column=0)
chosen_template_display = Entry(root, state='readonly')
chosen_template_display.grid(row=1,column=1,columnspan=3,sticky=EW)

field_tabs = ttk.Notebook(root)
field_tabs.grid(row=4,column=0,columnspan=4,sticky=NSEW)

tab1 = ttk.Frame(field_tabs)
tab2 = ttk.Frame(field_tabs)
tab3 = ttk.Frame(field_tabs)

# tab1.grid_columnconfigure(2,weight=1)

field_tabs.add(tab1,text="Text Queries")
field_tabs.add(tab2,text="Dropdowns")
field_tabs.add(tab3,text="Variables")

t1_canvas = Canvas(tab1) 
t1_scroll = ttk.Scrollbar(tab1,orient="vertical",command=t1_canvas.yview)
t1_scroll_frame = ttk.Frame(t1_canvas)
t1_scroll_frame.bind(
    "<Configure>",
    lambda e: t1_canvas.configure(
        scrollregion=t1_canvas.bbox("all")
    )
)
t1_canvas.create_window((0, 0), window=t1_scroll_frame, anchor="nw")
t1_canvas.configure(yscrollcommand=t1_scroll.set)
t1_scroll_frame.grid_columnconfigure(2,weight=1)

t1_canvas.pack(side="left",fill="both",expand=True)
t1_scroll.pack(side="right",fill="y")
# t1_scroll_frame.pack(fill="both",expand=True)

queries_in_template = [] # Stores the queries retrieved from template.
entry_dict = {} # Stores dict of entries.
label_dict = {}
def open_template():
    global entry_dict
    global label_dict
    global queries_in_template
    entry_dict.clear()
    label_dict.clear()
    for element in t1_scroll_frame.winfo_children():
        element.destroy()

    print("Opening File...")
    input_file = filedialog.askopenfilename(
        filetypes=(
            ("Templates", ("*.txt","*.doc", "*.docx")),
            ("Text files", "*.txt"),
            ("Word Documents", ("*.doc", "*.docx"))
        )
    )
    print("Opening ",input_file,"...")
    
    chosen_template_display.config(state='normal')
    chosen_template_display.delete(0,END)
    chosen_template_display.insert(0, input_file)
    chosen_template_display.config(state='readonly')
    
    # CONNECTION TO BACKEND
    queries = pdc.find_queries(input_file) # List of three lists: text, var and dropdown queries
    if type(queries) is str: # If it's a string, show a popup.
        print(queries) # Replace this with proper error popup
    else:
        queries_in_template = queries # set global variable for later use during replacing.
        # iterate over each list and spawn text boxes for each.
        # Add text queries programatically:
        for idx, text_query in enumerate(queries[0]):
            ttk.Label(t1_scroll_frame, text=str(idx+1)).grid(row=idx,column=0)
            label_dict[idx] = Label(t1_scroll_frame, text=text_query[2],wraplength=300)
            label_dict[idx].grid(row=idx,column=1)
            entry_dict[text_query[1]] = scrolledtext.ScrolledText(t1_scroll_frame,height=4)
            entry_dict[text_query[1]].grid(row=idx,column=2,sticky=EW)
            t1_scroll_frame.grid_rowconfigure(idx, weight=1)

ttk.Label(root, text="Import template").grid(row=0,column=0)
ttk.Button(root, text="Browse", command=open_template).grid(row=0,column=1,columnspan=3,sticky=EW)

def compile_document():
    filled_text_queries = {}
    #Gather text from all entries:
    for name, entry in entry_dict.items():
        filled_text_queries[name] = entry.get("1.0", END).strip()
    #Gather dropdown choices:
    dropdown_test = []
    #Gather variables:
    variable_test = []
    filled_queries = [filled_text_queries,dropdown_test,variable_test]
    pdc.compile(chosen_template_display.get(), filled_queries, queries_in_template) # Send template file path, filled queries, and retrieved queries

ttk.Button(root, text="Compile Document", command=compile_document).grid(row=5, column=0, columnspan=4,sticky=EW)

root.mainloop()