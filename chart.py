from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

opt = Options() 
opt.add_argument("--headless") #this one for not open browser
#opt.add_argument('--disable-popup-blocking')
opt.binary_location = r'C:\Users\Admin\chrome.exe' #path to chrome.exe
path = 'C:/Users/Admin/chromedriver.exe' #path to chromedriver.exe
driver = webdriver.Chrome(executable_path= path, options = opt)
driver.get("https://www.instiz.net/spage/8")
print(driver.title)
iframes = driver.find_elements_by_tag_name('iframe')
driver.switch_to.frame(iframes[0])
iframe = driver.find_element_by_xpath('//*[@id="content"]')
driver.switch_to.frame(iframe)
iframe = driver.find_element_by_xpath('//*[@id="score"]')
driver.switch_to.frame(iframe)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
names = []
songs = []
albums = []
companies = []

first = soup.find('div', attrs={'id':'score_1st'})
name_1st = first.find('div', attrs={'class':'ichart_score_artist1'})
song_1st = first.find('div', attrs={'class':'ichart_score_song1'})
album_1st = first.find('div', attrs={'class':'ichart_score_song2'})
company_1st = first.find('div', attrs={'class':'ichart_score_artist2'})
names.append(name_1st.text)
songs.append(song_1st.text)
albums.append(album_1st.text)
companies.append(company_1st.text)

for element in soup.findAll('div', attrs={'class':'spage_score_item'}):
	name = element.find('div', attrs={'class':'ichart_score2_artist1'})
	song = element.find('div', attrs={'class':'ichart_score2_song1'})
	album = element.find('div', attrs={'class':'ichart_score2_song2'})
	company = element.find('div', attrs={'class':'ichart_score2_artist2'})
	names.append(name.text)
	songs.append(song.text)
	albums.append(album.text)
	companies.append(company.text)
time = soup.select_one('#content > div.ichart_score_title > div.ichart_score_title_right.minitext3')
time = time.string.split()
date = time[0]
clock = time[1]
print('Date: {} \nTime: {}'.format(date, clock))
df = pd.DataFrame({'Artist Name':names,'Song':songs,'Album':albums, 'Company': companies})
df.to_csv("Chart.csv", index=False, encoding='utf_8_sig')
print('done')

