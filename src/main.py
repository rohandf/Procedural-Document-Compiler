from tkinter import *
from tkinter import filedialog
from tkinter import ttk
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
# root.grid_rowconfigure(4,weight=1)

# Template chooser

# Current template
ttk.Label(root, text="Current chosen template:").grid(row=1,column=0)
ttk.Entry(root, state='readonly').grid(row=1,column=1,columnspan=3,sticky=EW)

def open_template():
    print("Opening File...")
    input_file = filedialog.askopenfilename(
        filetypes=(
            ("Templates", ("*.txt","*.doc", "*.docx")),
            ("Text files", "*.txt"),
            ("Word Documents", ("*.doc", "*.docx"))
        )
    )
    print("Opening ",input_file,"...")
    queries = pdc.find_queries(input_file) # List of three lists: text, var and dropdown queries
    if type(queries) is str: # If it's a string, show an error message.
        print(queries) # Replace this with proper error popup
    else:
        # iterate over each list and spawn text boxes for each.
        print(queries) # Replace this with actual code for ^ this


ttk.Label(root, text="Import template").grid(row=0,column=0)
ttk.Button(root, text="Browse", command=open_template).grid(row=0,column=1,columnspan=3,sticky=EW)

field_tabs = ttk.Notebook(root)
field_tabs.grid(row=4,column=0,columnspan=4,sticky=NSEW)

tab1 = ttk.Frame(field_tabs)
tab2 = ttk.Frame(field_tabs)
tab3 = ttk.Frame(field_tabs)

field_tabs.add(tab1,text="Text Queries")
field_tabs.add(tab2,text="Dropdowns")
field_tabs.add(tab3,text="Variables")

# queries = pdc.start_process()

root.mainloop()