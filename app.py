from flask import Flask
app = Flask(__name__)
 
@app.route('/')
def hello_world():
  return '주말 잘 보내세요\n우혁프로님, 남기경 대리님, 오건철 대리님'
 
@app.route('/admin')
def adminPage():
  return "Out!!!!"

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000)
