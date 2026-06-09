from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
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
# tab3 = ttk.Frame(field_tabs)

# tab1.grid_columnconfigure(2,weight=1)

field_tabs.add(tab1,text="Text Queries")
field_tabs.add(tab2,text="Option Queries")
# field_tabs.add(tab3,text="Variables")

t1_canvas = Canvas(tab1) 
t1_scroll = ttk.Scrollbar(tab1,orient="vertical",command=t1_canvas.yview)
t1_scroll_frame = ttk.Frame(t1_canvas)
t1_scroll_frame.bind(
    "<Configure>",
    lambda e: t1_canvas.configure(
        scrollregion=t1_canvas.bbox("all")
    )
)
t1_canvas_window = t1_canvas.create_window((0, 0), window=t1_scroll_frame, anchor="nw")
t1_canvas.bind(
    "<Configure>",
    lambda e: t1_canvas.itemconfig(t1_canvas_window, width=e.width)
)
t1_canvas.configure(yscrollcommand=t1_scroll.set)
t1_scroll_frame.grid_columnconfigure(2,weight=1)

t1_canvas.pack(side="left",fill="both",expand=True)
t1_scroll.pack(side="right",fill="y")

t2_canvas = Canvas(tab2) 
t2_scroll = ttk.Scrollbar(tab2,orient="vertical",command=t2_canvas.yview)
t2_scroll_frame = ttk.Frame(t2_canvas)
t2_scroll_frame.bind(
    "<Configure>",
    lambda e: t2_canvas.configure(
        scrollregion=t2_canvas.bbox("all")
    )
)
t2_canvas_window = t2_canvas.create_window((0, 0), window=t2_scroll_frame, anchor="nw")
t2_canvas.bind(
    "<Configure>",
    lambda e: t2_canvas.itemconfig(t2_canvas_window, width=e.width)
)

t2_canvas.configure(yscrollcommand=t2_scroll.set)
t2_scroll_frame.grid_columnconfigure(2,weight=1)

t2_canvas.pack(side="left",fill="both",expand=True)
t2_scroll.pack(side="right",fill="y")

def create_option_popup(var, choices, button): # Replaced dropdown menu with option popup
    option_popup = Toplevel(root)
    option_popup.title("Choose an option...")
    option_popup.geometry("300x450")
    option_popup.minsize(300,400)
    option_popup.grab_set()

    opt_canvas = Canvas(option_popup)
    opt_scrollbar = ttk.Scrollbar(option_popup, orient="vertical", command=opt_canvas.yview)
    opt_scroll_frame = ttk.Frame(opt_canvas)

    opt_scroll_frame.bind(
        "<Configure>",
        lambda e: opt_canvas.configure(scrollregion=opt_canvas.bbox("all"))
    )
    opt_canvas_window = opt_canvas.create_window((0,0), window=opt_scroll_frame, anchor="nw")
    opt_canvas.bind(
        "<Configure>",
        lambda e: opt_canvas.itemconfig(opt_canvas_window, width=e.width)
    )
    opt_canvas.configure(yscrollcommand=opt_scrollbar.set)

    opt_canvas.pack(side="left", fill="both", expand=True)
    opt_scrollbar.pack(side="right", fill="y")

    def on_select():
        selected_text = var.get()
        preview = selected_text[:25]+"..." if len(selected_text) > 25 else selected_text
        button.config(text=preview)
        option_popup.destroy()
    
    for choice in choices:
        # Standard Tkinter Radiobutton supports 'wraplength' beautifully
        rb = Radiobutton(
            opt_scroll_frame, 
            text=choice, 
            variable=var, 
            value=choice, 
            wraplength=250,     # Wraps text to fit the popup window width
            justify="left", 
            anchor="w",
            command=on_select   # Auto-closes and updates when clicked
        )
        rb.pack(fill="x", padx=10, pady=8)

queries_in_template = [] # Stores the queries retrieved from template.
text_entry_dict = {} # Stores dict of entries.
text_label_dict = {}
drop_option_dict = {}
drop_label_dict = {}
def open_template():
    # Clear existing template stuff
    global text_entry_dict
    global text_label_dict
    global drop_option_dict
    global drop_label_dict
    global queries_in_template
    text_entry_dict.clear()
    text_label_dict.clear()
    drop_option_dict.clear()
    drop_label_dict.clear()
    for element in t1_scroll_frame.winfo_children():
        element.destroy()
    for element in t2_scroll_frame.winfo_children():
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
        print(queries)
        messagebox.showinfo(title="Notice!",message=queries)
    else:
        queries_in_template = queries # set global variable for later use during replacing.
        # iterate over each list and spawn text boxes for each.

        # Add text queries programatically:
        for idx, text_query in enumerate(queries[0]):
            ttk.Label(t1_scroll_frame, text=str(idx+1)).grid(row=idx,column=0)
            text_label_dict[idx] = Label(t1_scroll_frame, text=text_query[2],wraplength=300)
            text_label_dict[idx].grid(row=idx,column=1)
            text_entry_dict[text_query[1]] = scrolledtext.ScrolledText(t1_scroll_frame,height=4)
            text_entry_dict[text_query[1]].grid(row=idx,column=2,sticky=EW)
            t1_scroll_frame.grid_rowconfigure(idx, weight=1)

        # Add dropdown queries programatically:
        for idx, drop_query in enumerate(queries[2]):
            ttk.Label(t2_scroll_frame, text=str(idx+1)).grid(row=idx,column=0)
            drop_label_dict[idx] = Label(t2_scroll_frame, text=drop_query[1],wraplength=300)
            drop_label_dict[idx].grid(row=idx,column=1)
            drop_choices = drop_query[2].split('|')
            choice_value = StringVar(t2_scroll_frame)

            # Removed option dropdown code!
            # opt_menu = OptionMenu(t2_scroll_frame,choice_value,*drop_choices)
            # opt_menu.config(width=20)
            # New popup menu code:
            opt_menu_btn = ttk.Button(t2_scroll_frame, text="Select option...")
            opt_menu_btn.config(
                command=lambda v=choice_value, c=drop_choices, b=opt_menu_btn: create_option_popup(v, c, b)
            )
            # drop_option_dict[drop_query[1]] = (choice_value, opt_menu)
            drop_option_dict[drop_query[1]] = (choice_value, opt_menu_btn)
            drop_option_dict[drop_query[1]][1].grid(row=idx,column=2,sticky=EW)
            t2_scroll_frame.grid_rowconfigure(idx,weight=1)
            
            


ttk.Label(root, text="Import template").grid(row=0,column=0)
ttk.Button(root, text="Browse", command=open_template).grid(row=0,column=1,columnspan=3,sticky=EW)

def compile_document():
    filled_text_queries = {}
    filled_drop_queries = {}
    #Gather text from all entries:
    for name, entry in text_entry_dict.items():
        filled_text_queries[name] = entry.get("1.0", END).strip()
    #Gather dropdown choices:
    for name, (choice_value,opt_menu) in drop_option_dict.items():
        filled_drop_queries[name] = choice_value.get()
    #Gather variables:
    variable_test = []
    filled_queries = [filled_text_queries,filled_drop_queries,variable_test]
    if len(chosen_template_display.get())>0:
        cmp_result = pdc.compile(chosen_template_display.get(), filled_queries, queries_in_template) # Send template file path, filled queries, and retrieved queries
        messagebox.showinfo(title="Notice!",message=cmp_result)
    else:
        messagebox.showerror(title="Error!",message="No template has been loaded.")

ttk.Button(root, text="Compile Document", command=compile_document).grid(row=5, column=0, columnspan=4,sticky=EW)

root.mainloop()