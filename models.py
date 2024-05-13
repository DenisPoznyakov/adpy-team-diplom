import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'vk_user'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False, unique=True)
    first_name = sq.Column(sq.String(length=50), nullable=False)
    last_name = sq.Column(sq.String(length=50), nullable=False)
    city = sq.Column(sq.String(length=20), nullable=False)
    age = sq.Column(sq.Integer, nullable=False)
    gender = sq.Column(sq.String(length=10), nullable=False)


class Favorites(Base):
    __tablename__ = 'favorites'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, nullable=False, unique=True)
    first_name = sq.Column(sq.String(length=50), nullable=False)
    last_name = sq.Column(sq.String(length=50))
    link = sq.Column(sq.String(length=100), unique=True, nullable=False)


class UserFavorites(Base):
    __tablename__ = 'user_favorites'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey(User.id), nullable=False)
    favorite_id = sq.Column(sq.Integer, sq.ForeignKey(Favorites.id), nullable=False)

    user = relationship(User, backref='user_favorites')
    favorites = relationship(Favorites, backref='user_favorites')


class Photos(Base):
    __tablename__ = 'photos'

    id = sq.Column(sq.Integer, primary_key=True)
    favorite_id = sq.Column(sq.Integer, sq.ForeignKey(Favorites.id), nullable=False)
    link = sq.Column(sq.String(length=100), unique=True, nullable=False)

    favorites = relationship(Favorites, backref='photos')


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


def create_tables(engine):
    '''
    Создание таблиц
    '''
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
