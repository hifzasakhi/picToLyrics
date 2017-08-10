from PIL import Image
from flask import Flask, request
import io
import urllib2 as urllib 
import json
from PIL import Image
import io
from urllib2 import urlopen
from PIL import Image
from cStringIO import StringIO
      


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

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

  img_file = urllib.urlopen(image_url)
  im = StringIO(img_file.read())
  img = Image.open(im)
  #print(img.size)
  #image_b46 = base64.encodestring(image_byt)

  #img = Image.open(image_byt)
  print(height)
  img.show()
 
  return "{}\n"

@app.route('/facebook',methods=['POST'])
def facebook():
  #url="localhost:5001/size"
  data = request.get_json()
  #print whole json payloaf
  print(data)
  #pulls the URL out of the json payload
  image_url = data['entry'][0]['message']['attachments'][0]['payload']['url']

  print(image_url)

  #image_byt = urlopen(image_url)

  # img_file = urllib.urlopen(image_url)
  # im = StringIO(img_file.read())
  # img = Image.open(im)
  # #print(img.size)
  # #image_b64 = base64.encodestring(image_byt)

  # #img = Image.open(image_byt)
  # print(height)
  # img.show()
 
  return image_url

@app.route('/sizer',methods=['POST'])
def getSize():
  print("Hello")


#
if __name__ == "__main__":
  app.run(port=8000)
