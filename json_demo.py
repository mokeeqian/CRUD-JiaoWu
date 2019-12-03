#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!

import json

data = json.loads('[{"id":"001","title":"关于....","content":"正文内容111111","publisherid":"1001"},{"id":"002","title":"关于....","content":"正文内容22222","publisherid":"1002"}]')

print(data[0]['id'])

data = json.dumps(data)

