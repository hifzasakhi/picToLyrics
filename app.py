from PIL import Image
from flask import Flask, request, render_template
from jinja2 import Template, Environment, PackageLoader, select_autoescape
import io
import urllib2 as urllib2 
import urllib 
import random
import string
import pymongo
from pymongo import MongoClient


import json
from PIL import Image
import io
from urllib2 import urlopen
from PIL import Image
from cStringIO import StringIO
      


app = Flask(__name__)


@app.route("/hifza")
def helloHifza():
    return "Hello Hifza!"

@app.route('/img/<url>/',methods=['GET'])
def getImage(url):
  print(request.args)
  #fd = urllib.urlopen(url)
  #image_file = io.BytesIO(fd.read())
  #img = Image.open(image_file)
  return "cool"    
   #response = requests.get(url)
    #img = Image.open(BytesIO(response.content))
  #return img    
#height, width = img.size
    #return height, width
    #dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}



@app.route('/size',methods=['POST'])
def getSize_old():
  #url="localhost:5001/size"
  data = request.get_json()
  #print whole json payloaf
  print(data)
  #pulls the URL out of the json payload
  image_url = data['url']

  print(image_url)

  #image_byt = urlopen(image_url)

  img_file = urllib2.urlopen(image_url)
  im = StringIO(img_file.read())
  img = Image.open(im)
  #print(img.size)
  #image_b46 = base64.encodestring(image_byt)

  #img = Image.open(image_byt)
  print(height)
  img.show()
 
  return "{}\n"

def retrieveImageName(image_url):
  filename = image_url.split('/')[-1].split('.')[0]
  print("filename is: " + filename)
  return filename

def retrieveImageExtension(image_url):
  file_ext = '.'+ image_url.split('.')[-1]
  print("file_ext is: " + file_ext)
  return file_ext

def downloadImage(image_url):
  imageName = retrieveImageName(image_url) + retrieveImageExtension(image_url)
  urllib.urlretrieve(image_url, "/tmp/hifzaFlaskApp/" + retrieveImageName(image_url) + retrieveImageExtension(image_url))
  return imageName

def generateLyrics(imageName):
  lyrics = []
  for i in range(0,len(imageName)):
    lyrics.append(''.join(random.sample(string.ascii_lowercase, 5)))
  print("printing lyrics: ")  
  print(lyrics) 
  return lyrics

#this string will serve as the key in the database
def generateKeyString():
  return ''.join(random.sample(string.ascii_lowercase, 10))

def getDBConnection():
  try:

    client = MongoClient('localhost', 27017)
    db = client.SongLyrics
    return db

  except Exception, e:
    print str(e)

def insertIntoDB(key_string, lyrics_array):
  try:

    db = getDBConnection()
    db.SongLyrics.insert_one(
      {
        "key": key_string,
        "lyrics": lyrics_array
      })

  except Exception, e:
    print str(e)

def fetchLyricsFromDB(key_string):
  
  db = getDBConnection()
  lyrics_db = db.SongLyrics

  #gets the lyrics associated with this particular key
  lyrics_array = lyrics_db.find_one({"key": key_string}, {"lyrics":1})

  return lyrics_array

@app.route('/temp',methods=['POST'])
def renderTemplate(lyrics_array):

  return render_template("template.html", lyrics=lyrics_array)

@app.route('/facebook',methods=['POST'])
def facebook():
  #url="localhost:5001/size"
  data = request.get_json()
  #print whole json payload
  print(data)
  #pulls the URL out of the json payload
  image_url = data['entry'][0]['message']['attachments'][0]['payload']['url']

  print(image_url)

  imageName = downloadImage(image_url)
  #urllib.urlretrieve(image_url, "/tmp/hifzaFlaskApp/" + retrieveImageName(image_url) + retrieveImageExtension(image_url))

  lyrics = generateLyrics(imageName)

  key_string = generateKeyString()

  #db = getDBConnection()

  insertIntoDB(key_string, lyrics)

  print("Getting lyrics from db")
  lyrics_array_from_db = fetchLyricsFromDB(key_string)
  print("Lyrics from db are: ")
  print(lyrics_array_from_db)

  renderTemplate(lyrics_array_from_db)

  return ("",200)


  #image_byt = urlopen(image_url)

  # img_file = urllib.urlopen(image_url)
  # im = StringIO(img_file.read())
  # img = Image.open(im)
  # #print(img.size)
  # #image_b64 = base64.encodestring(image_byt)

  # #img = Image.open(image_byt)
  # print(height)
  # img.show()
 
  #return image_url


  #return 200 OK

@app.route('/sizer',methods=['POST'])
def getSize():
  print("Hello")


#
if __name__ == "__main__":
  app.run(port=8000)
