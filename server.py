#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import shutil
import json

from flask import Flask, request, Response, render_template as rt

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
            except IOError as msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
    #上传文件成功后，跑模型得到新的视频文件
    #保存进数据库以后再读取数据库返回数据库所有条目在前端表格中显示
    data=[{"_id": 95, "avg_height": 1.5526633223005046, "avg_gender": 1, "avg_age": 23, "min_time": 160.52, "max_time": 160.6,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 92, "avg_height": 1.7253909296321308, "avg_gender": 1, "avg_age": 21, "min_time": 160.08, "max_time": 164.24,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 84, "avg_height": 1.618190753334315, "avg_gender": 1, "avg_age": 25, "min_time": 142.64, "max_time": 150.16,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 83, "avg_height": 1.5766488467882043, "avg_gender": 0.2, "avg_age": 28, "min_time": 124.6, "max_time": 142.44,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 82, "avg_height": 1.4767778356946877, "avg_gender": 0.2, "avg_age": 27, "min_time": 123.56, "max_time": 127.36,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 80, "avg_height": 1.6305267477974306, "avg_gender": 0.2, "avg_age": 18, "min_time": 113.8, "max_time": 120.52,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 76, "avg_height": 1.6855931616806203, "avg_gender": 0.2, "avg_age": 17, "min_time": 97.08, "max_time": 97.96,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 64, "avg_height": 1.607870452636408, "avg_gender": 1, "avg_age": 16, "min_time": 95.28, "max_time": 96.92,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 7, "avg_height": 2.067718703833809, "avg_gender": 1, "avg_age": 15, "min_time": 4.8, "max_time": 7.64,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 57, "avg_height": 1.5854533427576873, "avg_gender": 1.0, "avg_age": 14, "min_time": 93.44, "max_time": 94.44,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 56, "avg_height": 1.6651421069121044, "avg_gender": 1.0, "avg_age": 13, "min_time": 92.92, "max_time": 95.2,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]},{"_id": 87, "avg_height": 1.6685129331401467, "avg_gender": 1.0, "avg_age": 12, "min_time": 152.4, "max_time": 157.84,"location": [{"x1": 634.181104712387, "x2": 953.9618854130132, "y1": 243.6836028234065, "y2": 641.204401454065}, {"x1": 680.6844718229, "x2": 949.9091972316673, "y1": 202.93548147094674, "y2": 535.3057713582584}]}];
    shutil.move("./upload/"+target_filename,"./static/"+target_filename)	
    time.sleep(3)	
    #data="finish"
    return json.dumps(data)


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


if __name__ == '__main__':
    app.run(debug=False, threaded=True,host='0.0.0.0')
