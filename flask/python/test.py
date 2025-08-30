from flask import Flask, render_template, jsonify  # 导入jsonify
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
# 这个路由返回HTML模板
@app.route("/")
def index():
    username = "alice"
    score = 95
    is_number = True
    hobbies = ["阅读", "跑步", "编程"]
    user_info = {"name": "bob", "age": 28, "city": "北京"}
    return render_template(
        "index.html",
        user=username,
        user_score=score,
        member_status=is_number,
        user_hobbies=hobbies,  # 修正了拼写错误hobibes→hobbies
        user_detail=user_info
    )

# 这个路由返回JSON数据
@app.route("/api")
def api():
    return jsonify({
        'username': "alice",
        "score": 95,
        'is_number': True,  # 修正了拼写错误is_numbert→is_number
    })

if __name__ == "__main__":
    app.run(debug=True, host="::")
