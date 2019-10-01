import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, KEYWORD
import sys
import codecs
import re
import mysql.connector
from mysql.connector import Error

RECORD_LIMIT = int(10000)

def getCleanedEmails(raw_html):
    return re.findall('[a-zA-Z0-9]\S+@\S+[a-zA-Z]', raw_html)
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6})|#[?]{1};')
  cleantext = re.sub(cleanr, ' ', raw_html)
  return cleantext

def createSearchableData():
    '''
    Schema definition: title(name of file), path(as ID),email_addr(as KEYWORD), content(indexed
    but not stored),textdata (stored text content)
    '''
    schema = Schema(title=TEXT(stored=True), email_from=TEXT(stored=True),email_to=TEXT(stored=True), email_addr=KEYWORD(stored=True, unique=True, lowercase=True), email_addr_full=KEYWORD(stored=True, unique=True, lowercase=True), id=ID(stored=True), content=TEXT, textdata=TEXT(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("../../indexdir")

    # Creating a index writer to add document as per schema
    ix = create_in("../../indexdir", schema)
    writer = ix.writer()
    try:
        connection = mysql.connector.connect(host='10.0.0.19',
                                             database='competi_competidb',
                                             user='root',
                                             password='root@20165')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True, dictionary=True)
            cursor.execute("select count(*) as total_records from cscan_email2011 c_email inner join cscan_email_text2011 text on(text.muid = c_email.muid AND text.cettype='text/html');")
            totalRecordsObj = cursor.fetchone()
            totalRecords = totalRecordsObj['total_records']
            hasQuotient = int(totalRecords)/RECORD_LIMIT
            hasRemainder = int(totalRecords) % RECORD_LIMIT
            print 'Total Records', totalRecords
            hasRemainder = 1
            remainder = 1
            if(hasRemainder==0):
                remainder = 0
            toLimit = 1#int(hasQuotient) + remainder
            print('Limits start')
            i = 1
            for t in range(toLimit):
                dataQuery = ("select c_email.muid,c_email.email_subject, c_email.email_from, c_email.email_to, text.cettext,text.cettype  from cscan_email2011 c_email inner join cscan_email_text2011 text on(text.muid = c_email.muid AND text.cettype='text/html') limit " + str(t*RECORD_LIMIT) + str(",") + str(RECORD_LIMIT) + ";")
                #print(dataQuery)
                cursor.execute(dataQuery)
                records = cursor.fetchall()
                #print(records)
                for record in records:
                    textContent = cleanhtml(record['cettext'])
                    lst = getCleanedEmails(textContent.replace("?",""))
                    lst_full = getCleanedEmails(textContent.replace("?",""))
                    subject = cleanhtml(record['email_subject']).replace("?","")
                    recordFrom = getCleanedEmails(record['email_from'])
                    recordTo = getCleanedEmails(record['email_to'])

                    if(len(recordFrom)):
                        emailFrom = recordFrom[0]
                    if(len(recordTo)):
                        emailTo = recordTo[0]
                    print(i)
                    i = i+1
                    # print(emailFrom)
                    # print(emailTo)
                    writer.add_document(title=subject,email_from=emailFrom,email_to=emailTo, email_addr=lst, email_addr_full=lst_full, id=unicode(
                        record['muid']), content=textContent, textdata=textContent)
                    #print(lst)
                    #print(lst_full)
            print('Limits end')
        print("Indexing done!")
        writer.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

createSearchableData()
