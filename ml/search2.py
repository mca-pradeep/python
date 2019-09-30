from whoosh import qparser
from whoosh import scoring
from whoosh.index import open_dir
from whoosh.query import *
import sys

ix = open_dir("indexdir")

# def hasAndOrString(userString):
#     flag = False
#     if(userString.index(' OR ') != -1):
#         flag = True
#     elif(userString.index(' AND ') != -1):
#         flag = True
#     return flag
# print hasAndOrString('test this ')
query = qparser.QueryParser("content", ix.schema)
op = qparser.OperatorsPlugin(And="&", Or="\|", Not="\~", AndNot="&!", AndMaybe="&~")
query.replace_plugin(op)
qr = query.parse(unicode(sys.argv[1]))
print qr
# def setUserQuery(userString):
#     updatedUserString = {'AND':[], 'OR':[], 'TEST':[]}
#     for condition in updatedUserString:
#         updatedUserString[condition] = userString.split(condition)
#     conditionCase = 'AND'
#     userStringArray = []
#     if len(updatedUserString[conditionCase]) > 1:
#         userStringArray = updatedUserString[conditionCase]
#     else:
#         conditionCase = 'OR'
#         if len(updatedUserString[conditionCase]) > 1:
#             userStringArray = updatedUserString[conditionCase]
#         else:
#             conditionCase = 'TEST'
#         userStringArray = userString
#     if conditionCase != 'TEST':
#         conditionCheck = 'OR'
#         if conditionCase == 'OR':
#             conditionCheck = 'AND'
#         setp1UserStringArray = []
#         setp2UserStringArray = []
#         for orStr in userStringArray:
#             uStringArr = orStr.strip()
#             step2UserQueryArray = uStringArr.split(conditionCheck)
#             for step2UserQuery in step2UserQueryArray:
#                 contentStringArray = step2UserQuery.strip().split(':')
#                 #contentStringArray[1] = unicode(contentStringArray[1])
#                 setp1UserStringArray.append(Term(contentStringArray[0], contentStringArray[1]))
#             setp2UserStringArray.append(setp1UserStringArray)
#             setp1UserStringArray = []
#             mergeSetp2Array = []
#             if(conditionCheck == 'OR'):
#                 for mergeSetp2 in setp2UserStringArray:
#                     mergeSetp2Array.append(Or(mergeSetp2))
#             else:
#                 for mergeSetp2 in setp2UserStringArray:
#                     mergeSetp2Array.append(And(mergeSetp2))
#         mergeSetp1Array = []
#         if(conditionCase == 'OR'):
#             mergeSetp1Array.append(Or(mergeSetp2Array))
#         else:
#             mergeSetp1Array.append(And(mergeSetp2Array))
#         updatedUserString = mergeSetp1Array
#     else:
#         #check for :
#         userStringTest = userStringArray.strip().split(':')
#         if(len(userStringTest) > 1):
#             updatedUserString = Term(userStringTest[0].strip(), unicode(userStringTest[1]))
#         else:
#             updatedUserString = Term('content', unicode(userStringArray.strip()))
#     return updatedUserString
# q = setUserQuery('content:test OR email_addr:test AND id:12345 OR email_to:test2 string')
# print q
# query = QueryParser("content", ix.schema)
# qr = query.parse(q)
# print qr
# with ix.searcher(weighting=scoring.Frequency) as searcher:
#     results = searcher.search(q, limit=10)
#     print results
# query_str is query string
# query_str = sys.argv[1]
# # Top 'n' documents as result
# if (len(sys.argv) < 3):
#     print('No limit given')
# else:
#     topN = int(sys.argv[2])
#     query = QueryParser("content", ix.schema)
#     print query.parse(query_str)
#     searchText = "content:"+str(query_str) + " OR email_addr:" + \
#         str(query_str) + " OR email_addr_full:" + str(query_str) +\
#         " OR title:" + str(query_str) +\
#         " OR email_from:" + str(query_str) +\
#         " OR email_to:" + str(query_str) +\
#         " OR id:" + str(query_str)
#     with ix.searcher(weighting=scoring.Frequency) as searcher:
#         qr = query.parse(unicode(searchText))
#         results = searcher.search(qr, limit=topN)
#         if(len(results)):
#             if(topN > len(results)):
#                 topN = len(results)
#             print('Result found:' + str(len(results)))
#             print("SR.NO    ID               EMAIL FROM                EMAIL TO")
#             for i in range(topN):
#                 print ('%d      %s          %s     %s' %((i+1), results[i]['id'], results[i]['email_from'], results[i]['email_to']))
#                 #print(results[i]['textdata'])
#         else:
#             print('No result found')
