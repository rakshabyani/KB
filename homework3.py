import lex
from copy import deepcopy
import re

def main():
    file = open("input.txt","r")

    no_of_queries = file.readline().strip()
    queries_list = []
    for i in range(int(no_of_queries)):
        temp = re.sub('\s+','',file.readline()).strip('\n').strip()
        queries_list.append(temp)

    no_of_sentences_KB = file.readline().strip()
    KB = []
    KB_and_clauses = []
    KB_string = []
    for n in range(int(no_of_sentences_KB)):
        temp = re.sub('\s+', '', file.readline()).strip('\n').strip()
        # temp = file.readline().replace("\s+", "").strip('\n')
        KB.append(lex.parser.parse(temp))

    #Convert to CNF
    for i in range(len(KB)):
        temp = KB[i]
        KB_and_clauses=[]

        #
        #
        # for sublist in temp:
        #     if isinstance(temp[sublist],list):
        #         removeimplication(temp[sublist])
        #     if '=>' in sublist:
        # #print(any('~' in x for x in temp))
        # if '=>' in temp:
        #     KB[i] = removeimplication(temp)
        # else:
        #     result = list(get_positions(temp,'=>'))
            # if len(result) > 0 :
            #     length = len(result[0])
            #     posImp = temp[result[0][0]]
            #     for index in range(1,len(result[0])-1):
            #         print(temp[index])
            #         posImp = posImp[index] #posImp has the clause with imply symbol
            #
            # # Replace this properly in it's position
            # after_removing_imply = removeimplication(posImp)
            # result = list(get_positions(temp,after_removing_imply))
            # if len(result):
            #     length  = len(result[0])
            #     posImp = temp[result[0][0]]
            #     for index in range(1,len(result[0])-2):
            #         print(temp[index])
            #         posImp = posImp[index]
            #     posImp[len(result[0]) - 1 ] = after_removing_imply
            #     KB[i] = posImp
            #     # posImp = result[0]
        temp_clause = []
        if not isinstance(temp,str):
            for sublist in temp:
                if isinstance(sublist,list):
                    sublist = removeimplication(sublist)
            if '=>' in temp:
                implypos = temp.index('=>')
                temp[implypos] = '|'
                clause_to_negate = temp[implypos - 1]
                temp_clause.append('~')
                temp_clause.append(clause_to_negate)
                temp[implypos - 1] = temp_clause
                KB[i] = temp
        else:
            KB[i] = temp

        temp = negateloop(temp)
        KB[i] = temp
        # result = [element for element in temp if '~' in element]
        # if len(result):
        #     #indices = [i for i, x in enumerate(temp) if x == "~"]
        #     posnot = temp.index(result[0])
        #     clause_to_negate = temp[posnot][1]
        #     if isinstance(clause_to_negate,list):
        #         negated_clause = negationMethod(clause_to_negate)
        #         temp[posnot] = negated_clause
        #         KB[i] = temp

        temp = convert_to_conjunction_of_clauses(temp)
        KB[i] = temp
        # if '|' in temp:
        #     pos = temp.index('|')
        #     result = [element for element in temp if '&' in element]
        #     temp = convert_to_conjunction_of_clauses(temp[pos - 1], temp[pos + 1])
        #     KB[i] = temp
        temp = seperate_and_clauses(temp)
        if isinstance(temp,list):
            KB_string.extend(temp)
        else:
            KB_string.append(temp)
        # KB[i] = temp
        # if '&' in temp:
        #     pos_of_and = temp.index('&')
        #     clause_before = temp[pos_of_and - 1]
        #     clause_after = temp[pos_of_and + 1]
        #     KB_and_clauses.append(seperate_and_clauses(clause_before))
        #     KB_and_clauses.append(seperate_and_clauses(clause_after))
        # else:
        #     KB_and_clauses.append(temp)
        # for element in KB_and_clauses:
        #     if isinstance(element,str):
        #         KB_string.append(element)
        #     else:
        #         KB_string.append(convert_to_string(element))
            # for element in KB[i]:
                # if isinstance(element,list):
                #     KB_string.append(convert_to_string(element))
                # else:
                #     KB_string.append(temp)
    print(KB_string)

    predicates = []
    for kbs in KB_string:
        list_of_predicates = []
        if '|' in kbs:
            list_of_predicates = kbs.split('|')
            # list_of_predicates.append(0)
            list_of_predicates = [NOT(x) for x in list_of_predicates]
        else:
            list_of_predicates.append(NOT(kbs))
        predicates.append(list_of_predicates)

    output = open("output.txt","w")

    #Resolve the query
    for query in queries_list:
        indices = []
        query = NOT(query)
        list_of_query_ele = []
        list_of_query_ele.append(query)
        dict_predicates = {}
        dict = {}
        try:
            is_resolved = resolve(list_of_query_ele, KB_string, dict, dict_predicates, predicates)
        except RuntimeError as res:
            is_resolved = "False"

        if is_resolved == "Resolved":
            output.write("TRUE")
        else:
            output.write("FALSE")
        output.write("\n")
    output.close()



