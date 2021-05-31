
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import os
from module.question import Question
from module.challenger import Challenger
from module.question_answer import QuestionAnswer
from module.user import User
from module.user_question import UserQuestion
from datetime import timedelta


import random
import json


app = Flask(__name__,  static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


MAX_ANSWER_LEN = 3

@app.route("/new")
def main():
    return render_template("new.html")

@app.route("/questioning/<name>", methods=['POST', 'GET'])
def questioning(name):
    max_length = int((Question().get_max_length())["cnt"])
    selected_question_list = list() 
    for num in range(0, int(max_length/2)):
        random_num = random.randrange(1, max_length + 1)
        if random_num not in selected_question_list:
            selected_question_list.append(random_num)


    return render_template("questioning.html", name=name, questions=selected_question_list)


@app.route("/questionCard", methods=['POST'])
def question_card():
    questions = request.form["questions"]
    result = list()

    for question in json.loads(questions):
        formatted_questions = dict()
        formatted_questions["question_idx"] = question

        q = Question().select(question)
        formatted_questions["question_content"] = q["content"]

        answers = QuestionAnswer().select(question)
        for idx in range(0, MAX_ANSWER_LEN):
            formatted_questions["answer_" + str(idx)] = answers[idx]["content"]
        
        result.append(formatted_questions)

    return render_template("question_card.html", result_list=result)



@app.route("/question/new", methods=['POST'])
def new_question():
    res = request.form["res"]
    name = request.form["name"]
    user_idx = User().insert(name)
    res = json.loads(res)
    for re in res:
        question_idx = re["question_idx"].split('_')[-1]
        UserQuestion().insert(question_idx, user_idx, re["answer"])
    
    return jsonify({'user_idx':user_idx}), 200


@app.route("/share/<user_idx>")
def share(user_idx):
    return render_template("share.html")



@app.route("/answering/<user_idx>")
def answering(user_idx):
    user = User().select(user_idx)

    return render_template("answering.html", user_idx=user_idx, name=user["name"])


@app.route("/answer/new", methods=['POST'])
def new_answer():
    res = request.form["res"]
    name = request.form["name"]
    user_idx = request.form["user_idx"]
    score = 0

    res = json.loads(res)
    #get score
    for re in res:
        question_idx = re["question_idx"].split('_')[-1]
        if UserQuestion().is_correct(user_idx, question_idx, re["answer"]):
            score = score + 1
        
    challenger_idx = Challenger().insert(user_idx, name, score)
    # session['challenger_idx'] = challenger_idx
    
    return jsonify(None), 200


@app.route("/answerCard", methods=['POST'])
def answer_card():
    user_idx = request.form["user_idx"]
    result = list()

    questions = UserQuestion().select_question_idx(user_idx)
    for question in questions:
        question = question["question_idx"]
        formatted_questions = dict()
        formatted_questions["question_idx"] = question

        q = Question().select(question)
        formatted_questions["question_content"] = q["content"]

        answers = QuestionAnswer().select(question)
        for idx in range(0, MAX_ANSWER_LEN):
            formatted_questions["answer_" + str(idx)] = answers[idx]["content"]
        
        result.append(formatted_questions)

    return render_template("question_card.html", result_list=result)


@app.route("/result/<user_idx>")
def result(user_idx):
    challenger_list = Challenger().select_all(user_idx)
    sorted_challenger_list = sorted(challenger_list, key=lambda k: k['score'], reverse=True) 

    questions = UserQuestion().select_question_idx(user_idx)
    question_len = len(questions)
    
    return render_template("result.html", result_list=sorted_challenger_list, question_len=question_len)


@app.route("/result/<user_idx>/comment/new")
def new_comment(user_idx):
    challenger_idx = session['challenger_idx']
    comment = request.form["comment"]
    Challenger().insert_comment(user_idx, challenger_idx, comment)

    return jsonify(None), 200





@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

if __name__ == '__main__':
    app.debug = True
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 80)))

