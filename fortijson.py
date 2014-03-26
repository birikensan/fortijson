#!/usr/bin/env python
# -*- coding: utf-8 -*-

# vdom$B$K$OBP1~$7$F$$$^$;$s!#(B
# vdom$B$GMxMQ$7$?$$>l9g$O!"3F(Bvdom$B$N@_Dj9`L\$rJL%U%!%$%k$KJ,$1$F2<$5$$!#(B
#
import re
import linecache

# config firewall policy$B$N>l=j$rC5$7$FJQ?t(Btop$B$K3JG<$9$k!#(B
top = 0
regex_top = re.compile('^config firewall policy$')
for i,line in enumerate(open('config.conf', 'r')):
    if regex_top.search(line) is not None:
        top = i + 1 

# end$B$N>l=j$rC5$7$F!"G[Ns(Bend$B$K3JG<$9$k!#(B
end = []
regex_end = re.compile('^end$')
for i,line in enumerate(open('config.conf', 'r')):
    if regex_end.search(line) is not None:
        end.append(i + 1)

# $BG[Ns(Bend$B$NMWAG$HJQ?t$H(Btop$B$rHf3S$7!"(B
# config firewall policy$B$KI3$E$/(Bend$B$r8+$D$1$k(B
for endpoint in end:
    if top < endpoint:
        last = endpoint
        break

# top$B$+$i(Blast$B$^$G$NHO0O$r(B1$B9T$:$DFI$_9~$s$G!"(Bjson$B5-K!$KCV49$7$F$$$/(B
# $BCj=P8e$KKvHx$N(B,$B$rD4@0$9$kI,MW$,$"$k$?$a!"G[Ns$KF~$l$k!#(B

# $BCV49$GMxMQ$9$k@55,I=8=$O$"$i$+$8$a%3%s%Q%$%k$9$k!#(B
regex_id = re.compile(r'edit\s([0-9]+)$')
regex_set = re.compile(r'set\s([^ ]+)\s(.+)$')
regex_delempty = re.compile(r'\"\s+?$')
regex_dq = re.compile(r'\"')
regex_next = re.compile(r'next$')
regex_end = re.compile(r'^end$')

config =[]
config.append("{")
config.append('"config firewall policy": {')
# top$B$+$i(Blast$B$N9THV9f$NHO0O$G(B
for linenum in range(top, last + 1):
    # $B9THV9f$r;XDj$7$F9T$rFI$_9~$_8eB3=hM}$K?J$`!#(B
    line = linecache.getline('config.conf',linenum)
    
    # edit hogehoge$B$rJQ49$9$kItJ,(B
    if regex_id.search(line) is not None:
        # $B@55,I=8=$G?t;z$NItJ,$R$C$+$1$k(B
        idnum = regex_id.search(line).groups(0)
        config.append('"'+idnum[0]+'":{')

    # set hoehoge hogehoge$B$rJQ49$9$kItJ,(B
    if regex_set.search(line) is not None:
        # $B@55,I=8=$G@_Dj9`L\$H@_DjFbMF$r$R$C$+$1$k(B
        setline = regex_set.search(line).groups()
        # $B@_DjFbMF$O8e$m$KL50UL#$J6uGr$,$"$k$N$GCV49$9$k(B
        setparam = regex_delempty.sub("",setline[1])
        # $B@_DjFbMF$N%@%V%k%3!<%F!<%7%g%s$rCV49$9$k(B
        setparam = regex_dq.sub("",setparam)
        config.append('"'+setline[0]+'":"'+setparam+'",')

    # next$B$rCV49$9$kItJ,(B
    if regex_next.search(line) is not None:
        config.append("},")

    if regex_end.search(line) is not None:
        config.append("}")
        
        
config.append('}')
config.append('}')
    
for i in range(len(config)):
    #
    # $BJ8;zNs$,(B},$B$@$C$?$i$R$H$DA0$NG[Ns$NKvHx$+$i(B,$B$r:o=|$9$k!#(B
    if config[i] == "},":
        config[i - 1] = re.sub('",','"',config[i -1])


for line in config:
    print(line)
