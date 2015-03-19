# Rubi Yanto - C00163855 - 28/11/2014

from flask import Flask, render_template, url_for, request, redirect, flash, session
import WGFunction
import time
import os
import pickle

APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top
#APP_STATIC = os.path.join(APP_ROOT, 'static')

app = Flask(__name__)
app.secret_key = '123456'


@app.route('/')
def display_home():
    mydict = os.path.join(APP_ROOT, WGFunction.WGFunction.urlOfDict07)
    count = WGFunction.WGFunction.countOfDict07
    word = WGFunction.get_random_word(mydict, count)
    session['finished'] = False
    session['word'] = word
    session['time'] = time.time();
    return render_template("home.html",
                           word=word,
                           numberOfGuesses=range(1, 8),
                           action=url_for('check'))


@app.route('/action', methods=["POST"])
def check():
    if (request.method == 'POST'):
        guesses = request.form.getlist('guess')
        checks = []
        for guess in guesses:
            result = None
            if WGFunction.WGFunction.is_guessword_in_word(guess, session['word']):
                if WGFunction.WGFunction.is_word_in_dict(guess,
                                                         os.path.join(APP_ROOT, WGFunction.WGFunction.urlOfDict03)):
                    result = 'yes'
                elif WGFunction.WGFunction.is_word_in_dict(guess,
                                                           os.path.join(APP_ROOT, WGFunction.WGFunction.urlOfDict07)):
                    result = 'yes'
                else:
                    result = 'no'
            else:
                result = 'no'
            checks.append({'word': guess,
                           'result': result})

        word_guess = set(guesses)
        for check in checks:
            if check['word'] in word_guess:
                word_guess = [x for x in word_guess if x != check['word']]
            else:
                check['result'] = 'duplicate word'

        allCorrect = True
        for check in checks:
            if check['result'] != 'yes':
                allCorrect = False

        if allCorrect:
            session['time'] = time.time() - session['time']
        return render_template("checkWord.html",
                               checks=checks,
                               correct=allCorrect,
                               time=session['time'],
                               action=url_for('rank'))


@app.route('/rank', methods=["POST"])
def rank():
    if session['finished']:
        return redirect(url_for('display_home'))

    file_name = os.path.join(APP_ROOT, 'rank.txt')
    fo = None
    rank_list = []
    if os.path.isfile(file_name):
        fo = open(file_name, 'rb')
        rank_list = pickle.load(fo)
        fo.close()
    rank_list.append({'name': request.form.get('name'),
                      'time': session['time'],
                      'id': len(rank_list) + 1})

    fo = open(file_name, 'wb')
    pickle.dump(rank_list, fo)
    fo.close()

    session['finished'] = True
    sorted_list = sorted(rank_list, key=lambda x: x['time'])
    my_rank = None
    count = 1
    id = len(sorted_list)
    for rank in sorted_list:
        if id == rank['id']:
            my_rank = {
                'id': id,
                'name': rank['name'],
                'time': rank['time'],
                'rank': count
            }
        count += 1
    return render_template("rankList.html",
                           rankList=sorted_list,
                           myRank=my_rank)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
