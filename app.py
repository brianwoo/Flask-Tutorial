from flask import Flask, request
import sqlite3
import os
from werkzeug.exceptions import abort

app = Flask(__name__)

DB = './db/database.db'

def create_db():
    conn = sqlite3.connect(DB)
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

def get_db_connection():
    if not os.path.isfile(DB):
        create_db()
    
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def querySingle(sql, args):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, args)
        for row in cursor:
            return dict((column[0],row[index]) for index, column in enumerate(cursor.description))
        return None
    finally:
        cursor.close()

def queryMultiple(sql, args):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if args is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, args)
        rows = cursor.fetchall()
        return [dict((column[0],row[index]) for index, column in enumerate(cursor.description)) for row in rows]
    finally:
        cursor.close()


def get_post(post_id):
    post = querySingle('SELECT * FROM posts WHERE id = ?', (post_id,))    
    if post is None:
        abort(404)
    return post


@app.route('/posts')
def index():
    posts = queryMultiple('SELECT * FROM posts', None)
    return posts


@app.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return post


@app.route('/posts', methods=('POST',))
def create():
    title = request.json['title']
    content = request.json['content']
    if not title:
        return 'Title is required', 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                    (title, content)
                    )
        conn.commit()
        return 'Post created', 201
    except sqlite3.Error as e:
        return str(e), 500
    finally:
        conn.close()
    


@app.route('/posts/<int:post_id>', methods=('PUT',))
def update(post_id):
    title = request.json['title']
    content = request.json['content']
    if not title:
        return 'Title is required', 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                    (title, content, post_id)
                    )
        conn.commit()
        return 'Post updated', 200
    except sqlite3.Error as e:
        return str(e), 500
    finally:
        conn.close()


@app.route('/posts/<int:post_id>', methods=('DELETE',))
def delete(post_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
        return 'Post deleted', 200
    except sqlite3.Error as e:
        return str(e), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)