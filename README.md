# Procedural-Document-Compiler
A tool that can be used to populate templates.

### Download here:
[CLICK TO GO TO LATEST RELEASE. DOWNLOAD VERSION APPROPRIATE TO YOUR OS, AND DOWNLOAD THE MANUAL PDF.](https://github.com/rohandf/Procedural-Document-Compiler/releases/latest)

# Todo:
- ~~Create Main UI HTML~~ (Created natively in Tkinter)
- Write Parsers
    - ~~txt~~
    - other txt based files
    - ~~docx~~
    - odf
- ~~Find queries and create textboxes for each~~
- ~~Find Dropdown queries and create dropdown options~~ (Renamed to Option Queries)
- Find calculation queries and create fields for filling variables
- Option to save data to database (sqlite, name chosen by user)
- Option to export doc to PDF

# Template syntax:
### Text Query:
`{{Q:Query name, Query description}}`  
`{{Q:Query name}}`(will use details of query of same name)  
eg: `{{Q:CoAddress, Address of the Company}}`

### Dropdowns:
`{{D:Dropdown Name,[<Option Name, Option Value>,<Option Name, Option Value>]}}`  
eg: `{{D:Item Type,[<Soda, The soda is fizzy>,<Sandwich, The sandwich is fresh>]}}`  
`{{D:Dropdown Name}}`(will use values of existing dropdown of same name)

### Calculation and Variables: *(Not implemented yet!)*
`{{C:[varA]+-/*[varB]}}`  
eg: Assets = `{{C:[Liabilities]+[Equity]}}`  
Creates two variable boxes, allowing you to fill in variables for calculation. Can contain any number of variables. If multiple calculation queries contain the same variable, it will reuse the value.

# Issues:
If you have run into issues and bugs, please remember that this project is still in its infancy. They will be fixed over time.

# For contributors:
I am a student working on this in my spare time. I am not taking contributions or PRs from people. Please refrain from creating PRs. I will likely not have the time to review your code.
