#for each class extract the details of class, goods and services
import sqlite3
import urllib
import re

from BeautifulSoup import BeautifulSoup

conn = sqlite3.connect('nice2017.db')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS class;
DROP TABLE IF EXISTS goods;

CREATE TABLE class(
    class_number TEXT,
    class_description TEXT,
    class_expnote_desc TEXT,
    class_expnote_includes TEXT,
    class_expnote_excludes TEXT,
    class_good_service TEXT 
    );

CREATE TABLE goods(
    class_number TEXT,
    basic_number INTEGER PRIMARY KEY,
    goods_desc TEXT,
    indication_gos TEXT
    );

''')

#link_list will contain all the html files of classes
link_list = list()
empty_string = ""

#save class html file names to link_list
for i in range(45):
    filename = "class" + str(i+1)+".html"
    link_list.append(filename)

#extracting information and transforming the information process
count =1

for link in link_list:
    class_page = open(link,'r')
    class_soup = BeautifulSoup(class_page)
    
    #class number
 #  class_tags = class_soup.h1
    class_heading = "class_heading_"+str(count)
    class_tags = class_soup.find("h1",{'id' : class_heading})
    if class_tags.contents[-1] is None:
        continue
    class_num = class_tags.contents[-1]
   # print 'class',class_num
    class_num = class_num.strip()
    class_num = class_num.split()
    class_no = class_num[-1]
    print class_no
 
    #class description
    class_tags = class_soup.find("div",{'class' : "class_heading" })
    if class_tags.contents[-1] is not None:
        class_desc = class_tags.contents[-1]
        print class_desc
    else:
        class_desc = empty_string

    #class_explanatory notes
    exp_note_tag =class_soup.find("div",{'class' : "explanatory_note" })
    if exp_note_tag.p.label is not None:
        class_expnote = exp_note_tag.p.label.string
        print class_expnote
    else:
        class_expnote = empty_string

    #class_explanatory notes includes
    class_includes = ""
    includes_tag = exp_note_tag.div
    if includes_tag is not None:
        for i in range(len(includes_tag.contents)):
             if i == 0:
                class_includes = includes_tag.contents[i].strip()
                
                print class_includes



             table_tag = class_soup.find(("div"),{'class':"ui-datatable-tablewrapper"}).table

             table_rows = table_tag.tbody

             for tr in table_rows.contents:
                 for td in tr.contents:
                     for label in td.contents:
                         class_includes = class_includes + " " + label.string

             break;# break is for i in range(len(class_tags.contents))
##
##    #class explanatory notes excludes
    class_excludes = ""
    excludes_tag = class_soup.find(("div"),{'id':"j_idt642:0:j_idt644:0:j_idt711"})
    if excludes_tag is not None:
        for i in range(len(excludes_tag.contents)):
            class_excludes = "This class does not include, in particular:"
##
##
            table_tag = excludes_tag.table
##
            table_rows = table_tag.tbody
##
            for tr in table_rows.contents:
                for td in tr.contents:
                    for label in td.contents:
                        pass
        
    if count>=1 and count <=34:
        goodService = 'good'
    else:
        if count >=35 and count<=45:
            goodService = 'service'
    #loading the extracted and transformed information into database.
 #   add_class = ("INSERT INTO class VALUES (?,?,?,?,?,?);")
    data_class = (class_no, class_desc,class_expnote,class_includes,class_excludes,goodService)
    cur.execute('''INSERT INTO class VALUES(?,?,?,?,?,?) ''', data_class)
    print "insert executed"
    conn.commit()
    #basic num and text retreival
    class_tags = class_soup.find('ul', {'class':'indication_container'})
    if class_tags is not None:
        cnt = 1
        for i in class_tags.contents:
            li= (i.nextSibling)
            if li.nextSibling is None:
                continue
            if li.findNext('div') is None:
                continue
            lis = li.findNext('div')
        
            basic_num = lis.text
            lis1 = lis.findNext('div')
            basic_text = lis1.text
          
            if cnt > 2:
                break
            cnt = cnt +1
##    if count > 1:
##                break
    count = count +1
            

    

