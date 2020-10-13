from src.db.crud import update_table, fetch_post, update_post_likes
from src.db.models import Posts, Likes
import pandas as pd
import datetime as dt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def insert_post_details(username, title, description, image, topics):
    data = {"username": [username], "title": [title], "description": [description], "image": [image], "likes": 0, "dislikes": 0,
            "date_created": dt.datetime.utcnow(), "topics": [topics]}

    new_df = pd.DataFrame(data)
    update_table(new_df, Posts)


def vote_post_db(post_id, username, liked, disliked):
    data = {"post_id": post_id, "username": [
        username], "liked": liked, "disliked": disliked}
    new_df = pd.DataFrame(data)
    update_table(new_df, Likes)

    post_df = fetch_post(Posts, post_id)
    likes = post_df.iloc[0]["likes"].item()
    dislikes = post_df.iloc[0]["dislikes"].item()

    if liked:
        likes += 1
    else:
        dislikes += 1

    update_post_likes(post_id, likes, dislikes)


#insert_post_details("onur", "asdsa", "aasdsads", "asdsada", "asdasdasddas")
#vote_post(6, "onur", True, False)
