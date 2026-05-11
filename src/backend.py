'''
Backend script that does processes.
'''

import re

def raise_error(error):
    match error:
        case "ERR_INV_FORMAT":
            return("Template is in invalid file format!")
        case "ERR_FILE_404":
            return("Template file not found at path!")
        case "ERR_NO_QUERIES":
            return("No queries found in the template!")
        case _:
            return("Unknown Error.")


# Restructures queries to send to UI
# in: list of queries
# out: list of 3 lists: [(original query,query name,(requested values))],[vars],[]
# (In case of dropdowns, requested values will be a tuple containing dictionary pairs of option and value)
def process_queries(queries):
    text_query_list = []
    text_query_name_set = [] #keeps track of query names to prevent duplication
    calculation_list = []
    dropdown_list = [] #gets output
    dropdown_name_set = []
    for query in queries:
        #print(queries)
        #print(query)
        match query[2]:
            case 'Q':
                text_query_list.append(query)
            case 'C':
                calculation_list.append(query)
            case 'D':
                dropdown_list.append(query)
            case _:
                pass
    # Queries sorted by types.
    assembled_text_query_list = []
    assembled_dropdown_list = []
    # Get name and requested values:
    regex_tq = re.compile(r"{{Q:([^{},]+),?([^{}]*)}}")
    for raw_text_query in text_query_list:
        search_result = re.search(regex_tq, raw_text_query) #extract groups
        if search_result != None:
            query_name = search_result.group(1)
            query_description = search_result.group(2)
            #check if name exists in set
            if query_name not in text_query_name_set:
                text_query_name_set.append(query_name)
                assembled_query = [raw_text_query, query_name, query_description]
                assembled_text_query_list.append(assembled_query)

    regex_cl = re.compile(r"\[[^+-/*%!]*?\]")
    list_of_vars = []
    list_of_assembled_calc_queries = []
    for raw_calc_query in calculation_list:
        expression = raw_calc_query[4:-2]
        var_search = re.findall(regex_cl,raw_calc_query)
        if len(var_search) > 0:
            for var in var_search:
                assembled_calc_query = [raw_calc_query, expression]
                if var not in list_of_vars:
                    list_of_vars.append(var)
            list_of_assembled_calc_queries.append(assembled_calc_query)
    assembled_calc_list = [list_of_vars, list_of_assembled_calc_queries] #list of two lists: [all vars], [[raw, expression],..]

    return([assembled_text_query_list,assembled_calc_list,[]])
    
# Gets list of all queries [{{...}},]
def parse_txt(file_path):
    re_query_getter = re.compile(r"{{[^{}]*?}}")
    queries = []
    try:
        with open(file_path) as txt_file:
            for line in txt_file.readlines():
                queries_in_line = re.findall(re_query_getter,line)
                if len(queries_in_line) > 0:
                    for q in queries_in_line:
                        queries.append(q)
                
    except FileNotFoundError:
        return(raise_error("ERR_FILE_404"))
    
    if len(queries) > 0:
        return(process_queries(queries))
    else:
        return(raise_error("ERR_NO_QUERIES"))


def find_queries(template_file):
    file_ext = template_file[template_file.rindex('.'):]
    #print(file_ext)
    match file_ext:
        case '.txt':
            return(parse_txt(template_file))
        #case '.docx':
        #    parse_docx(template_file)
        case _:
            return(raise_error("ERR_INV_FORMAT"))

# Called from ui, after file chosen.
