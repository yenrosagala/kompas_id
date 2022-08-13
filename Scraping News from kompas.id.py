#!/usr/bin/env python
# coding: utf-8

# # SCRAPING BERITA DARI KOMPAS.ID

# In[46]:


import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# # Konten yang dicari

# In[47]:


Options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
input_user =input('nyari berita apa?" ')
DRIVER_PATH = 'C:\SeleniumWebDriver\chromedriver.exe' #ganti dengan path ke chromedriver
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
doc = driver.get(f'https://www.kompas.id/label/{input_user}')


# In[48]:


#load more
for i in range(10):
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[5]/div/div/div[1]/div[2]/button'))).click()
    except:
        pass


# Untuk memperoleh link berita dan judul berita

# In[49]:


links = []
titles = []
news=driver.find_elements(By.TAG_NAME, 'h4')
for new in news[1:]:
    sumber=new.find_element(By.XPATH,'./..').get_attribute('href')
    link=f"{sumber}"
    
    if sumber is None:
        pass
    else:
        links.append(link)
        titles.append(new.text)
        
driver.quit()


# #memperoleh isi konten, dengan menggunakan link berita

# In[51]:


import requests
link_gambar = []
muatan = []
link_berita = []
count = 0
for link in links:
    count +=1
    try: 
        response = requests.get(f'{link}').text
        link_berita.append(link)
        soup = BeautifulSoup(response,'html.parser')
        content=soup.find(class_='content')
        image=content.find('img')['src']
        link_gambar.append(image)
        tekss = content.find_all('p')
        isi = []
        for teks in tekss:
            isi.append(teks.text)
        muatan.append(isi)
            
    except:
        pass
print(f'jumlah berita sebanyak {count}')  
df_berita =pd.DataFrame(list(zip(link_berita,link_gambar,titles, muatan)), columns=['Link Berita', 'Link Gambar','Judul', 'Isi Berita'])
df_berita.to_csv(f'Judul dan isi berita_tentang_{input_user}.csv')


# Membuat wordclout dari isi berita

# In[52]:


from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
 
comment_words = ''
stopwords = set(STOPWORDS)
 
# iterate through the csv file
for val in muatan:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 1080, height = 1080,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()

