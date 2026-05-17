# Procedural-Document-Compiler
A tool that can be used to populate templates.

# Todo:
- ~~Create Main UI HTML~~ (Created natively in Tkinter)
- Write Parsers
    - ~~txt~~
    - html
    - docx
    - pdf
- ~~Find queries and create textboxes for each~~
- Find Dropdown queries and create dropdown options
- Find calculation queries and create fields for filling variables
- Option to save data to database (sqlite, name chosen by user)
- Option to save to Docx
- Option to save data in same format
- Option to save to PDF

# Template syntax:
### Text Query:
`{{Q:Query name, Query description}}`  
`{{Q:Query name}}`(will use details of query of same name)  
eg: `{{Q:CoAddress, Address of the Company}}`

### Calculation and Variables:
`{{C:[varA]+-/*[varB]}}`  
eg: Assets = `{{C:[Liabilities]+[Equity]}}`  
Creates two variable boxes, allowing you to fill in variables for calculation. Can contain any number of variables. If multiple calculation queries contain the same variable, it will reuse the value.

### Dropdowns:
`{{D:Dropdown Name,[<Option Name, Option Value>,<Option Name, Option Value>]}}`  
eg: `{{D:Item Type,[<Soda, The soda is fizzy>,<Sandwich, The sandwich is fresh>]}}`  
`{{D:Dropdown Name}}`(will use values of existing dropdown of same name)
