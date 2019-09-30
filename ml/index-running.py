import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, KEYWORD
import sys
import codecs
import re


def createSearchableData(root):
    '''
    Schema definition: title(name of file), path(as ID),email_addr(as KEYWORD), content(indexed
    but not stored),textdata (stored text content)
    '''
    #email_addr=KEYWORD(stored=True, unique=True,lowercase=True),
    schema = Schema(title=TEXT(stored=True), email_addr=KEYWORD(stored=True, unique=True,
                                                                lowercase=True), email_addr_full=KEYWORD(stored=True, unique=True,
                                                                                                         lowercase=True), path=ID(stored=True), content=TEXT, textdata=TEXT(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    # Creating a index writer to add document as per schema
    ix = create_in("indexdir", schema)
    writer = ix.writer()

    filepaths = [os.path.join(root, i) for i in os.listdir(root)]
    for path in filepaths:
        #fp = open(path,'r')
        print(path)
        with codecs.open(path, 'r', encoding='utf8') as fp:
                # print(text)
            text = fp.read()
            fp.close()
        lst = re.findall('@\S+\.\S+', text)
        lst_full = re.findall('\S\.@\S+\.\S+', text)
        print(lst)
        print(lst_full)
        # print(path.split("/")[1])
        ttext = path.split("/")[1]
        # email_addr=lst,
        writer.add_document(title=unicode(ttext), email_addr=lst, email_addr_full=lst_full, path=unicode(
            path), content=text, textdata=text)
    writer.commit()


root = "corpus"

createSearchableData(root)
