from flask import Flask, render_template, request

# 初始化 Flask 应用
app = Flask(__name__)

# 1. 路由：访问首页，渲染表单页面
@app.route('/')
def index():
    # 渲染 templates 文件夹下的 index.html
    return render_template('index2.html')

# 2. 路由：接收前端 POST 请求传递的数据
# methods=['POST'] 表示该路由仅处理 POST 方法
@app.route('/submit', methods=['POST'])
def submit_data():
    # 从表单中获取数据（name 属性对应 HTML 表单的 name 值）
    username = request.form.get('username')  # 获取用户名
    age = request.form.get('age')            # 获取年龄
    hobby = request.form.getlist('hobby')    # 获取多选的爱好（用 getlist 接收数组）

    # 后端打印接收的数据（可替换为存储数据库、业务处理等逻辑）
    print(f"接收的前端数据：")
    print(f"用户名：{username}")
    print(f"年龄：{age}")
    print(f"爱好：{hobby}")

    # 将数据回传给前端展示（也可直接返回成功提示）
    return f"""
    <h3>数据提交成功！</h3>
    <p>用户名：{username}</p>
    <p>年龄：{age}</p>
    <p>爱好：{', '.join(hobby)}</p>
    <a href="/">返回重新提交</a>
    """

# 启动服务（仅开发环境使用）
if __name__ == '__main__':
    app.run(debug=True)  # debug=True 开启调试模式，代码修改后自动重启