from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
import sys

ix = open_dir("indexdir")

# query_str is query string
query_str = sys.argv[1]
# Top 'n' documents as result
if (len(sys.argv) < 3):
    print('No limit given')
else:
    topN = int(sys.argv[2])
    query = QueryParser("content", ix.schema)
    searchText = "content:"+str(query_str) + " OR email_addr:" + \
        str(query_str) + " OR email_addr_full:" + str(query_str)
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        qr = query.parse(unicode(searchText))
        results = searcher.search(qr, limit=topN)
        if(len(results)):
            if(topN > len(results)):
                topN = len(results)
            print('Result found:' + str(len(results)))
            for i in range(topN):
                print(str(i+1) + ' ' + results[i]['title'].encode(
                    'ascii', 'ignore') + ' ' + str(results[i].score))
                print(results[i]['textdata'])
        else:
            print('No result found')
