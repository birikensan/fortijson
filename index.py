#/usr/bin/env python
# -*- coding: utf-8 -*-

import fortijson
import datetime
from bottle import route, request, run, static_file, default_app
from bottle import jinja2_template as template
import tempfile


@route("/forti")
def index():
    return template('index')
    

@route("/forti", method='POST')
def upload():
    configfile = request.files.get('file')
    
    # policytojsonで読み込むためのtempファイルを作成する。
    f = tempfile.NamedTemporaryFile()
    strline = ''
    # HTMLから受けったファイルがbyteなので、一行ずつ文字列に変換して変数に格納する
    # もっといい方法がありそう。。。
    for line in configfile.file.readlines():
        strline = strline + line.decode()
    # byteに戻してtempファイルに書き込み
    f.write(strline.encode())
    # tempファイルのパスをメソッドに渡して、jsonな辞書型にする。
    policyjson = fortijson.policytojson(f.name)
    # 出力先ファイル名用の時刻を取得する$
    now = str(datetime.datetime.now())
    filename = configfile.filename+"_"+now
    f.close

    # 辞書と時刻を引数に関数を呼び出す$
    fortijson.jsontoparam(policyjson,filename)

    return template('index',filename=filename)

@route('/forti/static/<filename>')
def static(filename):
    return static_file(filename, root='./static')

app = default_app()
