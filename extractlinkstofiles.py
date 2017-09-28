#This program retreives and saves all the class html webpages to disk.
#The file name is class<num>.html

import urllib
from BeautifulSoup import BeautifulSoup

#first link that needs to be entered so that the all other class links can be retreived for that year
urllib.urlretrieve('http://web2.wipo.int/classifications/nice/nicepub/en/fr/edition-20170101/taxonomy/class-1','nice_page.html')

nice_page = open('nice_page.html','r')
page_soup = BeautifulSoup(nice_page)
link_list = list()

#clean_link function takes text and cleans it
#and adds prefix to it so that the webpage is complete
def clean_link(old_link):
    #"javascript:load_tab_content('/classifications/nice/nicepub/en/fr/edition-20170101/taxonomy/class-35/')
    #extract only the link from the above text
##    pos1 = old_link.find("'")
##    pos2 = old_link.find("'",pos1+1)
##    print pos1, pos2
##    new_link = old_link[pos1+1:pos2]
    #add "web2.wipo.int" to the link to create the new_link
    new_link = "http://web2.wipo.int" + old_link
    #print new_link
    return new_link

#td is for goods and services.
tags = page_soup('td')

#the links for each class is saved in link_list
for tag in tags:
 #   class_num = tag.text
    findA = tag.find('a')
    #print findA
    if findA is not None:
        href = findA.get('href',None)
        #print href
        link_list.append(clean_link(href))


count = 1

for link in link_list:
    filename = "class" + str(count) + ".html"
    page = urllib.urlretrieve(link,filename)
    count = count + 1
    
    
