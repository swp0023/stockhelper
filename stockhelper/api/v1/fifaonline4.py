import requests


APIKEY = '''eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiMTE3NDQzNjk5OCIsImF1dGhfaWQiOiIyIiwidG9rZW5fdHlwZSI6IkFjY2Vzc1Rva2VuIiwic2VydmljZV9pZCI6IjQzMDAxMTQ4MSIsIlgtQXBwLVJhdGUtTGltaXQiOiI1MDA6MTAiLCJuYmYiOjE2MDU0MjU2MjQsImV4cCI6MTYyMDk3NzYyNCwiaWF0IjoxNjA1NDI1NjI0fQ.T70wy14ebzWz-6q-XrHoSeu2HBcy-0TuJ20wm0qhnMA'''


def matchtype():
    url = 'https://static.api.nexon.co.kr/fifaonline4/latest/matchtype.json'
    res = requests.get(url)
    return res.json()


def get_users(nickname):
    url = '''https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname={}'''.format(nickname)
    headers = {
        'Authorization': APIKEY
    }
    res = requests.get(url, headers=headers)
    return res.json()


def user_matches(user_unique_id):
    url = '''https://api.nexon.co.kr/fifaonline4/v1.0/users/{}/matches?matchtype={}&offset=0&limit=100'''.format(user_unique_id, 40)
    headers = {
        'Authorization': APIKEY
    }
    res = requests.get(url, headers=headers)
    return res.json()


def match_detail(match_id):
    url = '''https://api.nexon.co.kr/fifaonline4/v1.0/matches/{}'''.format(match_id)
    headers = {
        'Authorization': APIKEY
    }
    res = requests.get(url, headers=headers)
    return res.json()


def get_user_nickname(users, user_ids, user_id):
    for i in range(0, len(user_ids)):
        if user_ids[i] == user_id:
            return users[i]
    return None


def get_match_raw_data(users):
    user_ids = []
    for i in users:
        user_ids.append(get_users(i)['accessId'])

    result = []
    for access_id in user_ids:
        for i in user_matches(access_id):
            match_info = match_detail(i)
            
            date = match_info['matchDate']
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

            result.append([date, nick1, nick1_score, nick2, nick2_Score])

    result.sort(key=lambda x: x[0])
    result = sorted(result, reverse=True)
    return result


def get_match_data_user_table(users, match_raw_data):
    user_match_result = [[[] * 5 for i in users] for j in users]

    for i in match_raw_data:
        for j in range(0, len(users)):
            for k in range(j, len(users)):
                if j == k:
                    continue

                if len(user_match_result[j][k]) > 4:
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
    result = [[[0, 0, 0] for i in users] for j in users]

    for row in range(0, len(user_match_result)):
        for column in range(0, len(user_match_result)):
            for i in range(0, len(user_match_result[row][column])):
                now_user = users[row]
                now_match = user_match_result[row][column][i]
                match_result = 'D'
                if now_match[1] == now_user:
                    if now_match[2] < now_match[4]:
                        match_result = 'L'
                    elif now_match[2] > now_match[4]:
                        match_result = 'W'
                elif now_match[3] == now_user:
                    if now_match[2] > now_match[4]:
                        match_result = 'L'
                    elif now_match[2] < now_match[4]:
                        match_result = 'W'
                else:
                    print('error')

                print(now_user, match_result, now_match, result[row][column][i][0], type(result[row][column][i][0]))

                if match_result == 'W':
                    result[row][column][i][0] = int(result[row][column][i][0]) + 1
                elif match_result == 'D':
                    result[row][column][i][1] = int(result[row][column][i][1]) + 1
                else:
                    result[row][column][i][2] = int(result[row][column][i][2]) + 1
    return result



# users = ['jo바페', 'jo펩', 'jo태곤', '다시돌아왔도다', '이언러쉬이이이이', 'jo인성']

# match_raw_data = get_match_raw_data(users)
# users_match_raw_table = get_match_data_user_table(users, match_raw_data)

# wdl_match_table = get_wdl_match_table(users, users_match_raw_table)

# for i in wdl_match_table:
#     for j in i:
#         print(j)
#     print('------------')
