from flask import Flask, render_template, request, url_for
from wordcloud import WordCloud
from konlpy.tag import Komoran
import os
app = Flask(__name__)

@app.route('/')
def render_file():
   return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save('./uploaded.txt')
      global t_file
      t_file = f.filename
      try:
         kkt_gen()
      except:
         return render_template('failed.html')
      return render_template('result.html')
      

def kkt_gen():
   cleaned = ""
   with open('uploaded.txt', "r", encoding="utf-8") as file:
      f_read = file.readlines()
      for loop in f_read:
         if '] [' in loop:
               cleaned = cleaned + loop.split('] ')[2].replace('이모티콘\n','').replace('사진\n','')

   font_path = 'templates/font.ttf'

   wc = WordCloud(font_path=font_path, background_color="white")
   wc.generate(cleaned)
   wc.to_file("static/img/result.png")
   return render_template('result.html', image_file='img/result.png')



if __name__ == '__main__':
   app.run(debug = True)
