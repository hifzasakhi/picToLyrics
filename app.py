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
db = None

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
    db.SongLyrics.insert_one(
      {
        "key": key_string,
        "lyrics": lyrics_array
      })

  except Exception, e:
    print str(e)

def fetchLyricsFromDB(key_string):
  lyrics_db = db.SongLyrics

  #gets the dictionary associated with this particular key
  lyrics_array = lyrics_db.find_one({"key": key_string}, {"lyrics":1})
  
  #drill down into only the lyrics portion of the dictionary 
  return lyrics_array['lyrics']

def renderTemplate(lyrics_array):
  print("Rendering lyrics template")
  return render_template("template.html",lyrics=lyrics_array)

def renderErrorTemplate():
  print("Rendering error template")
  return render_template("error.html")

@app.route('/facebook',methods=['POST'])
def facebook():

  data = request.get_json()
  if data == None:
    return renderTemplate(None)

  image_url = None
  if data != None: 
    #print whole json payload if present
    print(data)
    #pulls the URL out of the json payload
    image_url = data['entry'][0]['message']['attachments'][0]['payload']['url']
    print(image_url)

  imageName = None
  if image_url != None:   
    imageName = downloadImage(image_url)

  lyrics = None
  key_string = None
  if imageName != None:
    lyrics = generateLyrics(imageName)
    key_string = generateKeyString()
    print(key_string)

  if key_string != None:
    insertIntoDB(key_string, lyrics)

  return ("",200)

@app.route('/lyrics/<pageid>',methods=['GET'])
def getPage(pageid=None):
  print("Getting lyrics from db")
  lyrics = fetchLyricsFromDB(pageid)

  if lyrics != None: 
    print("Lyrics from db are: ")
    print(lyrics)
    return renderTemplate(lyrics)
  else:
    return renderErrorTemplate()

if __name__ == "__main__":
  db = getDBConnection()
  app.run(port=8000,debug=True)
