#/usr/bin/env python
# -*- coding: utf-8 -*-

import fortijson
import datetime
from bottle import route, request, run, static_file, default_app
from bottle import jinja2_template as template
import tempfile

# サブディレクトリ/fortiで公開する
@route("/forti-dev")
def index():
    return template('index')
    
# configファイルをPOSTした後の処理
@route("/forti-dev", method='POST')
def upload():
    # Formからファイルを受け取る。
    configfile = request.files.get('file')    
    # ファイルをpolicytojsonで読み込むためのtempファイルを作成する。
    f = tempfile.NamedTemporaryFile()
    strline = ''
    # HTMLから受けったファイルがbyteなので、一行ずつ文字列に変換して変数strlineに格納する
    # もっといい方法がありそう。。。
    for line in configfile.file.readlines():
        strline = strline + line.decode()
    # byteに戻してtempファイルに書き込み
    f.write(strline.encode())
    # tempファイルのパスをpolicytojsonメソッドに渡して、jsonな辞書型を受け取る。
    policyjson = fortijson.policytojson(f.name)

    # 出力先ファイル名用の時刻を取得する$
    now = str(datetime.datetime.now())
    # 返還後のファイル名をもともとのファイル名+_時刻とする。
    filename = configfile.filename+"_"+now
    # tmpfileをクローズする。
    f.close

    # 辞書と時刻を引数にjsontoparamメソッド呼び出して、ファイルを作成する。
    fortijson.jsontoparam(policyjson,filename)

    return template('index',filename=filename)

# 作成されたファイルを公開するための処理
@route('/forti-dev/static/<filename>')
def static(filename):
    return static_file(filename, root='./static')

app = default_app()
