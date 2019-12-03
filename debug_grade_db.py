#  Copyright (c) 2019.  MIT license
#  Jipeng Qian.
#  This is a copyrighted source code under MIT license,
#  you should receive a copy of the copyright,
#  together with this source code.
#  Have fun with your favor!

import unittest
import app

class MyTestCase(unittest.TestCase):
    def test_something(self):
        grade = app.Grade.query.filter_by(SId=179134088).all()

        print(grade)

        # self.assertEqual(True, False)
    def test2(self):
        grade = app.Grade.query.all()
        print(grade)

    def test3(self):
        notice = app.Notice.query.all()
        print(notice)


if __name__ == '__main__':
    unittest.main()
