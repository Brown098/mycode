from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "any random string"  # 移除了多余的空格

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
         "<b><a href='/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href='/login'><b>" + \
      "click here to log in</b></a>"  # 修复了HTML标签错误

@app.route("/login", methods=["GET", "POST"])  # 添加了方法声明
def login():
    
    if request.method == "POST":

        # 修复了request.from的拼写错误，应为request.form
        if request.form["username"] == "admin":
            return redirect(url_for('su'))
        else:
            abort(401)
    else:
        return redirect(url_for('index'))


        


@app.route('/logout')
def logout():
    # 移除会话中的用户名
    session.pop('username', None)
    return redirect(url_for('index'))
@app.route('/success')
def success():
   return 'logged in successfully'
if __name__ == "__main__":
    app.run(debug=True, host="::", port=5000)
    