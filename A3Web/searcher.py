import sys
from nltk.stem import PorterStemmer
import time

global positions
global indices

def search(queries):
    documents = dict()
    with open("index.txt",'r') as index:
        for query in queries:
            try:
                index.seek(indices[query])
            except KeyError:
                print("No such token: " + query)
                #Do something
                break
            entry = eval(index.readline())
            #print(entry)
            documents[entry[0]] = entry[1]
        #print(index.readline())
    '''for query in queries:
       # print(f"Searching {query}", time.time())
        with open(f"index-{query[0]}.txt", 'r') as index:
            while True:
                entry = index.readline()
                if not entry:
                    print("Query word missing.")
                    #do something here
                    break
                entry = eval(entry)
                if entry[0] == query:
                    documents[entry[0]] = entry[1]
                    break'''
    result = []
    #print("Before combine", time.time())
    for doc in documents.values():
        result.append(list(doc.items()))
    result = sorted(result, key=lambda x: len(x[1]))
    while len(result) > 1:
        tmp = []
        ycount = 0
        for x in result[0]:
            while ycount < len(result[1]) and result[1][ycount][0] <= x[0]:
                if x[0] == result[1][ycount][0]:
                    tmp.append((x[0], 0.5*(x[1]+result[1][ycount][1])))
                ycount += 1


        #Use two pointer method to compare entries?
        #for x in result[0]:
         #   for y in result[1]:
          #      if x[0] == y[0]:
           #         tmp.append((x[0], 0.5*(x[1]+y[1])))
        result[0] = tmp
        result.pop(1)
    #return sorted(result[0], key=lambda x: -x[1])
    #print("After combine", time.time())
    return result[0]

def translate(documents):
    count = 0
    trans = set()
    with open("doc_ids.txt", 'r') as ids:
        for doc in documents:
            ids.seek(positions[doc[0]])
            line = ids.readline()
            if '#' in line:
                line = line.split('#')[0]
            #if line not in [entry[0] for entry in trans]:
            trans.add((line.rstrip(), doc[1]))
                #print(trans)
    return trans
    #with open("doc_ids.txt", 'r') as ids:
     #   for i, line in enumerate(ids):
      #      if i == documents[count][0]:
       #         if '#' in line:
        #            line = line.split("#")[0]
         #       if line not in [entry[0] for entry in trans]:
          #          trans.append((line.rstrip(), documents[count][1]))
           #     #documents[count] = (line.rstrip(),documents[count][1])
            #    count += 1
            #if count == len(documents):
               # print("before sort", time.time())
             #   return trans
                #return documents




def main(user_search:str):
    global positions
    global indices
    with open("doc_pos.txt", 'r') as pos:
        positions = eval(pos.read().rstrip())
    with open("ind_pos.txt", 'r') as ind_pos:
        indices = eval(ind_pos.read().rstrip())
    #print("at start,", time.time())
    print("A3 Search Engine\n(enter 'q' to exit the program)\n")
    stemmer = PorterStemmer()
    
    user_inp = user_search
    # user_inp = input("Enter search: ")

    tokens = [stemmer.stem(query.lower()) for query in user_inp.split()]
    tokens = [token for token in tokens if len(token)>1]
    if len(tokens) != 0:
        #check if tokens is empty
        #Ignore one character query terms
        #What if only one characters -> empty string -> handle
        print("before search,", time.time())
        documents = search(tokens)
        print("after search,", time.time())
        documents = sorted(documents, key=lambda x: -x[1])[:10]
        #print(documents)
        #print(documents)
        #print(len(documents))
        #can be one or more queries - need to AND them (find multiple tokens and return their shared documents)
        #print(tr)
        translated = sorted(translate(documents),key=lambda x: -x[1])
        #print(translated)

        print("after translate,",time.time())
        #print("done translate:", time.time())
        print(f'Results for "{user_inp}":')
        if len(translated) > 4:
            for url in translated[:5]:
                print(url[0])
        else:
            for url in translated:
                print(url[0])
        return translated

        
    
        #print("complete:", time.time())
        #translate document number to url using doc_ids.txt
        #get search time <300ms somehow
            # maybe keep in indexer.py, when splitting index into ranges, keep track of number of lines in each file
            # then in searcher when opening the split index, use the length to do a binary search rather than iterate
            # also, for translate need to cut down
        #FOR M2:Add text interface

        #Questions to ask TA:
            #how many results to output - choose however many we want
            #what is a considered a database
            #what are we doing wrong
            #are we allowed to load each index range fully -- binary search maybe, send an email to Jina to ask about the grading rubric??
                #if not binary search, then need to keep track of position of each token through auxiliary file
                #load that fully into memory and read it to get the position, then seek(position)
                #use tell() to find current file position?
                #do the same for docids?
            #can we load in docids.txt fully
            #can we import tf-idf from sklearn -- yes
            #FOR M2:do we need to account for query errors -- only empty strings
            #also filter # from urls

        #also need to rank urls by average of tf-idf for each query word with weighting for importance
        #make a function in indexer that goes through index presplit and updates using total number of docs and len of each token's posting
        #or do it in split actually? that might work better
            #before writing, eval the line and use the tf to calc tf-idf, then replace tf with that
            #then write
    return


if __name__ == "__main__":
    main()
