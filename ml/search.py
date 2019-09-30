from whoosh import qparser
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
    #, "email_addr", "title", "email_from", "email_to", "id", "email_addr_full"
    query = qparser.MultifieldParser(["content"], ix.schema)
    op = qparser.OperatorsPlugin(And="&", Or="\|", Not="\~", AndNot="&!", AndMaybe="&~")
    query.replace_plugin(op)
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        qr = query.parse(unicode(query_str))
        results = searcher.search(qr, limit=topN, terms=True)
        if(len(results)):
            if(topN > len(results)):
                topN = len(results)
            print 'Result found:', len(results)
            #print 'Result found:', results.scored_length()
            print 'RRRR:', results.scored_length()
            print("SR.NO    ID               EMAIL FROM                EMAIL TO")
            for i in range(topN):
                print "Contains:"
                #matched = results[i].matched_terms()
                for t in results[i].matched_terms():
                    print " ", t
                print ('%d      %s          %s     %s' %((i+1), results[i]['id'], results[i]['email_from'], results[i]['email_to']))
                print(results[i]['textdata'])
        else:
            print('No result found')
