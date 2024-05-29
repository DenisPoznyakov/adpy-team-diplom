from db.models import Base
from db.models import User, Favorites, UserFavorites, BlackList, UserBlackList
from db.database import session, engine


def create_tables():
    """Создание таблиц"""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def add_user(user):
    """Добавление пользователя в БД"""
    with session() as sess:
        check = sess.query(User.id).filter(User.user_id == user.user_id).first()
        if not check:
            new_user = User(user_id=user.user_id,
                            first_name=user.first_name,
                            last_name=user.last_name,
                            city=user.city,
                            age=user.age)
            sess.add(new_user)
            sess.commit()


def add_or_del_favorite(user, favorite):
    """Добавление или удаление избранного пользователя и связи с user_favorites"""
    with session() as sess:
        check_favorite = sess.query(Favorites).filter(Favorites.user_id == favorite.user_id).first()
        user_id = sess.query(User.id).filter(User.user_id == user.user_id).first()[0]

        if not check_favorite:
            new_favorite = Favorites(user_id=favorite.user_id,
                                     first_name=favorite.first_name,
                                     last_name=favorite.last_name,
                                     link=favorite.link
                                     )

            sess.add(new_favorite)
            sess.commit()

            favorite_id = sess.query(Favorites.id).filter(Favorites.user_id == favorite.user_id).first()[0]
            new_user_favorite = UserFavorites(user_id=user_id, favorite_id=favorite_id)
            sess.add(new_user_favorite)
            sess.commit()
        else:
            favorite_id = sess.query(Favorites.id).filter(Favorites.user_id == favorite.user_id).first()[0]
            check_user_favorite = sess.query(UserFavorites).filter((UserFavorites.user_id == user_id) &
                                                                   (UserFavorites.favorite_id == favorite_id)).first()
            if not check_user_favorite:
                new_user_favorite = UserFavorites(user_id=user_id, favorite_id=favorite_id)
                sess.add(new_user_favorite)
                sess.commit()
            else:
                sess.query(UserFavorites).filter((UserFavorites.user_id == user_id) &
                                                 (UserFavorites.favorite_id == favorite_id)).delete()
                sess.commit()


def check_user_in_favorites(user_id, favorite_id):
    """Проверяет есть ли пользователь в избранных"""
    with session() as sess:
        check_favorites = sess.query(Favorites).filter(Favorites.user_id == favorite_id).first()
        if check_favorites:
            us_id = sess.query(User.id).filter(User.user_id == user_id).first()[0]
            fv_id = sess.query(Favorites.id).filter(Favorites.user_id == favorite_id).first()[0]
            check_user_favorites = sess.query(UserFavorites).filter((UserFavorites.user_id == us_id) &
                                                                    (UserFavorites.favorite_id == fv_id)).first()
            if check_user_favorites:
                return True
            return False
        return False


def check_user_in_blacklist(user_id, blacklist_id):
    """Проверяет есть ли пользователь в черном списке"""
    with session() as sess:
        check_blacklist = sess.query(BlackList).filter(BlackList.user_id == blacklist_id).first()
        if check_blacklist:
            us_id = sess.query(User.id).filter(User.user_id == user_id).first()[0]
            bl_id = sess.query(BlackList.id).filter(BlackList.user_id == blacklist_id).first()[0]
            check_user_blacklist = sess.query(UserBlackList).filter((UserBlackList.user_id == us_id) &
                                                                    (UserBlackList.blacklist_id == bl_id)).first()
            if check_user_blacklist:
                return True
            return False
        return False


def add_blacklist(user, blacklist_id):
    """Добавление в черный список и связи user_blacklist"""
    with session() as sess:
        check_blacklist = sess.query(BlackList).filter(BlackList.user_id == blacklist_id).first()
        user_id = sess.query(User.id).filter(User.user_id == user.user_id).first()[0]

        if not check_blacklist:
            new_blacklist = BlackList(user_id=blacklist_id)
            sess.add(new_blacklist)
            sess.commit()

            blacklist_id = sess.query(BlackList.id).filter(BlackList.user_id == blacklist_id).first()[0]
            new_user_blacklist = UserBlackList(user_id=user_id, blacklist_id=blacklist_id)
            sess.add(new_user_blacklist)
            sess.commit()
        else:
            blacklist_id = sess.query(BlackList.id).filter(BlackList.user_id == blacklist_id).first()[0]
            check_user_blacklist = (sess.query(UserBlackList)
                                    .filter((UserBlackList.user_id == user_id) &
                                            (UserBlackList.blacklist_id == blacklist_id)).first())
            if not check_user_blacklist:
                new_user_blacklist = UserBlackList(user_id=user_id, blacklist_id=blacklist_id)
                sess.add(new_user_blacklist)
                sess.commit()


def get_favorites(user):
    """Получение избранных пользователей"""
    with session() as sess:
        user_id = sess.query(User.id).filter(User.user_id == user.user_id)
        all_favorites = (sess.query(Favorites)
                         .join(UserFavorites.favorites)
                         .filter(UserFavorites.user_id == user_id).all())
        return all_favorites


def del_user(user_id):
    """Удаление пользователь из БД"""
    with session() as sess:
        us_id = sess.query(User.id).filter(User.user_id == user_id).first()[0]
        sess.query(UserFavorites).filter(UserFavorites.user_id == us_id).delete()
        sess.query(UserBlackList).filter(UserBlackList.user_id == us_id).delete()
        sess.query(User).filter(User.user_id == user_id).delete()
        sess.commit()
