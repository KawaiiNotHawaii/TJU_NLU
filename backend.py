# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request, url_for, redirect, session, flash
from databaseConn import MySqlHelper
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
sqlh = MySqlHelper()
sqlh.connect()


@app.route('/')
def route():
    if session.get('user_id') is not None:
        print('Already logged in as:', session.get('user_id'))
        return render_template('home.html')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET'])
def login():
    print("success")
    return render_template('login.html')

@app.route('/validate', methods=['GET', 'POST'])
def validate():
    if request.method == 'POST':
        # data = request.get_json()
        # user_id = data.get('user_id')
        # pwd = data.get('pwd')

        user_id = request.form.get('user_id')
        pwd = request.form.get('pwd')

        print("Form data recieved. User id:", user_id, "password:", pwd)

        if all([user_id, pwd]):
            try:
                user_id = int(user_id)
            except:
                message = '用户名必须为数字'
                print(message)
                flash(message)
            else:
                code = sqlh.login_validation(user_id, pwd)
                if (code == 0):
                    session['user_id'] = user_id
                    session.permanent = True

                    # TODO: double check
                    timer = 1000
                    while ((session.get('user_id') is None) and (timer != 0)):
                        session['user_id'] = user_id
                        session.permanent = True
                        timer -= 1
                    if(timer==0):
                        message = 'Session添加失败：Timeout. 请重新登陆。'
                        print(message)
                        flash(message)
                        return redirect('/login')

                    message = '登陆成功'
                    print("账号{}{}".format(user_id, message))
                    return redirect('/')
                elif (code == 1):
                    message = '密码错误'
                    print(message)
                    flash(message)
                elif (code == 2):
                    message = '用户名不存在'
                    print(message)
                    flash(message)

        else:
            message = '用户名或密码不能为空'
            print(message)
            flash('用户名或密码不能为空')
    return redirect('/login')

@app.route('/fetch', methods=['GET'])
def fetch_randomly():
    # data = sqlh.query_randomly_demo("novels")
    # message = {'id':data[0], 'context':data[1], 'targetSentence':data[2], 'targetWord':data[3]}

    # TODO: to be deleted
    # todo: add try catch to redirect if session.get fail!!!
    # print('Trying to get user_id in session in fetch_randomly():', session.get('user_id', "fail"))
    # if(session.get('user_id') is not None):
    res=-1

    # exception handler
    timer = 1000
    while (timer != 0):
        if (session.get('user_id') is not None):
            res = sqlh.fetch_randomly(session.get('user_id'))
            break
        timer -= 1
    if(timer==0):
        message = '用户ID获取失败：Timeout. 请重新登陆。'
        print("In fetch_randomly()", message, session.get('user_id'))
        flash(message)
        return jsonify({'state':-1, 'message':message})

    if (res is None):
        message = {'isFinished':True}
        return jsonify(message)
    else:
        (data, hasContext) = res

        message = {'id':data[0], 'context':data[1] + data[2], 'targetWord':data[3], 'extra':data[4], 'hasContext':hasContext}
        print(message)
        return jsonify(message)  # serialize and use JSON headers

@app.route('/post', methods=['POST'])
def post_to_db():
    print("recieved the posted guess!")
    if (request.is_json):
        request_data = request.get_json()
        novel_id  = int(request_data["novel_id"])
        user_id = -1

        # exception handler
        timer = 1000
        while (timer != 0):
            if (session.get('user_id') is not None):
                user_id = session.get('user_id')
                break
            timer -= 1
        if(timer==0):
            message = '用户ID获取失败：Timeout. 请重新登陆。'
            print("In post_to_db()", message, session.get('user_id'))
            flash(message)
            return jsonify({'state':-1, 'message':message})

        print('Guess recieved, annotater ID:', user_id)
        hasContext = bool(int(request_data["hasContext"]))
        guess = request_data["guess"]
        target_word = request_data['t_word']
        isRight = bool(int(request_data["isRight"]))

        print("novel_id:", novel_id, "; user_id:", user_id, "; hasContext:", hasContext, "; guess:", guess, "; t_word:",target_word, "; isRight:", isRight)
        sqlh.insert_into_guesses(novel_id, user_id, hasContext, guess, target_word,  isRight)

        sqlh.update_times_col("output_novels{}".format(user_id), novel_id, "hitTimesInContext")
        # '''
        # if isRight:
        #     if hasContext:
        #         print("Guess WITH context is RIGHT, update (hitTimesInContext)")
        #         sqlh.update_times_col(novel_id, "hitTimesInContext")
        #     else:
        #         print("Guess WITHOUT context is RIGHT, delete from table output_novels")
        #         sqlh.delete_from_outputNovels(novel_id)
        # else:
        #     if hasContext:
        #         print("Guess WITH context is WRONG, delete from table output_novels")
        #         sqlh.delete_from_outputNovels(novel_id)
        #     else:
        #         print("Guess WITHOUT context is WRONG, update (missTimesWithoutContext)")
        #         sqlh.update_times_col(novel_id, "missTimesWithoutContext")
        # '''

        # TODO: database operations here

    return jsonify({'state':1})

if __name__ == "__main__":
    app.run(debug=True, threaded=False)
