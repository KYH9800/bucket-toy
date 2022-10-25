from flask import Flask, render_template, request, jsonify
# mongoDB, You have to install pymongo, dnspython before a start
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.nxcyemj.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['user_bucket_give']

    count = len(list(db.bucket.find({}, {'_id': False})))
    count += 1

    doc = {
        'num': count,
        'bucket': bucket_receive,
        'done': 0
    }
    db.bucket.insert_one(doc)

    return jsonify({
        'msg': '리스트 추가 완료!'
    })


# 몇 번째의 리스트인지 num 가져오기 -> 완료 시 done을 1로 update
# db.bucket.update_one({'num': num_receive}, {'$set': {'done': 1}})

# 완료
@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']

    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({
        'msg': '달성!!'
    })


# 취소
@app.route("/bucket/undone", methods=["POST"])
def bucket_undone():
    num_receive = request.form['num_give']

    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({
        'msg': '취소 완료!!'
    })


# 삭제
@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    num_receive = request.form['num_give']

    db.bucket.delete_one({'num': int(num_receive)})
    return jsonify({
        'msg': '삭제 완료'
    })


@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_bucket_lists = list(db.bucket.find({}, {'_id': False}))

    return jsonify({
        'all_bucket_lists': all_bucket_lists
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