#STEP 1 : method to remove implication
def removeimplication(clause):
    temp = []
    for sublist in clause:
        if isinstance(sublist, list):
            # sublist = removeimplication(sublist)
            if '=>' in sublist:
                implypos = sublist.index('=>')
                sublist[implypos] = '|'
                clause_to_negate = sublist[implypos - 1]
                temp.append('~')
                temp.append(clause_to_negate)
                sublist[implypos - 1] = temp
                break
            else:
                sublist = removeimplication(sublist)

    if '=>' in clause:
        implypos = clause.index('=>')
        clause[implypos] = '|'
        clause_to_negate = clause[implypos - 1]
        temp.append('~')
        temp.append(clause_to_negate)
        clause[implypos - 1] = temp

    return clause


#STEP 2 : method to move negation inside
def negateloop(clause):


    for index in range((len(clause))):
        sublist = clause[index]
        if sublist == '~':
            if isinstance(clause[index + 1], list):
                clause = negationMethod(clause[index+1])
                # clause.pop(0)
                break
            else:
                continue
        if isinstance(sublist, list):
            sublist = negateloop(sublist)
            clause[index] = sublist
    if '~' in clause:
        if isinstance(clause[1], list):
            clause[1] = negationMethod(clause[1])
            clause.pop(0)

    return clause

def negationMethod(clause_to_negate):
    temp = []
    if '&' in clause_to_negate:
        #indices = [i for i, x in enumerate(temp) if x == "&"]
        pos_of_and = clause_to_negate.index('&')
        clause_to_negate[pos_of_and] = '|'
        if isinstance(clause_to_negate[pos_of_and - 1 ] , list):
            clause_to_negate[pos_of_and - 1 ] = negationMethod(clause_to_negate[pos_of_and - 1])
        else:
            clause_to_negate[pos_of_and - 1] = NOT(clause_to_negate[pos_of_and - 1 ])
        if isinstance(clause_to_negate[pos_of_and + 1 ], list ):
            clause_to_negate[pos_of_and + 1 ] = negationMethod(clause_to_negate[pos_of_and + 1])
        else:
            clause_to_negate[pos_of_and + 1] = NOT(clause_to_negate[pos_of_and + 1 ])

    elif '|' in clause_to_negate:
        pos_of_or = clause_to_negate.index('|')
        clause_to_negate[pos_of_or] = '&'
        if isinstance(clause_to_negate[pos_of_or - 1], list):
            clause_to_negate[pos_of_or - 1] = negationMethod(clause_to_negate[pos_of_or - 1])
        else:
            clause_to_negate[pos_of_or - 1] = NOT(clause_to_negate[pos_of_or - 1])
        if isinstance(clause_to_negate[pos_of_or + 1], list):
            clause_to_negate[pos_of_or + 1] = negationMethod(clause_to_negate[pos_of_or + 1])
        else:
            clause_to_negate[pos_of_or + 1] = NOT(clause_to_negate[pos_of_or + 1])

    elif '~' in clause_to_negate:
        clause_to_negate.pop(0)
    return clause_to_negate

#STEP 3 : Convert to conjunction of disjunction clauses

