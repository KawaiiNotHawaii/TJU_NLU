from flask import Flask, render_template, jsonify, request, url_for, redirect, session, flash
from databaseConn import MySqlHelper
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

sqlh = MySqlHelper()
sqlh.connect()

@app.route('/')
def route():
    if session.get('user_id'):
        print('Already logged in as:', session.get('user_id'))
        return render_template('home.html')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET'])
def login():
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

                code = sqlh.login_validation(user_id, pwd)
                if (code == 0):
                    session['user_id'] = user_id
                    session.permanent = True
                    print('登陆成功')
                    return redirect('/')
                elif (code == 1):
                    print('密码错误')
                elif (code == 2):
                    print('用户名不存在')
            except:
                print("用户名必须为数字:")
                return redirect('/login')
        else:
            print('用户名、密码不能为空')
    return redirect('/login')

@app.route('/fetch', methods=['GET'])
def fetch_randomly():
    # data = sqlh.query_randomly_demo("novels")
    # message = {'id':data[0], 'context':data[1], 'targetSentence':data[2], 'targetWord':data[3]}
    res = sqlh.fetch_randomly()
    if (res is None):
        message = {'id':data[0], 'context':'所有数据均已标注完成！', 'targetSentence':'所有数据均已标注完成！', 'targetWord':data[3], 'hasContext':hasContext}
        return jsonify(message)
    else:
        (data, hasContext) = res
        message = {'id':data[0], 'context':data[1], 'targetSentence':data[2], 'targetWord':data[3], 'hasContext':hasContext}
        print(res)
        return jsonify(message)  # serialize and use JSON headers

@app.route('/post', methods=['POST'])
def post_to_db():
    if (request.is_json):
        request_data = request.get_json()
        novel_id  = int(request_data["novel_id"])
        user_id = session.get('user_id')
        print('Guess recieved, annotater ID:', user_id)
        hasContext = bool(int(request_data["hasContext"]))
        guess = request_data["guess"]
        isRight = bool(int(request_data["isRight"]))

        print("novel_id:", novel_id, "; user_id:", user_id, "; hasContext:", hasContext, "; guess:", guess, "; isRight:", isRight)
        sqlh.insert_into_guesses(novel_id, user_id, hasContext, guess, isRight)

        if isRight:
            if hasContext:
                print("Guess WITH context is RIGHT, update (hitTimesInContext)")
                sqlh.update_times_col(novel_id, "hitTimesInContext")
            else:
                print("Guess WITHOUT context is RIGHT, delete from table output_novels")
                sqlh.delete_from_outputNovels(novel_id)
        else:
            if hasContext:
                print("Guess WITH context is WRONG, delete from table output_novels")
                sqlh.delete_from_outputNovels(novel_id)
            else:
                print("Guess WITHOUT context is WRONG, update (missTimesWithoutContext)")
                sqlh.update_times_col(novel_id, "missTimesWithoutContext")

        # TODO: database operations here

    return jsonify({'message':'Got it.'})

if __name__ == "__main__":
    app.run(debug=True, threaded=False)
