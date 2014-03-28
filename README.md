# fortijson
FortiGateのコンフィグファイルをjsonにするpythonスクリプトを目指しています。

## 機能

### fortijson.policytojson
文字列のコンフィグファイルを渡すと、FWポリシー（config firewal policy）の部分をjson化した上で辞書オブジェクトとして戻します。途中のtmp変数に、json化された文字列が格納されています。  
※VDOMを利用しているconfigは正常に動作しません。VDOMごとに取得したコンフィグファイルを利用してください。

### fortijson.jsontoparam
policytojsonで作成された辞書オブジェクトとファイル名を渡すと、辞書オブジェクトの中身を整形して、「ファイル名.csv」のファイルを作成します。

### index.py
policytojsonとjsontoparamを使ったGUIです。FortiGateのコンフィグをアップロードすると、FWポリシーの部分がいい感じで整理されたCSVとして出力されます。
bottle+gunicornで実装されています。

## GUIの使い方
python3で書いています。virtualenvなどでpython3が使える環境を用意してください。

	git clone https://github.com/kongou-ae/fortijson.git
	cd fortijson
    ### 必要に応じてpipでモジュールをインストールしてください。
	pip install bottle
	pip install jinja2
	pip install gunicorn
	### IPアドレスとポート番号とワーカは任意で変更してください。
    ### 製作者はnginxをプロキシとして利用しているため、loopbackで起動させています。
	gunicorn -b 127.0.0.1:8085 -w 1 index:app


    
