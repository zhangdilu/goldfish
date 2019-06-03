#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from flask import Flask, request, Response,send_file, render_template as rt
import pymongo
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
from bson.errors import InvalidId # For catching InvalidId exception for ObjectId
from bson.json_util import dumps

app = Flask(__name__)

#static_folder='static',static_url_path=''
@app.route('/', methods=['GET'])
def index():
    return rt('./index.html')


@app.route('/file/upload', methods=['POST'])
def upload_part():  # 接收前端上传的一个分片
    task = request.form.get('task_id')  # 获取文件的唯一标识符
    chunk = request.form.get('chunk', 0)  # 获取该分片在所有分片中的序号
    filename = '%s%s' % (task, chunk)  # 构造该分片的唯一标识符

    upload_file = request.files['file']
    upload_file.save('./upload/%s' % filename)  # 保存分片到本地
    return rt('./index.html')


@app.route('/file/merge', methods=['GET'])
def upload_success():  # 按序读出分片内容，并写入新文件
    target_filename = request.args.get('filename')  # 获取上传文件的文件名
    task = request.args.get('task_id')  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    with open('./upload/%s' % target_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except (IOError, msg):
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间

    return rt('./index.html')


@app.route('/file/list', methods=['GET'])
def file_list():
    files = os.listdir('./upload/')  # 获取文件目录
    files = map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), files)  # 注意编码
    return rt('./list.html', files=files)


@app.route('/file/download/<filename>', methods=['GET'])
def file_download(filename):
    def send_chunk():  # 流式读取
        store_path = './upload/%s' % filename
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')

@app.route('/#one',methods=['GET'])
def return_video():
	# TODO:前端渲染index.html中的#one
	# TODO:不应该读取最新的
	dir = './analysis'
	videos = os.listdir(dir)
	videos.sort(key=lambda fn: os.path.getmtime(dir + "/" + fn)
                    if not os.path.isdir(dir + "/" + fn) else 0)
	print('newest: ' + videos[-1])
	file = os.path.join(dir, videos[-1])
	print('fullpath', file)
	return send_file(file,mimetype='video/mp4')
	#return rt('./data.html',files=file)

#@app.route('/data',methods=['GET'])
@app.route('/result/<p_id>',methods=['GET'])
def show_result(p_id):
	# 返回pid对应的分析结果
	# TODO:渲染index.html中的#two
	return dumps(collection.find_one({'p_id':p_id}))
	#return rt('./index.html')

@app.route('/result',methods=['GET'])
def show_results():
	# 返回所有分析结果
	# TODO:渲染index.html中的#two
	return dumps(collection.find())
	#return rt('./index.html')

if __name__ == '__main__':
	connection=pymongo.MongoClient("localhost",27017)
	db = connection.goldfish
	collection = db.goldfish
	app.run(debug=True, threaded=True,host='0.0.0.0')
