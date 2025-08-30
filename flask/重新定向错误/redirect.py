from flask import Flask, redirect, url_for, render_template, request,abort
# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('log_in.html')

@app.route("/login", methods=["GET", "POST"])  # 添加了方法声明
def login():
    
    if request.method == "POST":

        # 修复了request.from的拼写错误，应为request.form
        if request.form["username"] == "admin":
            return redirect(url_for('success'))
        else:
            abort(404)
    else:
        return redirect(url_for('index'))


@app.route('/success')
def success():
   return 'logged in successfully'
	
if __name__ == '__main__':
   app.run(debug = True,host = "::")