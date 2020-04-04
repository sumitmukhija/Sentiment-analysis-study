import twint
import pandas as pd


def get_dataframe(file_name='iava.csv'):
    return pd.read_csv(file_name)

def get_list_of_usernames_from_dataframe(df):
    if df is not None and df['username'] is not None:
        return (list(df['username']))
    else:
        return []

def get_bio_for_each_user_from_list(users):
    list_of_filtered_vets = list()
    c = twint.Config()
    for user in users:
        print("Going for user ", user)
        c.Username = user
        c.Hide_output = True
        c.Store_object = True
        twint.run.Lookup(c)
        user = twint.output.users_list[0]
        bio = user.bio
        if user.tweets > 50 and 'veteran' in bio.lower() or 'army' in bio.lower():
            filtered_veteran = dict()
            filtered_veteran['username'] = user
            filtered_veteran['bio'] = bio.lower()
            filtered_veteran['name'] = name.lower()
            list_of_filtered_vets.append(filtered_veteran)
        
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

    











