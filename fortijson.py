#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
import re
import linecache
import json

def policytojson(configfile):

    # config firewall policyの場所を探して変数topに格納する。
    top = 0
    regex_top = re.compile('^config firewall policy$')
    for i,line in enumerate(open(configfile, 'r')):
        if regex_top.search(line) is not None:
            top = i + 1 

    # endの場所を探して、配列endに格納する。
    # endは複数あるので配列を利用する
    end = []
    regex_end = re.compile('^end$')
    for i,line in enumerate(open(configfile, 'r')):
        if regex_end.search(line) is not None:
            end.append(i + 1)

    # 配列endの要素と変数とtopを比較し、
    # config firewall policyに紐づくendを見つける
    for endpoint in end:
        if top < endpoint:
            last = endpoint
            break

    # topからlastまでの範囲を1行ずつ読み込んで、json記法に置換していく
    # 抽出後に末尾の,を調整する必要があるため、配列configに入れる。

    # 置換で利用する正規表現はあらかじめコンパイルする。
    regex_id = re.compile(r'edit\s([0-9]+)$')
    regex_set = re.compile(r'set\s([^ ]+)\s(.+)$')
    regex_delempty = re.compile(r'\"\s+?$')
    regex_dq = re.compile(r'\"')
    regex_next = re.compile(r'next$')
    regex_end = re.compile(r'^end$')

    config =[]
    config.append("{")
    config.append('"config firewall policy": {')
    # topからlastの行番号の範囲で
    for linenum in range(top, last + 1):
        # 行番号を指定して行を読み込み後続処理に進む。
        line = linecache.getline(configfile,linenum)
    
        # edit hogehogeを変換する部分
        if regex_id.search(line) is not None:
            # 正規表現で数字の部分ひっかける
            idnum = regex_id.search(line).groups(0)
            config.append('"'+idnum[0]+'":{')

        # set hoehoge hogehogeを変換する部分
        if regex_set.search(line) is not None:
            # 正規表現で設定項目と設定内容をひっかける
            setline = regex_set.search(line).groups()
            # 設定内容はなぜか後ろに無意味な空白ができるので置換する
            setparam = regex_delempty.sub("",setline[1])
            # 設定内容のダブルコーテーションを置換する
            setparam = regex_dq.sub("",setparam)
            config.append('"'+setline[0]+'":"'+setparam+'",')

        # nextを置換する部分
        if regex_next.search(line) is not None:
            config.append("},")

	# 最後のendを置換する部分
        if regex_end.search(line) is not None:
            config.append("}")
        
        
    # 微調整する
    for i in range(len(config)):
        #
        # 文字列が},だったらひとつ前の配列の末尾から,を削除する。
        if config[i] == "},":
            config[i - 1] = re.sub('",','"',config[i -1])

        # 文字列が}だったら、ひとつ前の配列の末尾から,を削除する。
        if config[i] == "}":
            config[i - 1] = re.sub('},','}',config[i -1])

    config.append('}')

    # 配列の要素を一つの変数に格納する
    tmp = ''
    for line in config:
        tmp = tmp + line

    # 格納した変数（str）をjsonモジュールで辞書型に変更する。
    json_conf = json.loads(tmp)
    # 辞書型を戻す
    return json_conf


def jsontoparam(json_conf,filename):
    # ポリシーで設定されている設定項目を抽出する。
    # ポリシーidの箇所をイテレータで確認する。
    params = []
    for id in iter(json_conf['config firewall policy'].keys()):
        # ポリシーID配下の設定項目をイテレータで確認する
        for value in iter(json_conf['config firewall policy'][id].keys()):
            # 確認した要素を配列に格納する。
            params.append(value)

    #　配列から重複を削除し、ユニークな設定項目配列を作成する。
    param_array = list(set(params))

    policy_array = []
    policy_line = ''
    # ポリシーIDを一つずつ変数idに格納する。
    for id in iter(json_conf['config firewall policy'].keys()):
        # ユニークな設定項目の配列から一つずつ設定項目をparamに格納する。
        for param in param_array:
            # 辞書の中にparamの設定内容があるかチェックして、pilicy_lineに要素を追記していく
            policy_line = policy_line + ',' + json_conf['config firewall policy'][id].get(param,"-")
        #　追記した要素をpolicy_array配列に格納する。
        policy_array.append(id+policy_line)
        # 次のIDに備えてpolicy_lineを初期化する
        policy_line = ''

    #　ポリシー一覧の見出しとなる1行目をparam_lineに格納する。
    param_line = 'id'
    for param in param_array:
        param_line = param_line + "," + param

    # csvファイルにparam_line（見出しを書き込む）
    f = open("./static/"+filename+".csv",'w')
    f.write(param_line+"\n")

    # csvファイルにpolicy_array（ID単位のルール）を書き込む
    policy = ''
    for policy in policy_array:
        f.write(policy+"\n")

    f.close