def convert_to_conjunction_of_clauses(clause):
    simplified_clause = []
    for index in range(len(clause)):
        subclause = clause[index]
        if isinstance(subclause,list):
            subclause = convert_to_conjunction_of_clauses(subclause)
            clause[index] = subclause


    if '|' in clause:
        posOr = clause.index('|')
        clause_before = clause[posOr - 1 ]
        clause_after = clause[posOr + 1]
        temp_clause = []
        pos_and_in_clause_before = []
        pos_and_in_clause_after = []
        if isinstance(clause_before,list):
            pos_and_in_clause_before = [i for i in range(len(clause_before)) if clause_before[i] == '&']
        if isinstance(clause_after,list):
            pos_and_in_clause_after = [i for i in range(len(clause_after)) if clause_after[i] == '&']
        if(len(pos_and_in_clause_after) > 0) and (len(pos_and_in_clause_before)>0):
            for count in range(len(pos_and_in_clause_after)):
                temp_clause = []
                term1_in_clause_after_and = clause_after[pos_and_in_clause_after[count] - 1]
                temp_clause.append(clause_before)
                temp_clause.append('|')
                temp_clause.append(term1_in_clause_after_and)
                simplified_clause.append(convert_to_conjunction_of_clauses(temp_clause))
                simplified_clause.append('&')
            temp_clause = []
            term2_in_clause_after_and = clause_after[pos_and_in_clause_after[count] + 1]
            temp_clause.append(clause_before)
            temp_clause.append('|')
            temp_clause.append(term2_in_clause_after_and)
            simplified_clause.append(convert_to_conjunction_of_clauses(temp_clause))

        elif len(pos_and_in_clause_before) > 0 :
            for count in range(len(pos_and_in_clause_before)):
                temp_clause = []
                temp_clause.append(clause_before[pos_and_in_clause_before[count] - 1])
                temp_clause.append('|')
                temp_clause.append(clause_after)
                simplified_clause.append(temp_clause)
                simplified_clause.append('&')
            temp_clause = []
            temp_clause.append(clause_before[pos_and_in_clause_before[count] + 1])
            temp_clause.append('|')
            temp_clause.append(clause_after)
            simplified_clause.append(temp_clause)

        elif len(pos_and_in_clause_after) > 0:
            # print(range(len(pos_and_in_clause_after)))
            for count in range(len(pos_and_in_clause_after)):
                temp_clause = []
                temp_clause.append(clause_before)
                temp_clause.append('|')
                temp_clause.append(clause_after[pos_and_in_clause_after[count] - 1])
                simplified_clause.append(temp_clause)
                simplified_clause.append('&')
            temp_clause = []
            temp_clause.append(clause_before)
            temp_clause.append('|')
            temp_clause.append(clause_after[pos_and_in_clause_after[count] + 1])
            simplified_clause.append(temp_clause)
    if '&' in clause:
        pos_of_and = clause.index('&')
        simplified_clause.append(clause[pos_of_and - 1 ])
        simplified_clause.extend('&')
        if isinstance(clause[pos_of_and + 1],list):
            simplified_clause.extend(clause[pos_of_and + 1 ])
        else :
            simplified_clause.append(clause[pos_of_and + 1])
        # clause = clause.remove(posOr)

    if len(simplified_clause) == 0 :
        simplified_clause = clause
    return simplified_clause

#STEP 4 : Remove the parantheses and make it a list of clauses
def seperate_and_clauses(clause):
    KB_and_clauses = []
    for subclause in clause:
        if isinstance(subclause,list):
            subclause = seperate_and_clauses(subclause)
    if '&' in clause:
        pos_of_and = [i for i in range(len(clause)) if clause[i] == '&']
        for count in range(len(pos_of_and)):
            clause_before = clause[pos_of_and[count] - 1]
            KB_and_clauses.append(convert_to_string(clause_before))
        clause_after = clause[pos_of_and[count] + 1]
        KB_and_clauses.append(convert_to_string(clause_after))

    if len(KB_and_clauses) == 0:
        KB_and_clauses = convert_to_string(clause)

    return KB_and_clauses


def convert_to_string(clause):
    KB_string = ''
    for element in clause:
        if isinstance(element,list):
            KB_string += convert_to_string(element)
        else:
            KB_string += element
    return KB_string

def resolve(list_of_query_ele, KB_string, dict,dict_predicates, predicates):
    is_resolved = False
    list_of_predicates = []
    indices = []
    index_of_query = 0
    while (len(list_of_query_ele) != 0) and (index_of_query < len(list_of_query_ele)):
        query = list_of_query_ele[index_of_query]
        index_of_query += 1
        # check_in_KB(query)
        predicate_q = get_query_predicate(query)
        indices = []
        for i in range(len(predicates)):
            ele = ''
            element = predicates[i]
            for elem in element:
                if (elem.find(predicate_q) != -1) :
                    for elem in element:
                        ele += NOT(elem) + '|'
                    ele = ele[:-1]
                    indices.append(ele)

        for index_clause in indices:
            dict_copy = {}
            # dict_predicates_copy = deepcopy(dict_predicates)
            list_of_query = deepcopy(list_of_query_ele)
            is_resolved = False
            is_unified = check_in_KB(query,KB_string, dict_predicates, list_of_query, dict_copy, index_clause)
            if is_unified == "Resolved":
                return "Resolved"
            if is_unified == "False" and len(list_of_query) == 1:
                continue
            if is_unified == "False":
                continue
            if is_unified == "True" and len(list_of_query) == 0:
                return True
            is_resolved = resolve(list_of_query, KB_string, dict_copy, dict_predicates, predicates)
            if is_resolved == "Resolved":
                return "Resolved"

    return "False"

