from flask import Flask, render_template, request
from werkzeug.utils import secure_filename  # 修正导入路径
import os

app = Flask(__name__)

# 配置上传文件夹和允许的文件扩展名
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',"zip"}

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload')
def show_upload_form():  # 修正函数名，避免重复
    return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def handle_upload():  # 修正函数名，避免重复
    if request.method == 'POST':
        # 检查是否有文件部分
        if 'file' not in request.files:
            return 'No file part'
        
        f = request.files['file']
        
        # 检查用户是否选择了文件
        if f.filename == '':
            return 'No selected file'
        
        # 检查文件是否符合要求并保存
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            # 保存到指定的上传文件夹
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'
        
        # 如果文件类型不允许
        return 'File type not allowed'
		
    # 处理GET请求
    return 'Please use POST method to upload files'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

