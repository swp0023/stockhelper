from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import requests

from stockhelper.config import APIKEY_FIFAONLINE4


api_v1_fifaonline4 = Blueprint('api_v1_fifaonline4', __name__)


def matchtype():
    url = 'https://static.api.nexon.co.kr/fifaonline4/latest/matchtype.json'
    res = requests.get(url)
    return res.json()


def get_users(nickname):
    url = '''https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname={}'''.format(nickname)
    headers = {
        'Authorization': APIKEY_FIFAONLINE4
    }
    res = requests.get(url, headers=headers)
    return res.json()


def user_matches(user_unique_id):
    url = '''https://api.nexon.co.kr/fifaonline4/v1.0/users/{}/matches?matchtype={}&offset=0&limit=100'''.format(user_unique_id, 40)
    headers = {
        'Authorization': APIKEY_FIFAONLINE4
    }
    res = requests.get(url, headers=headers)
    return res.json()


def match_detail(match_id):
    url = '''https://api.nexon.co.kr/fifaonline4/v1.0/matches/{}'''.format(match_id)
    headers = {
        'Authorization': APIKEY_FIFAONLINE4
    }
    res = requests.get(url, headers=headers)
    return res.json()


def get_user_nickname(users, user_ids, user_id):
    for i in range(0, len(user_ids)):
        if user_ids[i] == user_id:
            return users[i]
    return None


def get_match_raw_data(users, period_start, period_end):
    user_ids = []
    for i in users:
        user_ids.append(get_users(i)['accessId'])

    result = []
    for access_id in user_ids:
        for i in user_matches(access_id):
            match_info = match_detail(i)
            
            date = match_info['matchDate']
            if not period_start < date or not date < period_end:
                break

            match_end_type = match_info['matchInfo'][0]['matchDetail']['matchEndType']
            if match_end_type != 0:
                continue

            try:
                nick1 = get_user_nickname(users, user_ids, match_info['matchInfo'][0]['accessId'])
                nick1_score = match_info['matchInfo'][0]['shoot']['goalTotalDisplay']

                nick2 = get_user_nickname(users, user_ids, match_info['matchInfo'][1]['accessId'])
                nick2_Score = match_info['matchInfo'][1]['shoot']['goalTotalDisplay']
                
                if nick2 is None:
                    continue
                if nick1 is None:
                    continue
            except Exception as e:
                continue

            if [date, nick1, nick1_score, nick2, nick2_Score] in result:
                continue

            result.append([date, nick1, nick1_score, nick2, nick2_Score])

    result.sort(key=lambda x: x[0])
    result = sorted(result, reverse=True)

    return result


def get_match_data_user_table(users, match_raw_data):
    user_match_result = [[[] * 5 for i in users] for j in users]

    for i in match_raw_data:
        if not PERIOD_START < i[0] or not i[0] < PERIOD_END:
            continue

        for j in range(0, len(users)):
            for k in range(j, len(users)):
                if j == k:
                    continue

                if len(user_match_result[j][k]) >= MAX_GAME_PER_USER:
                    continue

                isHas = False
                for tmp in user_match_result[j][k]:
                    if i == tmp:
                        isHas = True
                        break
                if isHas:
                    continue

                if (i[1] == users[j] or i[3] == users[j]) and (i[1] == users[k] or i[3] == users[k]):
                    user_match_result[j][k].append(i)
                    user_match_result[k][j].append(i)
                    break

    return user_match_result


def get_wdl_match_table(users, user_match_result):
    result = [[[0, 0, 0, 0, 0] for i in users] for j in users]

    for row in range(0, len(user_match_result)):
        for column in range(0, len(user_match_result)):
            for i in range(0, len(user_match_result[row][column])):
                now_user = users[row]
                now_match = user_match_result[row][column][i]
                match_result = 'D'
                goals_for = 0
                goals_against = 0

                if now_match[1] == now_user:
                    goals_for += now_match[2]
                    goals_against += now_match[4]
                    if now_match[2] < now_match[4]:
                        match_result = 'L'
                    elif now_match[2] > now_match[4]:
                        match_result = 'W'
                elif now_match[3] == now_user:
                    goals_for += now_match[4]
                    goals_against += now_match[2]
                    if now_match[2] > now_match[4]:
                        match_result = 'L'
                    elif now_match[2] < now_match[4]:
                        match_result = 'W'
                else:
                    print('error')

                # print(now_user, match_result, now_match, row, column)
                if match_result == 'W':
                    result[row][column][0] += 1
                elif match_result == 'D':
                    result[row][column][1] += 1
                else:
                    result[row][column][2] += 1

                result[row][column][3] += goals_for
                result[row][column][4] += goals_against

    return result


def get_rank_table(users, wdl_match_table):
    temp_result = [[] for i in users]

    for row in range(0, len(wdl_match_table)):
        temp_result[row].append(users[row])
        w = d = l = gf = ga = gd = 0

        for column in range(0, len(wdl_match_table[row])):
            w  += wdl_match_table[row][column][0]
            d  += wdl_match_table[row][column][1]
            l  += wdl_match_table[row][column][2]
            gf += wdl_match_table[row][column][3]
            ga += wdl_match_table[row][column][4]
            gd += wdl_match_table[row][column][3] - wdl_match_table[row][column][4]
        
        temp_result[row].append(w + d + l)
        temp_result[row].append(w*3 + d*1)
        temp_result[row].append(w)
        temp_result[row].append(d)
        temp_result[row].append(l)
        temp_result[row].append(gf)
        temp_result[row].append(ga)
        temp_result[row].append(gd)
                
    temp_result.sort(key=lambda x: (x[2], x[8]))
    temp_result.reverse()

    result = []
    result.append(['순위', '팀', '경기수', '승점', '승', '무', '패', '득점', '실점', '득실차', '도움', '파울'])
    rank = 1
    for row in temp_result:
        result.append([rank, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], 0, 0])
        rank += 1

    return result


@api_v1_fifaonline4.route('/matchData', methods=['GET'])
def get_match_data():

    # user array
    users = ['jo바페', 'jo펩', 'jo태곤', '다시돌아왔도다', '이언러쉬이이이이', 'jo인성']

    # period
    MAX_GAME_PER_USER = 5
    period_start = '2020-09-01'
    period_end = '2020-12-31'

    dt = datetime.strptime(period_end, '%Y-%m-%d')
    period_end = str(dt + timedelta(days=1))

    match_raw_data = get_match_raw_data(users, period_start, period_end)

    return jsonify(data=match_raw_data, code=200, users=users), 200




# def print_arr_2X2(arr):
#     for i in arr:
#         for j in i:
#             print(j)
#         print('------------')
#     print('===========================')


# users = ['jo바페', 'jo펩', 'jo태곤', '다시돌아왔도다', '이언러쉬이이이이', 'jo인성']
# # users = ['jo바페', '특별함']

# match_raw_data = get_match_raw_data(users)
# for i in match_raw_data:
#     print(i)

# users_match_raw_table = get_match_data_user_table(users, match_raw_data)
# # print_arr_2X2(users_match_raw_table)

# wdl_match_table = get_wdl_match_table(users, users_match_raw_table)
# # print_arr_2X2(wdl_match_table)

# rank_table = get_rank_table(users, wdl_match_table)
# # print_arr_2X2(rank_table)

# print('\n\n산정기간 : ' + PERIOD_START + ' ~ ' + PERIOD_END_ORIGIN)
# print('기간 내 마지막 경기 시간 : ' + str(match_raw_data[0][0]) + '\n')
# for i in rank_table:
#     result = ''
#     for j in i:
#         result += str(j) + '\t'
#     print(result)

