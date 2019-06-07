#!/usr/bin/env python
# coding=utf-8

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
            except IOError, msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
    #上传文件成功后，跑模型得到新的视频文件
    #保存进数据库以后再读取数据库返回数据库所有条目在前端表格中显示


    #第一步读取数据库中所有男性的数目，和所有女性的数目，得到男女占比,返回男比例，女比例,前端显示饼状图.
    #第二步每隔一段时间（可以是5s，10s）统计人的数目，返回 时间：数目,前端显示折线图.
    #第三步读取数据库中所有人的条目返回，前端显示列表
	
    #返回的数据写在这里 data[0],data[1]放男和女的占比 比如说0.2 0.8,
    #data[2]放  时间：人数,时间不管是多少间隔要一样,这里间隔是1
    #data[3]之后放返回给前端表格的数据，依次为出现时间，消失时间，x平均值，y平均值，性别，身高年龄

    data = [{
					    "value": .2,
					    "color": "#BEE7E9",
					    "title": "男",
					  		
					},{
					    "value": .8,
					    "color": "#ECAD9E",
					    "title": "女"
					},{
					    "1": 5,
					    "2":10,
					    "3":14,
					    "4":18,
					    "5":25,
					    "6":29,	
					},{
					    "appeartime":3,
					    "disappeartime":4,
					    "centerx":5,
					    "centery":6,
					    "Gender":"male",
					    "Height":1.80,
					    "Age":35,
					}	
	  		
												
						];
 
    shutil.move("./upload/"+target_filename,"./static/"+target_filename)	
    time.sleep(3)	
    #data="finish"
    return json.dumps(data)


@app.route('/file/list', methods=['GET'])
def file_list():
    files = os.listdir('./upload/')  # 获取文件目录
    files = map(lambda x: x if isinstance(x, unicode) else x.decode('utf-8'), files)  # 注意编码
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
