from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session, save
from bayes import NaiveBayesClassifier

# constants
s = session()
classifier = NaiveBayesClassifier()
mark_news = s.query(News).filter(News.label != None).all()
x_title = [row.title for row in mark_news]
y_lable = [row.label for row in mark_news]
classifier.fit(x_title, y_lable)


@route('/')
@route('/news')
def news_list():
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    row_id = request.query.id
    row = s.query(News).filter(News.id == row_id).one()
    row.label = label
    s.commit() # сохраняем все в базу
    if request.query.classify == 'True':
        redirect('/classify')
    else:
        redirect('/news')


@route('/update')
def update_news():
    save(get_news('https://news.ycombinator.com/newest', 1))
    redirect('/')


@route('/classify')
def classify_news():
    recently_mark_news = s.query(News).filter(News.title not in x_title and News.label != None).all()
    title_extra = [row.title for row in recently_mark_news]
    label_extra = [row.label for row in recently_mark_news]
    classifier.fit(title_extra, label_extra)
    not_mark_news = s.query(News).filter(News.label == None).all() # отбираем все новости, у которых нет лейбла
    x = [row.title for row in not_mark_news]
    labels = classifier.predict(x) # пытаемся определить какой лейбл будет у новости
    for i in range(len(not_mark_news)):
        not_mark_news[i].label = labels[i]
    s.commit() # сохраняем в базу данных
    classified_news = s.query(News).filter(News.label == 'good').all()
    return template('classify_template', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
