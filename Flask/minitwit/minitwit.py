from __future__ import with_statement
import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from contextlib import closing
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash
from werkzeug.security import check_password_hash, generate_password_hash

# 환경설정.
DATABASE = 'minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

# DB 연결.
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# [DB] create table
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# DB 쿼리문 처리.
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
                for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

# username을 입력하면, user_id를 가져오는 함수.
def get_user_id(username):
    rv = g.db.execute('select user_id from user where username = ?',
                        [username]).fetchone()
    return rv[0] if rv else None

def format_datetime(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

# 주소에 대한 gravatar 이미지 반환.
def gravatar_url(email, size=80):
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@app.before_request
def before_request():
    g.db = connect_db() # DB 연결.

    # 사용자 정보 조회.
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                            [session['user_id']], one=True)

# 요청 응답 후 DB 연결 끊기.
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


# 기본 타임라인.(로그인 상태)
@app.route('/')
def timeline():

    # 로그인하지 않은 경우 공용 타임라인으로 리디렉션.
    if not g.user:
        return redirect(url_for('public_timeline'))

    # 사용자 & 팔로잉 하는 사용자의 메시지 표시.
    return render_template('timeline.html', messages=query_db('''
        select message.*, user.* 
          from message, user
         where message.author_id = user.user_id and 
                (user.user_id = ? or
                 user.user_id in (select whom_id 
                                    from follower
                                   where who_id = ?))
         order by message.pub_date desc limit ?''',
        [session['user_id'], session['user_id'], PER_PAGE]))

# 공용 타임라인.
# 전체 사용자의 메시지 표시.
@app.route('/public')
def public_timeline():
    return render_template('timeline.html', messages=query_db('''
        select message.*, user.*
          from message, user
         where message.author_id = user.user_id
         order by message.pub_date desc limit ?''', [PER_PAGE]))

# 특정 사용자 타임라인.
@app.route('/<username>')
def user_timeline(username):

    # 지정한 사용자가 실제 존재하는지 확인.
    profile_user = query_db('select * from user where username = ?',
                            [username], one=True)
    if profile_user is None:
        abort(404)
    followed = False

    # 지정한 사용자의 팔로잉 유무를 확인.
    if g.user:
        followed = query_db('''select 1 
                                 from follower
                                where follower.who_id = ? and follower.whom_id = ?''',
                                [session['user_id'], profile_user['user_id']], 
                                one=True) is not None
    return render_template('timeline.html', messages=query_db('''
            select message.*, user.*
              from message, user
             where user.user_id = message.author_id and user.user_id = ?
             order by message.pub_date desc limit ?''',
             [profile_user['user_id'], PER_PAGE]), followed=followed,
             profile_user=profile_user)

# follow.
@app.route('/<username>/follow')
def follow_user(username):

    # 로그인 상태 확인.
    if not g.user:
        abort(401)

    whom_id = get_user_id(username)
    if whom_id is None:
        abort(404)
    g.db.execute('insert into follower (who_id, whom_id) values (?, ?)',
                [session['user_id'], whom_id])
    g.db.commit()
    flash('"%s"님을 팔로우 합니다.' % username)
    return redirect(url_for('user_timeline', username=username))

# unfollow.
@app.route('/<username>/unfollow')
def unfollow_user(username):
    if not g.user:
        abort(401)
    whom_id = get_user_id(username)
    if whom_id is None:
        abort(404)
    g.db.execute('delete from follower where who_id=? and whom_id=?',
                [session['user_id'], whom_id])
    g.db.commit()
    flash('"%s"님을 언팔합니다.' % username)
    return redirect(url_for('user_timeline', username=username))

# 메시지 등록.
@app.route('/add_message', methods=['POST'])
def add_message():
    if 'user_id' not in session:
        abort(401)
    if request.form['text']:
        g.db.execute('''insert into message (author_id, text, pub_date)
                            values (?, ?, ?)''',
                        (session['user_id'], request.form['text'], int(time.time())))
        g.db.commit()
        flash('메시지가 등록되었습니다.')
    return redirect(url_for('timeline'))

# 로그인.
@app.route('/login', methods=['GET', 'POST'])
def login():

    # 로그인을 했으면, 타임라인을 보여주는 URL로 리디렉션.
    if g.user:
        return redirect(url_for('timeline'))

    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where username = ?''',
                [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'], request.form['password']):
            error = 'Invalid password'
        else:
            flash('로그인 성공:)')
            session['user_id'] = user['user_id']
            return redirect(url_for('timeline'))
    return render_template('login.html', error=error)

# 회원 가입.
@app.route('/register', methods=['GET', 'POST'])
def register():

    # 로그인을 했으면, 타임라인을 보여주는 URL로 리디렉션.
    if g.user:
        return redirect(url_for('timeline'))

    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'username을 입력해야 합니다.'
        elif not request.form['email'] or \
            '@' not in request.form['email']:
            error = '유효한 이메일 주소를 입력해야합니다.'
        elif not request.form['password']:
            error = 'password를 입력해야 합니다.'
        elif request.form['password'] != request.form['password2']:
            error = '두 암호가 일치하지 않습니다.'
        elif get_user_id(request.form['username']) is not None:
            error = 'username은 이미 사용 중입니다.'
        else:
            g.db.execute('''insert into user (username, email, pw_hash) 
                                values(?, ?, ?)''',
                            [request.form['username'], request.form['email'],
                             generate_password_hash(request.form['password'])])
            g.db.commit()
            flash('회원가입 성공! 지금 로그인 가능합니다.')

            # 로그인 페이지로 리디렉션.
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

# 로그아웃.
@app.route('/logout')
def logout():
    flash('로그아웃 되었습니다.')
    session.pop('user_id', None)
    return redirect(url_for('public_timeline'))

# 신사에서 필터 추가.
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url

if __name__ == '__main__':
    init_db()
    app.run()


    








