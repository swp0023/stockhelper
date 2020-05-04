from flask import Flask, render_template
app = Flask(__name__, static_url_path='')
 
@app.route('/')
def index():
  return render_template('/login.html')


@app.route('/dashboard')
def dashborad():
  return render_template('/index.html')


if __name__ == '__main__':
  app.run('0.0.0.0', port=5000)
