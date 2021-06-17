#!/usr/bin/env python
# coding: utf-8

# In[68]:


import sys
import requests
from bs4 import BeautifulSoup,NavigableString
from selenium import webdriver


# In[143]:


"""Připojí se na https://www.cts-tradeit.cz/kariera/ """

res = requests.get("https://www.cts-tradeit.cz/kariera/") #(sys.argv[-1])
soup = BeautifulSoup(res.text, "html.parser")

"""Aktuálně hledané pozice."""

jobNames = []
for link in soup.find_all("a", class_= "card card-lg card-link-bottom"):
    jobNames.append(str(link['href']).split("/")[2])


# In[193]:


"""Pro každou nabízenou pozici proklikem zjistí obsah sekce  „Co Tě u nás čeká“. """

driver = webdriver.Chrome('J:/chromedriver.exe')
res = requests.get(sys.argv[-1])

for job in jobNames:
    
    # Prokliky
    url = "https://www.cts-tradeit.cz/kariera/{}".format(job)
    driver.get(url)
    res = requests.get("https://www.cts-tradeit.cz/kariera/{}".format(job))
    soup = BeautifulSoup(res.text, "html.parser")

    paragraphs = soup.find_all("p")
    maintextList = []
    checkList = []
    
    for paragraph in paragraphs:
        for element in paragraph:
            maintextList.append(element)

    """Zjištěná data zapíše do souborů v aktuálním adresáři. Název souboru bude odpovídat  masce  „{název  pozice}.txt”.  
    Obsah  souboru  bude neformátovaný  text  sekce „Co  Tě  u  nás  čeká“. """

    path = "J:/{}.txt".format(job)
    file = open(path,"a")
    
    # Html odkazu na DevOps Engineer - Junior/Medior se liší od html ostatních nabízených pozic, proto ta podmínka.
    if job == jobNames[2]:
        # Před uložením do souboru, se zbavíme se všech tagů <span>...</li> 
        maintext = str(maintextList[3]).replace('<span>', '',).replace('</span>', '',)
        file.write("{}\n".format(maintext))
        
        for ultag in soup.find_all('ul', {'class': 'list-check'}):
            checkList.append(ultag)
        for litag in checkList[0].find_all('li'):
            checks = str(litag).replace("<li>", "").replace("</li>", "").replace("<span>", "").replace("</span>", "")
            file.write("{}\n".format(checks))
    else:
        maintext = str(maintextList[2]).replace('<span>', '',).replace('</span>', '',)
        file.write("{}\n".format(maintext))
        
        for ultag in soup.find_all('ul', {'class': 'list-check'}):
            checkList.append(ultag)
        for litag in checkList[0].find_all('li'):
            checks = str(litag).replace("<li>", "").replace("</li>", "").replace("<span>", "").replace("</span>", "")
            file.write("{}\n".format(checks))
        
file.close()


# In[ ]:




