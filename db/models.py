import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False, unique=True)
    first_name = sq.Column(sq.String(length=50), nullable=False)
    last_name = sq.Column(sq.String(length=50), nullable=False)
    city = sq.Column(sq.String(length=20), nullable=False)
    age = sq.Column(sq.Integer, nullable=False)


class Favorites(Base):
    __tablename__ = 'favorites'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False, unique=True)
    first_name = sq.Column(sq.String(length=50), nullable=False)
    last_name = sq.Column(sq.String(length=50))
    link = sq.Column(sq.String(length=100), unique=True, nullable=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}, ссылка - {self.link}'


class UserFavorites(Base):
    __tablename__ = 'user_favorites'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey(User.id), nullable=False)
    favorite_id = sq.Column(sq.Integer, sq.ForeignKey(Favorites.id), nullable=False)

    user = relationship(User, backref='user_favorites')
    favorites = relationship(Favorites, backref='user_favorites')


class BlackList(Base):
    __tablename__ = 'blacklist'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False, unique=True)


class UserBlackList(Base):
    __tablename__ = 'user_blacklist'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey(User.id), nullable=False)
    blacklist_id = sq.Column(sq.Integer, sq.ForeignKey(BlackList.id), nullable=False)

    user = relationship(User, backref='user_blacklists')
    blacklist = relationship(BlackList, backref='user_blacklists')


class UserVK:
    def __init__(self, user_id, first_name, last_name, city, age):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.age = age


class FavoriteVK:
    def __init__(self, user_id, first_name, last_name, link):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.link = link
