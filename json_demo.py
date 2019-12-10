#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!

import json


with open('.\\score.json', 'r', encoding='utf8') as f:
    source = f.read()

source = json.loads(source)

zhuguan = list()
tingli = list()
yuedu = list()

for item in source:
    if item['class'] == '价191':
        zhuguan.append(item['主观'])
