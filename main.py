# import pandas as pd
from utils.Cleaner import Cleaner
from utils.TWManager import TWManager
from utils.PicMaker import PicMaker

if __name__ == '__main__':
    twm = TWManager()

    twm.auth_user()

    df = twm.tweets_df_auth_user()

    # df = twm.tweets_df_by_user("<USERNAME>")

    # df = pd.read_json(
    #     "data.json",
    #     orient='index',
    #     keep_default_dates=False,
    #     convert_dates=False,
    #     convert_axes=False
    # )
    #
    # df.reset_index(inplace=True)
    # df = df.rename(columns={'index': 'tweet_id'})

    cleaner = Cleaner()

    df = cleaner.clean_up(df)

    pm = PicMaker(url="<URL>/index")

    pm.generate_image_from_df(df)
