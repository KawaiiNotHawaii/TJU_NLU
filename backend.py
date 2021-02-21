from flask import Flask, render_template, jsonify, request
from databaseConn import MySqlHelper

app = Flask(__name__)

sqlh = MySqlHelper()
sqlh.connect()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/fetch', methods=['GET'])
def fetch_randomly():
    # data = sqlh.query_randomly_demo("novels")
    # message = {'id':data[0], 'context':data[1], 'targetSentence':data[2], 'targetWord':data[3]}
    (data, hasContext) = sqlh.fetch_randomly()
    message = {'id':data[0], 'context':data[1], 'targetSentence':data[2], 'targetWord':data[3], 'hasContext':hasContext}
    print((data, hasContext))
    return jsonify(message)  # serialize and use JSON headers

@app.route('/post', methods=['POST'])
def post_to_db():
    if (request.is_json):
        request_data = request.get_json()
        novel_id  = int(request_data["novel_id"])
        user_id = int(request_data["user_id"])
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
