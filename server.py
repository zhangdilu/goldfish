#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import shutil
import json
import resolve
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
    local_path = '/Users/michelle/Documents/research/goldfish/upload/'
    name = local_path+target_filename
    os.system("python3 /Users/michelle/Documents/research/homework/backend/Goldfish_backend/realtime_demo_fast_with_track_dataset_output.py --video %s"
            %name)
    #shutil.move("./upload/"+target_filename,"./static/"+target_filename)
    time.sleep(10)
    data = resolve.resolveJson('./merged.json')
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
