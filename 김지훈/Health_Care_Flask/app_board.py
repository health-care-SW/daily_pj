from flask import Flask, render_template, request, redirect, url_for, g, jsonify, redirect, url_for
import Board
import math
from __main__ import app

ROWS_PER_PAGE = 20

#게시글 리스트
@app.route('/boardlist')
def boardlist():
    #로그인 체크
    if g.user == None:
        return redirect(url_for("hello"))

    pageNum = request.args.get('page', default=1, type = int)
    articlelist = Board.select_board_paging(pageNum, ROWS_PER_PAGE)
    max_page = math.ceil(articlelist.total / ROWS_PER_PAGE)

    start_page = max(1, pageNum - 5)
    end_page = min(pageNum + 5, max_page)

    #print(f'start: {start_page}, end: {end_page}')
    #print(articlelist[0].board_title)

    return render_template("boardlist.html", articlelist = articlelist,
                            nowPage = pageNum,
                            start_page = start_page,
                            end_page = end_page)

#게시글 작성
@app.route('/boardwrite', methods = ["GET", "POST"])
def boardwrite():
    #로그인 체크
    if g.user == None:
        return redirect(url_for("hello"))

    if request.method == 'GET':
        return render_template("boardwrite.html")

    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("content")
        article = Board.Board(title, content)

        #print(f'post content: {content}, title: {title}')
        Board.insert_board(article)
        return redirect(url_for("boardlist"))

    

# 게시글 열람
@app.route('/boarddetail/<id>')
def boarddetail(id):
    #로그인 체크
    if g.user == None:
        return redirect(url_for("hello"))

    article = Board.select_board_with_id(id)
    return render_template("boarddetail.html", article = article)


# 게시글 삭제
@app.route('/boarddelete')
def boardDelete():
    #로그인 체크
    if g.user == None:
        return redirect(url_for("hello"))

    board_id = request.args.get("board_id")
    Board.delete_board_with_id(board_id)

    return redirect(url_for("boardlist"))


