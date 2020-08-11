import sys
from bs4 import BeautifulSoup
import requests
import re
import json
import copy
import pandas as pd
import numpy as np
from functions import quarterbyminute, calculatetime, samelineup, maketraditional, makeadvanced, makeopponent, makescoring
from Lineup import Lineup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
headers2 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
lineups = []
quarters = ['FirstQuarter', 'SecondQuarter', 'ThirdQuarter', 'ForthQuarter']
competition = ""
format = ""
paint_zone = ['A', 'B', 'C']
midrange_zone = ['D', 'E', 'F', 'G']

def main():
    if len(sys.argv) != 4:
        print("Wrong format")
        exit()
    season = sys.argv[2]
    if int(season)<2007:
        print("Lineup data started in 2007")
        exit()
    if (sys.argv[3] != "totals") and (sys.argv[3] != "mean"):
        print("Wrong format")
        exit()
    format = sys.argv[3]
    team = sys.argv[1]
    url = "https://www.euroleague.net/competition/teams/showteam?clubcode="+team+"&seasoncode=E"+str(season)+"#!games"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    title = soup.title.text.strip()
    if title == "404 Not Found":
        print("This team code is not correct")
        exit()
    euroleaguecontroller = soup.findAll("span", {"class": "ClubSubTitle"})
    el_texttocheck = "EuroLeague "+str(season)
    eu_texttocheck = "EuroCup "+str(season)
    if euroleaguecontroller[0].getText().startswith(el_texttocheck):
        competition = "E"
    else:
        url = "https://www.euroleague.net/competition/teams/showteam?clubcode="+team+"&seasoncode=U"+str(season)+"#!games"
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        euroleaguecontroller = soup.findAll("span", {"class": "ClubSubTitle"})
        if euroleaguecontroller[0].getText().startswith(eu_texttocheck):
            competition = "U"
        else:
            print("This team did not play European competition in this season")
            exit()
    print("Getting game list")
    versuscontainer = soup.findAll("td", {"class": "VersusContainer"})
    for value in versuscontainer:
        played = value.find_previous_sibling("td", {"class": "WinLoseContainer"})
        if played.text.strip() == "W" or played.text.strip() == "L":
            print("Analyzing "+value.text.strip())
            gameended = False
            at = value.find("span", {"class": "TeamPhaseGameVersusTypeContainer"})
            if at.text == "at":
                home = 0
                clase = "RoadClubStatsContainer"
            else:
                home = 1
                clase = "LocalClubStatsContainer"
            link = value.find("a")
            result = re.search('gamecode=(.*)&', link['href'])
            code = result.group(1)
            lineup_q = 1
            lineup_time = "10:00"
            url2 = "https://www.euroleague.net/main/results/showgame?gamecode="+code+"&seasoncode="+competition+season+"#!boxscore"
            req2 = requests.get(url2, headers)
            soup2 = BeautifulSoup(req2.content, 'html.parser')

            # Shots
            url_shots = "http://live.euroleague.net/api/Points?gamecode="+code+"&seasoncode="+competition+season
            result_shots = requests.get(url_shots, headers=headers)
            d_shots = json.loads(result_shots.content.decode())
            df_shots = pd.json_normalize(d_shots['Rows'])

            div = soup2.find("div", {"class": clase})
            starters = div.findAll("a", {"class": "PlayerStartFive"})
            current_lineup = Lineup([], [int(code)], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            for player in starters:
                current_lineup.players.append(player.text)
            current_lineup.players.sort()

            # PlayByPlay
            url3 = "https://live.euroleague.net/api/PlayByPlay?gamecode="+code+"&seasoncode="+competition+season
            result = requests.get(url3, headers=headers2)
            if result.content.decode() != '':
                d = json.loads(result.content.decode())
                for value in quarters:
                    df = pd.json_normalize(d[value])
                    df['CODETEAM'] = df['CODETEAM'].str.strip()
                    df['PLAYTYPE'] = df['PLAYTYPE'].str.strip()
                    for index, row in df.iterrows():
                        if ((row['CODETEAM'] == str(team)) and (row['PLAYTYPE'] == "IN" or row['PLAYTYPE'] == "OUT")) or (row['PLAYTYPE'] == "EG" and not(gameended)):
                            if len(lineups) == 0:
                                if row['PLAYTYPE'] == "EG":
                                    gameended = True
                                    time = "00:00"
                                    laurden = 40
                                else:
                                    time = row['MARKERTIME']
                                    laurden = row['MINUTE']

                                minutes = calculatetime(lineup_q, lineup_time, laurden, time)
                                current_lineup.minutes = minutes
                                record_man = copy.deepcopy(current_lineup)
                                lineups.append(record_man)
                                lineup_q = laurden
                                lineup_time = row['MARKERTIME']

                            else:
                                indize = 0
                                aurkitua = False
                                current_players = list(current_lineup.players)

                                while indize < len(lineups) and not(aurkitua):
                                    list_players = list(lineups[indize].players)
                                    list_players.sort()

                                    if samelineup(list_players, current_players):

                                        if int(code) not in lineups[indize].games :
                                            lineups[indize].games.append(int(code))

                                        if row['PLAYTYPE'] == "EG":
                                            gameended = True
                                            time = "00:00"
                                            laurden = 40
                                        else:
                                            time = row['MARKERTIME']
                                            laurden = row['MINUTE']
                                        minutes = calculatetime(lineup_q, lineup_time, laurden, time)
                                        lineups[indize].minutes = lineups[indize].minutes+minutes

                                        lineups[indize].t3_int = lineups[indize].t3_int+current_lineup.t3_int
                                        lineups[indize].opp_t3_int = lineups[indize].opp_t3_int+current_lineup.opp_t3_int
                                        lineups[indize].t3_con = lineups[indize].t3_con+current_lineup.t3_con
                                        lineups[indize].opp_t3_con = lineups[indize].opp_t3_con+current_lineup.opp_t3_con

                                        lineups[indize].t2_int = lineups[indize].t2_int+current_lineup.t2_int
                                        lineups[indize].opp_t2_int = lineups[indize].opp_t2_int+current_lineup.opp_t2_int
                                        lineups[indize].t2_con = lineups[indize].t2_con+current_lineup.t2_con
                                        lineups[indize].opp_t2_con = lineups[indize].opp_t2_con+current_lineup.opp_t2_con

                                        lineups[indize].t1_int = lineups[indize].t1_int+current_lineup.t1_int
                                        lineups[indize].opp_t1_int = lineups[indize].opp_t1_int+current_lineup.opp_t1_int
                                        lineups[indize].t1_con = lineups[indize].t1_con+current_lineup.t1_con
                                        lineups[indize].opp_t1_con = lineups[indize].opp_t1_con+current_lineup.opp_t1_con

                                        lineups[indize].d_reb = lineups[indize].d_reb+current_lineup.d_reb
                                        lineups[indize].opp_d_reb = lineups[indize].opp_d_reb+current_lineup.opp_d_reb

                                        lineups[indize].ast = lineups[indize].ast+current_lineup.ast
                                        lineups[indize].opp_ast = lineups[indize].opp_ast+current_lineup.opp_ast

                                        lineups[indize].per = lineups[indize].per+current_lineup.per
                                        lineups[indize].opp_per = lineups[indize].opp_per+current_lineup.opp_per

                                        lineups[indize].rob = lineups[indize].rob+current_lineup.rob
                                        lineups[indize].opp_rob = lineups[indize].opp_rob+current_lineup.opp_rob

                                        lineups[indize].foul = lineups[indize].foul+current_lineup.foul
                                        lineups[indize].opp_foul = lineups[indize].opp_foul+current_lineup.opp_foul

                                        lineups[indize].foul_f = lineups[indize].foul_f+current_lineup.foul_f
                                        lineups[indize].opp_foul_r = lineups[indize].opp_foul_r+current_lineup.opp_foul_r

                                        lineups[indize].blk = lineups[indize].blk+current_lineup.blk
                                        lineups[indize].opp_blk = lineups[indize].opp_blk+current_lineup.opp_blk

                                        lineups[indize].blk_a = lineups[indize].blk_a+current_lineup.blk_a
                                        lineups[indize].opp_blk_a = lineups[indize].opp_blk_a+current_lineup.opp_blk_a

                                        lineups[indize].o_reb = lineups[indize].o_reb+current_lineup.o_reb
                                        lineups[indize].opp_o_reb = lineups[indize].opp_o_reb+current_lineup.opp_o_reb


                                        lineups[indize].mr_points = lineups[indize].mr_points+current_lineup.mr_points
                                        lineups[indize].pitp = lineups[indize].pitp+current_lineup.pitp
                                        lineups[indize].p_off_tov = lineups[indize].p_off_tov+current_lineup.p_off_tov
                                        lineups[indize].p_fastbreak = lineups[indize].p_fastbreak+current_lineup.p_fastbreak

                                        lineup_q = laurden
                                        lineup_time = row['MARKERTIME']

                                        aurkitua = True
                                    indize += 1
                                if not(aurkitua):

                                    if row['PLAYTYPE'] == "EG":
                                        gameended = True
                                        time = "00:00"
                                        laurden = 40
                                    else:
                                        time = row['MARKERTIME']
                                        laurden = row['MINUTE']

                                    minutes = calculatetime(lineup_q, lineup_time, laurden, time)
                                    current_lineup.minutes = minutes
                                    record_man = copy.deepcopy(current_lineup)
                                    lineups.append(record_man)

                                    lineup_q = laurden
                                    lineup_time = row['MARKERTIME']

                            if row['PLAYTYPE'] == "IN":
                                current_lineup.players.append(row['PLAYER'])
                            elif row['PLAYTYPE'] == "OUT":
                                for ind2, j2 in enumerate(current_lineup.players):
                                    if j2.startswith(row['PLAYER']) or row['PLAYER'].startswith(j2) or row['PLAYER'] == j2:
                                        del current_lineup.players[ind2]

                            players_copy = list(current_lineup.players)
                            current_lineup = Lineup(players_copy, [int(code)], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                            current_lineup.players.sort()

                        else:

                            if row['PLAYTYPE'] == "3FGA":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.t3_int += 1
                                else:
                                    current_lineup.opp_t3_int += 1
                            elif row['PLAYTYPE'] == "3FGM":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.t3_int += 1
                                    current_lineup.t3_con += 1
                                    fb = df_shots['FASTBREAK'][df_shots['NUM_ANOT'] == int(row['NUMBEROFPLAY'])].values[0]
                                    off_tov = df_shots['POINTS_OFF_TURNOVER'][df_shots['NUM_ANOT'] == int(row['NUMBEROFPLAY'])].values[0]
                                    if str(fb) == "None":
                                        fb = "0"
                                    if str(off_tov) == "None":
                                        off_tov = "0"
                                    if int(fb):
                                        current_lineup.p_fastbreak += 3
                                    if int(off_tov):
                                        current_lineup.p_off_tov += 3
                                else:
                                    current_lineup.opp_t3_int += 1
                                    current_lineup.opp_t3_con += 1
                            elif row['PLAYTYPE'] == "2FGA" or row['PLAYTYPE'] == "LAYUPATT":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.t2_int += 1
                                else:
                                    current_lineup.opp_t2_int += 1
                            elif row['PLAYTYPE'] == "2FGM" or row['PLAYTYPE'] == "DUNK" or row['PLAYTYPE'] == "LAYUPMD":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.t2_int += 1
                                    current_lineup.t2_con += 1
                                    fb = df_shots['FASTBREAK'][df_shots['NUM_ANOT'] == int(row['NUMBEROFPLAY'])].values[0]
                                    off_tov = df_shots['POINTS_OFF_TURNOVER'][df_shots['NUM_ANOT'] == int(row['NUMBEROFPLAY'])].values[0]
                                    pitp = df_shots['ZONE'][df_shots['NUM_ANOT'] == int(row['NUMBEROFPLAY'])].values[0]
                                    if str(fb) == "None":
                                        fb = "0"
                                    if str(off_tov) == "None":
                                        off_tov = "0"
                                    if int(fb):
                                        current_lineup.p_fastbreak += 2
                                    if int(off_tov):
                                        current_lineup.p_off_tov += 2
                                    if pitp in paint_zone:
                                        current_lineup.pitp += 2
                                    if pitp in midrange_zone:
                                        current_lineup.mr_points += 2

                                else:
                                    current_lineup.opp_t2_int += 1
                                    current_lineup.opp_t2_con += 1
                            elif row['PLAYTYPE'] == "FTA":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.t1_int += 1
                                else:
                                    current_lineup.opp_t1_int += 1
                            elif row['PLAYTYPE'] == "FTM":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.t1_int += 1
                                    current_lineup.t1_con += 1
                                else:
                                    current_lineup.opp_t1_int += 1
                                    current_lineup.opp_t1_con += 1
                            elif row['PLAYTYPE'] == "D":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.d_reb += 1
                                else:
                                    current_lineup.opp_d_reb += 1
                            elif row['PLAYTYPE'] == "AS":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.ast += 1
                                else:
                                    current_lineup.opp_ast += 1
                            elif row['PLAYTYPE'] == "TO":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.per += 1
                                else:
                                    current_lineup.opp_per += 1
                            elif row['PLAYTYPE'] == "ST":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.rob += 1
                                else:
                                    current_lineup.opp_rob += 1
                            elif row['PLAYTYPE'] == "CM" or row['PLAYTYPE'] == "OF" or row['PLAYTYPE'] == "CMT" or row['PLAYTYPE'] == "CMU":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.foul += 1
                                else:
                                    current_lineup.opp_foul += 1
                            elif row['PLAYTYPE'] == "RV":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.foul_f += 1
                                else:
                                    current_lineup.opp_foul_r += 1
                            elif row['PLAYTYPE'] == "FV":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.blk += 1
                                else:
                                    current_lineup.opp_blk += 1
                            elif row['PLAYTYPE'] == "AG":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.blk_a += 1
                                else:
                                    current_lineup.opp_blk_a += 1
                            elif row['PLAYTYPE'] == "O":
                                if row['CODETEAM'] == str(team):
                                    current_lineup.o_reb += 1
                                else:
                                    current_lineup.opp_o_reb += 1

    name_traditional = team+"_"+season+"_traditional.csv"
    name_advanced = team+"_"+season+"_advanced.csv"
    name_scoring = team+"_"+season+"_scoring.csv"
    name_opponent = team+"_"+season+"_opponent.csv"

    df = pd.DataFrame([t.__dict__ for t in lineups ])

    #Lineups with dif 5 players delete
    df.drop(df[df['players'].str.len() != 5].index, inplace=True)

    #Lineups with 0 seconds delete
    df.drop(df[df['minutes'] == 0].index, inplace=True)

    #Players array --> String

    #Games array --> Int
    df['games'] = df['games'].str.len()

    # print(df.dtypes)
    df.players = df.players.astype(str)

    # Sort by players
    df.sort_values('players', inplace=True, ascending=True)

    # Make 4 files
    df_traditional = maketraditional(df.copy(), format)
    df_advanced = makeadvanced(df.copy(), format)
    df_scoring = makescoring(df.copy(), format)
    df_opponent = makeopponent(df.copy(), format)

    # Export 4 files
    df_traditional.to_csv(name_traditional, index=False, decimal=',')
    df_advanced.to_csv(name_advanced, index=False, decimal=',')
    df_scoring.to_csv(name_scoring, index=False, decimal=',')
    df_opponent.to_csv(name_opponent, index=False, decimal=',')
    print("Done")

if __name__ == "__main__":
    main()
