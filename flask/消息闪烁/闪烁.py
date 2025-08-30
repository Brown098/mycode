from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # 消息闪现需要配置秘钥


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # 模拟登录验证（用户名和密码均为 'admin' 时通过）
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials! Please try again.'  # 验证失败时的错误信息
        else:
            # 登录成功，闪现成功消息并跳转首页
            flash('You were successfully logged in!')
            return redirect(url_for('index'))
    # GET 请求或验证失败时，返回登录页并显示错误
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True,host="::")