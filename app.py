from PIL import Image
from flask import Flask, request
import io
import urllib2 as urllib 
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/hifza")
def helloHifza():
    return "Hello Hifza!"

@app.route('/img/<url>/',methods=['GET'])
def getImage(url):
  print url
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
def getSize():
  #url="localhost:5001/size"
  data = request.get_json()
  #print json
  print(data)
  #print(data[0])
  # r = requests.get('http://httpbin.org/get')  #r = requests.get(url, headers=my_headers, params=payload)
  return "{}\n"

if __name__ == "__main__":
    app.run(port=5001)
