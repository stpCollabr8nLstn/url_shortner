import flask
import uuid
import base64
import json
import os

app = flask.Flask(__name__)

urls = {}

if os.path.exists('bookmarks.json'):
    with open('bookmarks.json', 'r') as f:
        urls = json.load(f)


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_alias():
    key = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:12].decode('ascii')
    url = flask.request.form['url']
    if not url.startswith('http'):
        url = 'http://' + url
    for saved_key in urls:
        print(saved_key)
        if urls[saved_key] == url:
            print('url already in database')
            return flask.redirect(saved_key + '?preview=1')
    else:
        urls.update({key: url})
        with open('bookmarks.json', 'w') as f:
            json.dump(urls, f)
        return flask.redirect(key + '?preview=1')


@app.route('/<key>')
def preview(key):
    if key not in urls:
        flask.abort(404)
    if 'preview' in flask.request.args:
            if flask.request.args['preview'] == '1':
                return flask.render_template('preview.html', key=key, dict_keys=urls)
    else:
        print(urls[key])
        return flask.redirect(urls[key], 301)
2
@app.errorhandler(404)
def not_found(err):
    return flask.render_template('404.html', path=flask.request.path), 404


if __name__ == '__main__':
    app.run()
