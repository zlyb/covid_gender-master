import requests
import json
from pymongo import MongoClient
from covid_gender.config import *
import pandas as pd


# Author detail info
# https://dev.acemap.info/api/v2/author/info?id=1018175185
# {
#   "id": 1018175185,
#   "name": "Xinbing Wang",
#   "paper_count": 454,
#   "citation_count": 6059,
#   "hindex": 39,
#   "conference_count": 228,
#   "journal_count": 198,
#   "avatar": "https://dev.acemap.info/api/v2/img/default/author.png",
#   "affiliation": [
#     {
#       "id": 2103723062,
#       "name": "Shanghai Jiao Tong University"
#     }
#   ],
#   "field":
#   "citation_statistic":
#   "map":
#  }
def request_author(author_id=None):
    url = 'https://dev.acemap.info/api/v2/author/info?id={}'.format(author_id)
    headers = {"Accept": "application/json"}
    res = requests.get(url, headers=headers)
    author_info = json.loads(res.text)
    return author_info


# Affiliation detail info
# // https://dev.acemap.info/api/v2/affiliation/info?id=2103723062
#
# { "id": 2103723062, "name": "Shanghai Jiao Tong University", "introduction": "Shanghai Jiao Tong University (SJTU;
# Chinese: 上海交通大学) is a major research university in Shanghai. Established in 1896 as Nanyang Public School by an
# imperial edict issued by the Guangxu Emperor, it has been referred to as 'The MIT of the East' since the 1930s. It
# is one of the nine members of the elite C9 League,and is a Chinese Ministry of Education Class A Double First Class
# University.", "url": "http://www.sjtu.edu.cn/", "logo":
# "https://dev.acemap.info/api/v2/img/affiliation/2103723062.jpg" }
def request_affiliation(affiliation_id=None):
    url = 'https://dev.acemap.info/api/v2/affiliation/info?id={}'.format(affiliation_id)
    headers = {"Accept": "application/json"}
    res = requests.get(url, headers=headers)
    affiliation_info = json.loads(res.text)
    return affiliation_info


def extract_author_name(df):
    author_info = request_author(df['first_author_id'])
    author_name = author_info.get('name')
    if author_name is None:
        first_author_fullname = ''
    else:
        author_name = str(author_name)
        name_list = author_name.split()
        result = name_list[:-1]
        result.insert(0, name_list[-1])
        first_author_fullname = ''.join(result)
    return first_author_fullname


def extract_affiliation_name(df):
    affiliation_info = request_affiliation(df['first_affiliation_id'])
    affiliation_name = affiliation_info.get('name')
    return affiliation_name


# client = MongoClient(MONGO_URL, username=USERNAME, password=PASSWORD)
# db = client[MONGO_DB]
# # mongodb返回指定字段<field> 1: 包括; 0: 排除
# # result = db.country.find({"country_id": '2140066376'},
# #                          {'name': 1, 'name_cn': 1})
# result = db.paper_info.find({"first_country_id": 2140066376},
#                             {'title': 1, 'paper_id': 1, 'date': 1, 'first_author_id': 1, 'first_affiliation_id': 1}
#                             )
# df_result = pd.DataFrame(list(result))
# df_result.to_csv("../data/paper_info.csv")

df_test = pd.read_csv("../data/paper_info.csv")
df_test['first_author_fullname'] = df_test.apply(lambda r: extract_author_name(r), axis=1)
df_test['first_affiliation_name'] = df_test.apply(lambda r: extract_affiliation_name(r), axis=1)
df_test.to_csv("../data/paper_info_result.csv")

