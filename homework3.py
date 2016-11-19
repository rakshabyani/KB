import lex

def main():
    file = open("input.txt","r")

    no_of_queries = file.readline().strip()
    queries_list = []
    for i in range(int(no_of_queries)):
        temp = file.readline().replace("\s+","").strip('\n')
        queries_list.append(lex.parser.parse(temp))
    print(queries_list)

    no_of_sentences_KB = file.readline().strip()
    KB = []
    for n in range(int(no_of_sentences_KB)):
        temp = file.readline().replace("\s+", "").strip('\n')
        KB.append(lex.parser.parse(temp))
    # n = file.readline().strip()
    # mode = file.readline().strip()
    # globalplayer = file.readline().strip()
    # cutting_depth = file.readline().strip()
    # cell_values = []
    #
    # boardState = []
    # cell_valuesRow = []
    # boardStateRow = []
    #
    # for i in range(int(n)):
    #     cell_valuesRow = file.readline().split()
    #     cell_values.append(cell_valuesRow)

    output = open("output.txt","w")

main()