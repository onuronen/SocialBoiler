import logging
import pandas as pd
from sqlalchemy import func, create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.db.models import User_Credentials, Base, Profile_Page, Posts, Likes, Topics, Comments
from src.config import postgres_config

logger = logging.getLogger(__name__)
conn_str = f"postgresql://{postgres_config['user']}:{postgres_config['password']}@{postgres_config['host']}/{postgres_config['database']}"
engine = create_engine(conn_str)
Session = sessionmaker(bind=engine)

def create_tables():
    logger.info("Creating the database if it does not already exist")
    Base.metadata.create_all(bind=engine)


def fetch_rows(BaseClass):
    """
    :param BaseClass: Base child-class object from /src/db/models.py
    :returns: pandas.DataFrame
    """
    session = Session()

    try:
        result = session.query(BaseClass)

    finally:
        session.close()

    if result is not None:
        df = pd.read_sql(result.statement, result.session.bind)
        return df

    else:
        return None


def update_table(new_df, BaseClass):
    """"
    :param new_df: pandas.DataFrame containing rows to be loaded into Postgres
    :param BaseClass: Base child-class (sqlalchemy model)

    """""

    session = Session()
    session.bulk_insert_mappings(
        BaseClass,
        new_df.to_dict(orient="records"))
    session.commit()
    session.close()

def update_authentication_token(BaseClass, username, token):
    """
    :param BaseClass: Base child-class (sqlalchemy model)
    :param email: Email whose authentication token will be updated
    :param token: token assigned to user in each login
    """
    session = Session()
    session.query(BaseClass).filter(BaseClass.username == username).update({BaseClass.auth_token: token})
    session.commit()
    session.close()


# def update_user_profile(BaseClass, email, phone_number, age, about):
def update_user_profile(BaseClass, username, email, phone_number, age, about):
    """
    :param BaseClass: Base child-class (sqlalchemy model)
    :param email: Email whose authentication token will be updated
    :param token: token assigned to user in each login
    """
    session = Session()
    session.query(BaseClass).filter(BaseClass.username == username).update(
        {
            BaseClass.email: email,
            BaseClass.phone_number: phone_number,
            BaseClass.age: age,
            BaseClass.about: about
        }
    )
    session.commit()
    session.close()

def update_profile_avatar(BaseClass, username, image):
    # print("here: ", image)
    session = Session()
    session.query(BaseClass).filter(BaseClass.username == username).update(
        {
           BaseClass.image: image
        }
    )
    session.commit()
    session.close()

# Update user email in credentials
def update_user_credentials(BaseClass, username, email):
    session = Session()

    session.query(BaseClass).filter(BaseClass.username == username).update(
        {
            BaseClass.email: email,

        }
    )
    session.commit()
    session.close()


def delete_rows(BaseClass, username):
    session = Session()
    session.query(BaseClass).filter(BaseClass.username == username).delete()
    session.commit()
    session.close()

def delete_account_likes(post_id):
    session = Session()
    session.query(Likes).filter(Likes.post_id == post_id).delete()
    session.commit()
    session.close()

def fetch_post(BaseClass, post_id):
    session = Session()

    try:
        result = session.query(BaseClass).filter(BaseClass.post_id == post_id)

    finally:
        session.close()

    if result is not None:
        df = pd.read_sql(result.statement, result.session.bind)
        return df

    else:
        return None


# Update post likes and dislikes
def update_post_likes(post_id, like, dislike):
    session = Session()

    session.query(Posts).filter(Posts.post_id == post_id).update(
        {
            Posts.likes: like,
            Posts.dislikes: dislike

        }
    )
    session.commit()
    session.close()


def delete_row_likes(BaseClass, post_id, username):
    session = Session()
    session.query(BaseClass).filter(BaseClass.post_id == post_id).filter(BaseClass.username == username).delete()
    session.commit()
    session.close()

def delete_post_likes_or_comments(BaseClass, post_id):
    session = Session()
    session.query(BaseClass).filter(BaseClass.post_id == post_id).delete()
    session.commit()
    session.close()

def update_followers(BaseClass, username, followed_username, user_following, followed_followers):
    session = Session()

    session.query(BaseClass).filter(BaseClass.username == username).update(
        {
            BaseClass.following: user_following,
        }
    )
    session.query(BaseClass).filter(BaseClass.username == followed_username).update(
        {
            BaseClass.followers: followed_followers,
        }
    )
    session.commit()
    session.close()

# Update/ Create topic
def update_topic(BaseClass, topic, posts):
    # check  procedure if query returns nothing
    session = Session()
    query = session.query(BaseClass).filter(BaseClass.topic_title == topic)
    res = query.first()
    if res is None:
        row = Topics(topic_title=topic, posts_ids = posts)
        session.add(row)
    else:
        query.update(
            {
            BaseClass.topic_title: topic,
            BaseClass.posts_ids: posts
            }
        )
    session.commit()
    session.close()

#update a user's followed topics
def update_user_topics(BaseClass, username, topics):
    session = Session()
    session.query(BaseClass).filter(BaseClass.username == username).update(
            {
            BaseClass.topics_following: topics
            }
    )
    session.commit()
    session.close()

def fetch_user_post(username):
    session = Session()

    try:
        result = session.query(Posts).filter(Posts.username == username)

    finally:
        session.close()

    if result is not None:
        df = pd.read_sql(result.statement, result.session.bind)
        return df

    else:
        return None

def fetch_posts_with_topic(topic):
    session = Session()

    try:
        result = session.query(Posts).filter(Posts.topics == topic)

    finally:
        session.close()

    if result is not None:
        df = pd.read_sql(result.statement, result.session.bind)
        return df

    else:
        return None


def fetch_users_following(username):
    session = Session()

    try:
        result = session.query(User_Credentials.following).filter(User_Credentials.username == username)

    finally:
        session.close()

    if result is not None:
        df = pd.read_sql(result.statement, result.session.bind)
        return df

    else:
        return None

def fetch_topics_following(username):
    session = Session()

    try:
        result = session.query(User_Credentials.topics_following).filter(User_Credentials.username == username)

    finally:
        session.close()

    if result is not None:
        df = pd.read_sql(result.statement, result.session.bind)
        return df

    else:
        return None

# fetches the votes by the user
def fetch_votes_by_user(username):
    session = Session()

    try:
        result = session.query(Likes).filter(Likes.username == username)

    finally:
        session.close()

    if result is not None:
        df = pd.read_sql(result.statement, result.session.bind)
        return df

    else:
        return None


def delete_topics_data():
    session = Session()
    session.query(Topics).delete()
    session.commit()
    session.close()


def fetch_comments_by_user(username, post_id):
    session = Session()

    try:
        result = session.query(Comments).filter(Comments.username == username).filter(Comments.post_id == post_id)

    finally:
        session.close()

    if result is not None:
        df = pd.read_sql(result.statement, result.session.bind)
        return df

    else:
        return None


def update_post_bookmarked(post_id, bookmarked_users):
    session = Session()
    session.query(Posts).filter(Posts.post_id == post_id).update(
            {
            Posts.bookmarked: bookmarked_users
            }
    )
    session.commit()
    session.close()

   
#create_tables()

if __name__ == '__main__':
    pass
