from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)

def save(pre_base):
    s = session()
    rows = s.query(News).filter(not News.label).all()
    labels = []
    for row in rows:
        labels.append(row.title)
    for cur_row in pre_base:
        if cur_row['title'] not in labels:
            news = News(title=cur_row['title'],
                        author=cur_row['author'],
                        url=cur_row['url'],
                        points=cur_row['points'],
                        comments=cur_row['comments'])
            s.add(news)
    s.commit()

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)
