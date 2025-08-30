from flask import Flask, render_template, request, make_response  # 新增make_response导入
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
      user = request.form['nm']
   
      resp = make_response(render_template('readcookie.html'))
      resp.set_cookie('userID', user)
      return resp  # 将return移到条件判断内，确保只在POST时返回
   # 处理GET请求的情况
   return "请通过POST方法提交表单", 405

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('userID')
   if name:  # 增加判断，避免cookie不存在时出错
       return f'<h1>welcome {name}</h1>'
   return '<h1>未找到用户信息</h1>'

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
