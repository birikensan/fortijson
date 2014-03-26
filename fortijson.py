#!/usr/bin/env python
# -*- coding: utf-8 -*-

# vdomには対応していません。
# vdomで利用したい場合は、各vdomの設定項目を別ファイルに分けて下さい。
#
import re
import linecache

# config firewall policyの場所を探して変数topに格納する。
top = 0
regex_top = re.compile('^config firewall policy$')
for i,line in enumerate(open('config.conf', 'r')):
    if regex_top.search(line) is not None:
        top = i + 1 

# endの場所を探して、配列endに格納する。
end = []
regex_end = re.compile('^end$')
for i,line in enumerate(open('config.conf', 'r')):
    if regex_end.search(line) is not None:
        end.append(i + 1)

# 配列endの要素と変数とtopを比較し、
# config firewall policyに紐づくendを見つける
for endpoint in end:
    if top < endpoint:
        last = endpoint
        break

# topからlastまでの範囲を1行ずつ読み込んで、json記法に置換していく
# 抽出後に末尾の,を調整する必要があるため、配列に入れる。

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
    line = linecache.getline('config.conf',linenum)
    
    # edit hogehogeを変換する部分
    if regex_id.search(line) is not None:
        # 正規表現で数字の部分ひっかける
        idnum = regex_id.search(line).groups(0)
        config.append('"'+idnum[0]+'":{')

    # set hoehoge hogehogeを変換する部分
    if regex_set.search(line) is not None:
        # 正規表現で設定項目と設定内容をひっかける
        setline = regex_set.search(line).groups()
        # 設定内容は後ろに無意味な空白があるので置換する
        setparam = regex_delempty.sub("",setline[1])
        # 設定内容のダブルコーテーションを置換する
        setparam = regex_dq.sub("",setparam)
        config.append('"'+setline[0]+'":"'+setparam+'",')

    # nextを置換する部分
    if regex_next.search(line) is not None:
        config.append("},")

    if regex_end.search(line) is not None:
        config.append("}")
        
        
config.append('}')
config.append('}')
    
for i in range(len(config)):
    #
    # 文字列が},だったらひとつ前の配列の末尾から,を削除する。
    if config[i] == "},":
        config[i - 1] = re.sub('",','"',config[i -1])


for line in config:
    print(line)
