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
    
    # policytojson$B$GFI$_9~$`$?$a$N(Btemp$B%U%!%$%k$r:n@.$9$k!#(B
    f = tempfile.NamedTemporaryFile()
    strline = ''
    # HTML$B$+$i<u$1$C$?%U%!%$%k$,(Bbyte$B$J$N$G!"0l9T$:$DJ8;zNs$KJQ49$7$FJQ?t$K3JG<$9$k(B
    # $B$b$C$H$$$$J}K!$,$"$j$=$&!#!#!#(B
    for line in configfile.file.readlines():
        strline = strline + line.decode()
    # byte$B$KLa$7$F(Btemp$B%U%!%$%k$K=q$-9~$_(B
    f.write(strline.encode())
    # temp$B%U%!%$%k$N%Q%9$r%a%=%C%I$KEO$7$F!"(Bjson$B$J<-=q7?$K$9$k!#(B
    policyjson = fortijson.policytojson(f.name)
    # $B=PNO@h%U%!%$%kL>MQ$N;~9o$r<hF@$9$k(B$
    now = str(datetime.datetime.now())
    filename = configfile.filename+"_"+now
    f.close

    # $B<-=q$H;~9o$r0z?t$K4X?t$r8F$S=P$9(B$
    fortijson.jsontoparam(policyjson,filename)

    return template('index',filename=filename)

@route('/forti/static/<filename>')
def static(filename):
    return static_file(filename, root='./static')

app = default_app()
