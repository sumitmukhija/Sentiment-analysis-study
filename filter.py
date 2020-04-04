import twint
import pandas as pd
import nest_asyncio

nest_asyncio.apply()

def get_dataframe(file_name='iava.csv'):
    return pd.read_csv(file_name)

def get_list_of_usernames_from_dataframe(df):
    if df is not None and df['username'] is not None:
        return (list(df['username']))
    else:
        return []

def get_bio_for_each_user_from_list(users):
    list_of_filtered_vets = list()
    for user in users[:5]:
        c = twint.Config()
        print("Going for user ", user)
        c.Username = "sumitmukhija"
        c.Hide_output = True
        c.Pandas = True
        twint.run.Lookup(c)
        df2 = twint.storage.panda.User_df
        print(df2.shape)
        twint.storage.panda.clean()
        twint.run.Lookup(c)
        df = twint.storage.panda.User_df
        print(df)
        # user = twint.output.users_list[0]
        # bio = user.bio
        # if user.tweets > 0:
        #     # or 'veteran' in bio.lower() or 'army' in bio.lower()
        #     # filtered_veteran = dict()
        #     # filtered_veteran['username'] = user
        #     # filtered_veteran['bio'] = bio.lower()
        #     # filtered_veteran['name'] = user.name.lower()
        #     # print(filtered_veteran)
        #     print(user.name)
        #     list_of_filtered_vets.append(user)
        
    print(list_of_filtered_vets)
    df = pd.DataFrame(list_of_filtered_vets)
    df.to_excel("step_2.xlsx")
    print("Fin.")

def test_usr(name='sumitmukhija'):
    c = twint.Config()
    c.Username = name
    c.Hide_output = True
    c.Store_object = True
    twint.run.Lookup(c)
    user = twint.output.users_list[0]
    print(dir(user))
    print(user.tweets)

if __name__ == "__main__":
    users = get_list_of_usernames_from_dataframe(get_dataframe())
    if len(users) > 0:
        get_bio_for_each_user_from_list(users)

    











