from utils.Cleaner import Cleaner
from utils.TWManager import TWManager
from utils.PfpManager import PicMaker

if __name__ == '__main__':
    twm = TWManager()

    '''
        Step 1: Authorize User
    '''
    twm.auth_user()

    '''
        Step 2: Fetch Tweets of User
    '''
    df = twm.tweets_df_auth_user()

    '''
        Step 3: Clean and Tokenize Tweets
    '''
    cleaner = Cleaner()

    df = cleaner.clean_up(df)

    '''
        Step 4: Generate Profile Picture Using Tokenized Tweets
    '''
    pm = PicMaker(url="<URL>/index")

    pm.generate_image_from_df(df)

    '''
        Step 5: Update Profile Picture of the User
    '''
    twm.update_auth_user_pfp("response.png")
