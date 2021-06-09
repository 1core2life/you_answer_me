
from flask import Flask, jsonify, request, render_template, redirect, url_for
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


MAX_ANSWER_LEN = 3
MAX_QUESTION_LEN = 20

@app.route("/new")
@app.route("/")
def main():
    return render_template("new.html")

@app.route("/questioning/<name>", methods=['POST', 'GET'])
def questioning(name):
    max_length = int((Question().get_max_length())["cnt"])
    selected_question_list = list() 
    for num in range(0, MAX_QUESTION_LEN):
        while(True):
            random_num = random.randrange(1, max_length + 1)
            if random_num not in selected_question_list:
                selected_question_list.append(random_num)
                break


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



@app.route("/userQuestion/new", methods=['POST'])
def new_user_question():
    res = request.form["res"]
    name = request.form["name"]
    user_idx = User().insert(name)
    res = json.loads(res)

    for re in res:
        question_idx = re["question_idx"].split('_')[-1]
        UserQuestion().insert(question_idx, user_idx, re["answer"])
    
    user = User().select(user_idx)
    
    return jsonify({'code':user["code"]}), 200


@app.route("/share/<code>")
def share(code):
    return render_template("share.html")



@app.route("/answering/<code>")
def answering(code):
    user = User().select_code(code)

    return render_template("answering.html", user_idx=user["idx"], name=user["name"], code=code)


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
    
    return jsonify(None), 200


@app.route("/answerCard", methods=['POST'])
def answer_card():
    user_idx = request.form["user_idx"]
    result = list()

    questions = UserQuestion().select(user_idx)
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

    return render_template("question_card.html", result_list=result, answer=False)


@app.route("/userQuestion/answer/<code>", methods=['POST'])
def get_answer_user_question(code):
    user = User().select_code(code)
    user_idx = user["idx"]

    result = list()

    questions = UserQuestion().select(user_idx)
    for question in questions:
        formatted_questions = dict()
        formatted_questions["correct_answer"] = question["answer"]

        question = question["question_idx"]
        formatted_questions["question_idx"] = question

        q = Question().select(question)
        formatted_questions["question_content"] = q["content"]


        answers = QuestionAnswer().select(question)
        for idx in range(0, MAX_ANSWER_LEN):
            formatted_questions["answer_" + str(idx)] = answers[idx]["content"]
        
        result.append(formatted_questions)

    
    return render_template("question_card.html", result_list=result, answer=True)


@app.route("/result/<code>")
def result(code):
    user = User().select_code(code)
    user_idx = user["idx"]

    challenger_list = Challenger().select_all(user_idx)
    sorted_challenger_list = sorted(challenger_list, key=lambda k: k['score'], reverse=True) 

    questions = UserQuestion().select(user_idx)
    question_len = len(questions)
    
    return render_template("result.html", result_list=sorted_challenger_list, question_len=question_len)


@app.route("/result/<user_idx>/comment/new")
def new_comment(user_idx):
    # challenger_idx = session['challenger_idx']
    # comment = request.form["comment"]
    # Challenger().insert_comment(user_idx, challenger_idx, comment)

    return jsonify(None), 200




# admin
@app.route("/admin/question/new", methods=['POST'])
def admin_new_question():
    question = request.form["question"]
    answer_0 = request.form["answer_0"]
    answer_1 = request.form["answer_1"]
    answer_2 = request.form["answer_2"]

    question_idx = Question().insert(question)
    QuestionAnswer().insert(question_idx, answer_0)
    QuestionAnswer().insert(question_idx, answer_1)
    QuestionAnswer().insert(question_idx, answer_2)
    
    return jsonify(None), 200


@app.route("/admin/question/update", methods=['POST'])
def admin_update_question():
    question_idx = request.form["question_idx"]
    question = request.form["question"]
    answer_0 = request.form["answer_0"]
    answer_1 = request.form["answer_1"]
    answer_2 = request.form["answer_2"]

    Question().update(question_idx, question)

    answers = QuestionAnswer().select(question_idx)
    QuestionAnswer().update(answers[0]["idx"], answer_0)
    QuestionAnswer().update(answers[1]["idx"], answer_1)
    QuestionAnswer().update(answers[2]["idx"], answer_2)
    
    return jsonify(None), 200


@app.route("/admin/question/new/page")
def admin_question_new_page():
    return render_template("/admin/new_question.html")


@app.route("/admin/question/update/page")
def admin_question_update_page():
    return render_template("/admin/update_question.html")


@app.route("/admin/question/all/get", methods=['POST'])
def admin_get_all_question():
    questions = Question().select_all()
    
    result = list()

    for question in questions:
        formatted_questions = dict()
        formatted_questions["question_content"] = question["content"]
        
        question_idx = question["idx"]
        formatted_questions["question_idx"] = question_idx


        answers = QuestionAnswer().select(question_idx)
        for idx in range(0, MAX_ANSWER_LEN):
            formatted_questions["answer_" + str(idx)] = answers[idx]["content"]
        
        result.append(formatted_questions)

    return render_template("/admin/question_card.html", result_list=result)


@app.route("/admin/question/all")
def admin_all_question():
    return render_template("/admin/all_question.html")




if __name__ == '__main__':
    app.debug = True
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 80)))

