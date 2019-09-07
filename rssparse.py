'''
Created on Aug 21, 2019

@author: Waiwai Kim
'''
import os, time, threading, random
import feedparser
from PIL import Image, ImageFont, ImageDraw
from random import shuffle

items = [] 
displayItems=[]
feeds = [
    #"https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "https://www.economist.com/science-and-technology/rss.xml"     
    ]
    
def populate_items():
    del items[:]
    del displayItems[:]
    os.system("find . -name \*.ppm -delete")
    
    for url in feeds:
        feed = feedparser.parse(url)
        posts = feed["items"]
    
        for post in posts:
            items.append(post)
        
    shuffle(items)
    
    
def createLinks():
    try:
        populate_items()
        for idx, item in enumerate(items):
            pass
            writeImage(str(item["title"]), idx)
    except ValueError:
        print("Error: sorry! I couldn't make links :(")
    finally: 
        print("\nWill get more news in 30 minutes! \n")
        
def colorRed():
    return (255, 0 , 0)
def colorGreen():
    return (0, 255, 0)
def colorBlue():
    return (0, 0, 255)
def colorRandom():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def colorize(index):
    if index%3 == 0:
        return colorRed()
    elif index%3 == 1:
        return colorGreen()
    elif index%3 ==2:
        return colorBlue()
    else:
        colorRandom()

def run():
    print("News Fetched at {}\n".format(time.ctime()))
    createLinks()
    threading.Timer(len(items)+60, run).start()
    showOnLEDDisplay()
    
def showOnLEDDisplay():
    for disp in displayItems[:60]:
        os.system("sudo ./led-matrix -r 16 -c 3 -t 60 -m 25 -D 1 "+disp) \

def writeImage(url, count):  
    bitIndex = 0 
    link, headLine = url[0], url[:]
    
    text = ((headLine, colorize(count)),  (link,colorRandom()))
    font = ImageFont.truetype('arial.ttf', 16,)
    all_text =""
    for text_color_pair in text:
        t = text_color_pair[0]
        all_text = all_text + t 
        #print(all_text) 
        
    width, ignore = font.getsize(all_text) 
    im = Image.new("RGB", (width+30,16), "black")
    #creates a new image 
    draw = ImageDraw.Draw(im)      
     
    x=0
    for text_color_pair in text:
        t=text_color_pair[0]
        c=text_color_pair[1]
        draw.text((x,0),t,c, font=font)
        x = x + font.getsize(t)[0]
    
    filename= str(count)+".ppm"
    displayItems.append(filename)
    im.save(filename)    
    
if __name__ == '__main__':
    
    run()
    