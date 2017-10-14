#!/usr/bin/env python
# @Author  : pengyun


from eve import Eve
from flask import request

app = Eve(auth=None)


@app.before_request
def before():
    print('before', request)


@app.after_request
def after(response):
    return response


if __name__ == '__main__':
    app.run(debug=True)
