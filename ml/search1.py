from whoosh import qparser
from whoosh import scoring
from whoosh.index import open_dir
import sys
import mysql.connector
from mysql.connector import Error
ix = open_dir("indexdir")

# query_str is query string
query_str = sys.argv[1]
# Top 'n' documents as result
if (len(sys.argv) < 3):
    print('No limit given')
else:
    topN = int(sys.argv[2])
    try:
        connection = mysql.connector.connect(host='localhost',
                                         database='ml',
                                         user='root',
                                         password='root')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True, dictionary=True)
            cursor.execute("SELECT * FROM `retail`;")
            totalRecordsObj = cursor.fetchall()
            print 'Test Criteria';
            file = open('test.txt', 'a+')
            for criteriaObj in totalRecordsObj:
                print criteriaObj['sub_category']
                file.write(str(criteriaObj['sub_category']) + "\n")
                testCriteriaArray = criteriaObj['test_criteria'].strip().split(', ')
                for testCriteria in testCriteriaArray:
                    print "\t", testCriteria
                    file.write("\t" + str(testCriteria) + "\n")
                    #, "email_addr", "title", "email_from", "email_to", "id", "email_addr_full"
                    query = qparser.MultifieldParser(["content", "email_addr", "title", "email_from", "email_to", "id", "email_addr_full"], ix.schema)
                    op = qparser.OperatorsPlugin(And="&", Or="\|", Not="\~", AndNot="&!", AndMaybe="&~")
                    query.replace_plugin(op)

                    with ix.searcher(weighting=scoring.Frequency) as searcher:
                        qr = query.parse(unicode(testCriteria))
                        results = searcher.search(qr, limit=topN, terms=True)
                        if(len(results)):
                            if(topN > len(results)):
                                topN = len(results)
                            file.write("\tResult found:" + str(len(results)) + "\n")
                            #print 'Result found:', len(results)
                            #print 'Result found:', results.scored_length()
                            #print 'RRRR:', results.scored_length()
                            # print("SR.NO    ID               EMAIL FROM                EMAIL TO")
                            for i in range(topN):
                                #print "Contains:"
                                file.write("\t\tContains:\n")
                                #matched = results[i].matched_terms()
                                for t in results[i].matched_terms():
                                    #print " ", t
                                    file.write("\t\t" + str(t) + "\n")
                                #print ('%d      %s          %s     %s' %((i+1), results[i]['id'], results[i]['email_from'], results[i]['email_to']))
                                #print(results[i]['textdata'])
                        else:
                            file.write("\tNo result found\n")
                            print('No result found')

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    file.close()
