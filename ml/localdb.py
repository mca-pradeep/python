import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, KEYWORD
import sys
import codecs
import re
import mysql.connector
from mysql.connector import Error

RECORD_LIMIT = int(10000)
def removeQuotes(oldStr):
    return oldStr.replace('\"', '').lower()
def getCleanedEmails(raw_html):
    return re.findall('[a-zA-Z0-9]*\S*@\S+[a-zA-Z]', raw_html)
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6})|#[?]{1};')
  cleantext = re.sub(cleanr, ' ', raw_html)
  return cleantext

def createSearchableData():
    '''
    Schema definition: title(name of file), path(as ID),email_addr(as KEYWORD), content(indexed
    but not stored),textdata (stored text content)
    '''
    #schema = Schema(title=TEXT(stored=True), email_from=TEXT(stored=True),email_to=TEXT(stored=True), email_addr=KEYWORD(stored=True, unique=True, lowercase=True), email_addr_full=KEYWORD(stored=True, unique=True, lowercase=True), id=ID(stored=True), content=TEXT, textdata=TEXT(stored=True))
    #if not os.path.exists("indexdir"):
    #    os.mkdir("indexdir")

    # Creating a index writer to add document as per schema
    #ix = create_in("indexdir", schema)
    #writer = ix.writer()
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='ml',
                                             user='root',
                                             password='root')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True, dictionary=True)
            dataQuery = ("select id, sub_category, criteria from retail;")
            cursor.execute(dataQuery)
            records = cursor.fetchall()
            #print(records)
            for record in records:
                cleanedCriteria = getCleanedEmails(removeQuotes(record['criteria']))
                testCriteria = str(', ').join(cleanedCriteria)
                print record['id'], record['sub_category']
                #print testCriteria
                testQ = 'update retail set test_criteria=\'' + str(testCriteria) + '\' where id=' + str(record['id']) + ';'
                #print testQ
                cursor.execute(testQ)
                connection.commit()
                # print(emailFrom)
                # print(emailTo)
                #writer.add_document(title=subject,email_from=emailFrom,email_to=emailTo, email_addr=lst, email_addr_full=lst_full, id=unicode(
                #    record['muid']), content=textContent, textdata=textContent)
                #print(lst)
                #print(lst_full)
            print('Limits end')
        print("Indexing done!")
        #writer.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

createSearchableData()
