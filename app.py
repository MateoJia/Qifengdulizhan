from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 模拟商品数据
products = [
    {
        'id': 1,
        'name': '精品茶具套装',
        'description': '传统手工制作，精致典雅',
        'price': 299,
        'image': 'https://via.placeholder.com/300x200'
    },
    {
        'id': 2,
        'name': '手工编织包',
        'description': '天然材料，环保时尚',
        'price': 399,
        'image': 'https://via.placeholder.com/300x200'
    },
    {
        'id': 3,
        'name': '手工皮具',
        'description': '优质真皮，匠心之作',
        'price': 499,
        'image': 'https://via.placeholder.com/300x200'
    }
]

# 模拟评价数据
reviews = [
    {
        'user_name': '张先生',
        'rating': 5,
        'comment': '非常好用的鱼竿，手感轻盈，收线顺滑，已经用它钓到好几条大鱼了！',
        'image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f',
        'date': '2024-12-28'
    },
    {
        'user_name': '李先生',
        'rating': 5,
        'comment': '做工精细，携带方便，性价比很高。周末去钓鱼特别适合！',
        'image': 'https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b',
        'date': '2024-12-25'
    },
    {
        'user_name': '王女士',
        'rating': 4,
        'comment': '很适合新手使用，重量轻，操作简单。唯一缺点是收纳袋可以再结实一点。',
        'image': 'https://images.unsplash.com/photo-1542372147193-a7aca54189cd',
        'date': '2024-12-20'
    }
]

@app.route('/')
def home():
    return render_template('index.html', products=products, reviews=reviews)

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    # 这里可以添加发送邮件或保存联系信息的逻辑
    return jsonify({'message': '消息已收到，我们会尽快回复您！'})

@app.route('/submit-review', methods=['POST'])
def submit_review():
    if 'image' not in request.files:
        return jsonify({'error': '请上传图片'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        new_review = {
            'user_name': request.form.get('user_name'),
            'rating': int(request.form.get('rating')),
            'comment': request.form.get('comment'),
            'image': url_for('static', filename=f'uploads/{filename}'),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        reviews.insert(0, new_review)
        
        return redirect(url_for('home') + '#reviews')

if __name__ == '__main__':
    app.run(debug=True)
