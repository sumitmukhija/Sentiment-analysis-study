import twint
import json
import pandas as pd
import csv

def get_dataframe(file_name='iava.csv'):
    return pd.read_csv(file_name)

def get_list_of_usernames_from_dataframe(df):
    if df is not None and df['username'] is not None:
        return (list(df['username']))
    else:
        return []

def get_filtered_soldiers():
    eligible_vets = list()
    with open('user_info.json') as json_file:
        data = json.load(json_file)
        for vet in data:
            bio = vet['bio'].lower()
            tweets = vet['tweets']
            join_year = int(vet['join_date'].split(' ')[-1])
            if ('army' in bio or 'veteran' in bio or 'soldier' in bio or 'military' in bio) and ('organization' not in bio and 'group' not in bio) and tweets > 50 and join_year < 2019:
                eligible_vets.append(vet)
        print(len(eligible_vets))

        with open('data/filtered_vets.json', 'w') as output:
            json.dump(eligible_vets, output)
            print("filtered_vets.json created. Contains all information. Use to verify. Don't use as input")

        with open('data/filtered_vets_username.csv', 'wb') as csv:
            csv.write('username'.encode())
            csv.write("\n".encode())
            for vet in eligible_vets:
                csv.write(vet['username'].encode())
                csv.write("\n".encode())
            print("filtered_vets_username.csv created. Contains username. Use as input")



if __name__ == "__main__":
    get_filtered_soldiers()
    # users = get_list_of_usernames_from_dataframe(get_dataframe())
    # if len(users) > 0:
    #     get_bio_for_each_user_from_list(users)