def check_in_KB(query, KB_string, dict_predicates,list_of_query_ele, dict, matching_clause):

    predicate_q = ''
    i = 0
    while (query[i] != '('):
        predicate_q += query[i]
        i += 1
    i = i + 1
    vars_q = query[i:len(query) - 1]

    list_of_predicates = []
    if '|' in matching_clause:
        list_of_predicates = matching_clause.split('|')
        list_of_predicates = [NOT(x) for x in list_of_predicates]
    else:
        list_of_predicates.append(NOT(matching_clause))

    unified = False
    for predicate in list_of_predicates:
        predicate_s = ''
        i = 0
        while (predicate[i] != '('):
            predicate_s += predicate[i]
            i += 1
        i = i + 1
        vars_s = predicate[i:len(predicate) - 1]
        query_variables = vars_q.split(',')
        sentence_variables = vars_s.split(',')
        if (predicate_q == predicate_s):
            if len(query_variables) == len(sentence_variables):
                unified = unify(vars_q, vars_s,dict)
        if unified:
            # dict_predicates[matching_clause] = 1
            list_of_predicates.remove(predicate)
            temp_list = []
            infinity_check = []
            infinity_check_list = []
            # put this to keep a check for infinity. Before I replace the var names, I need to store in this. Because otherwise it'll never get compared
            for temp in list_of_predicates:
                # calculate the variables
                pred_s = ''
                i = 0
                while (temp[i] != '('):
                    pred_s += temp[i]
                    i += 1
                i = i + 1
                vars_s = temp[i:len(temp) - 1]
                sentence_variables = vars_s.split(',')

                pred_s+='('
                for var in sentence_variables:
                    if var in dict.keys():
                        pred_s += dict[var] + ','
                    else:
                        pred_s += var + ','

                pred_s = pred_s[:-1]
                pred_s += ')'

                temp_list.append(NOT(pred_s))
            list_of_query_ele.remove(query)

            for pos in range(len(list_of_query_ele)):
                temp = list_of_query_ele[pos]
                pred_s = ''
                i = 0
                while (temp[i] != '('):
                    pred_s += temp[i]
                    i += 1
                i = i + 1
                vars_s = temp[i:len(temp) - 1]
                sentence_variables = vars_s.split(',')

                pred_s += '('
                for var in sentence_variables:
                    if var in dict.keys():
                        pred_s += dict[var] + ','
                    else:
                        pred_s += var + ','
                pred_s = pred_s[:-1]
                pred_s += ')'
                list_of_query_ele[pos] = pred_s

            list_of_query_ele.extend(temp_list)
            if matching_clause in dict_predicates.keys():
                if dict_predicates[matching_clause] == list_of_query_ele:
                    return "False"
            else:
                dict_predicates[matching_clause] = list_of_query_ele
            if len(list_of_query_ele) == 0:
                return "Resolved"
            return "True"
    return "False"

def unify(vars_q, vars_s,dict):
    no_of_vars_unified = 0
    query_variables = vars_q.split(',')
    sentence_variables = vars_s.split(',')
    if len(query_variables) != len(sentence_variables):
        return False

    for index in range(len(query_variables)):
        variable_q = query_variables[index]
        variable_s = sentence_variables[index]

        #F(x) and F(Tim)
        if (isVar(variable_q)) and (not isVar(variable_s)):
            if variable_q in dict:
                if dict[variable_q] == variable_s:
                    no_of_vars_unified += 1

            else:
                if not (variable_s in dict.values()):
                    dict[variable_q] = variable_s
                    no_of_vars_unified += 1

        #F(Jack) and F(y)
        elif (not isVar(variable_q)) and (isVar(variable_s)):
            if variable_s in dict:
                if dict[variable_s] == variable_q:
                    no_of_vars_unified += 1

            else:
                if not variable_q in dict.values():
                    dict[variable_s] = variable_q
                    no_of_vars_unified += 1

        #F(x) nd F(y)
        elif (isVar(variable_q)) and (isVar(variable_s)):
            if (variable_q in dict) and (not variable_s in dict):
                dict[variable_s] = dict.get(variable_q)
                no_of_vars_unified += 1
            elif (not variable_q in dict) and (variable_s in dict):
                dict[variable_q] = dict.get(variable_s)
                no_of_vars_unified += 1
            else:
                dict[variable_s] = variable_q + '1'
                no_of_vars_unified += 1

        #F(Jack) and F(Jack)
        elif (not isVar(variable_q)) and (not isVar(variable_s)):
            if variable_q == variable_s:
                no_of_vars_unified += 1
    if no_of_vars_unified == len(query_variables):
        return True
    else:
        return False


def isVar(elem):
    return True if re.search("^[a-z]",elem) else False


def NOT(clause):
    if len(clause) > 0:
        if clause[0] == '~':
            clause = clause.lstrip('~')
        else:
            clause = '~' + clause
    return clause

def get_query_predicate(query):
    predicate_q = ''
    i = 0
    while(query[i] != '('):
        predicate_q += query[i]
        i += 1
    predicate_q += '('
    return predicate_q

def get_positions(xs, item):
    if isinstance(xs, list):
        for i, it in enumerate(xs):
            for pos in get_positions(it, item):
                yield (i,) + pos
    elif xs == item:
        yield ()
main()