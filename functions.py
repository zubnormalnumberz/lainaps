import datetime
import pandas as pd

def quarterbyminute(minute):
    if minute<=10:
        return 1
    if minute<=20:
        return 2
    if minute<=30:
        return 3
    if minute<=40:
        return 4
    return 5

def calculatetime(lineup_min, lineup_time, min, time):
    if quarterbyminute(lineup_min) == quarterbyminute(min):
        t1 = lineup_time.split(":")
        t2 = time.split(":")
        a1 = datetime.timedelta(minutes = int(t1[0]), seconds = int(t1[1]))
        a2 = datetime.timedelta(minutes = int(t2[0]), seconds = int(t2[1]))
        dif = a1-a2
        return dif.seconds
    else:
        q_dif = quarterbyminute(min)-quarterbyminute(lineup_min)-1
        t1 = lineup_time.split(":")
        t2 = time.split(":")
        a1 = datetime.timedelta(minutes = int(t1[0]), seconds = int(t1[1]))
        a2 = datetime.timedelta(minutes = int(t2[0]), seconds = int(t2[1]))
        a3 = datetime.timedelta(minutes = 10, seconds = 0)
        dif = a3-a2
        return (q_dif*60)+(a1.seconds)+(dif.seconds)

def samelineup(l1, l2):
    if len(l1) != len(l2):
        return False
    else:
        for i in range(len(l1)):
            berdina = l1[i].startswith(l2[i]) or l2[i].startswith(l1[i]) or l2[i] == l1[i]
            if not(berdina):
                return False
        return True

def calculatepoints(row):
    return row.t1_con + (2*row.t2_con) + (3*row.t3_con)

def calculatepoints_a(row):
    return row.opp_t1_con + (2*row.opp_t2_con) + (3*row.opp_t3_con)

def calculateplusminus(row, fav):
    if fav:
        return calculatepoints(row)-calculatepoints_a(row)
    else:
        return calculatepoints_a(row)-calculatepoints(row)

def calculatepercentage(con, int):
    if con == 0:
        return 0.0
    else:
        return round(con/int*100, 2)

def asttoratio(row):
    if row.per == 0:
        return 0.0
    else:
        return round(row.ast/row.per, 2)

def calculatetovpercentage(row):
    if row.t2_int + row.t3_int + row.t1_int + row.per == 0:
        return 0.0
    else:
        return round(row.per*100/((row.t2_int + row.t3_int)+(0.44*row.t1_int)+row.per), 2)

def calculatets(row):
    if row.t1_int + row.t2_int + row.t3_int == 0:
        return 0.0
    else:
        points = calculatepoints(row)
        return round(points*100/(2 * ((row.t2_int + row.t3_int) + 0.44 * row.t1_int)), 2)

def calculateefg(row):
    if row.t2_int + row.t3_int == 0:
        return 0.0
    else:
        return round(((row.t2_con+row.t3_con) + 0.5 * row.t3_con)*100 / (row.t2_int+row.t3_int), 2)

def calculateastratio(row):
    if row.t2_int + row.t3_int + row.t1_int + row.ast + row.per == 0:
        return 0.0
    else:
        return round(row.ast*100/((row.t2_int + row.t3_int)+(0.44*row.t1_int)+row.ast+row.per), 2)

def calculateorebpercentage(row):
    if row.o_reb + row.opp_d_reb == 0:
        return 0.0
    else:
        return round(100 * row.o_reb / (row.o_reb + row.opp_d_reb), 2)

def calculatedrebpercentage(row):
    if row.d_reb + row.opp_o_reb == 0:
        return 0.0
    else:
        return round(100 * row.d_reb / (row.d_reb + row.opp_o_reb), 2)

def calculaterebpercentage(row):
    if row.d_reb + row.o_reb + row.opp_o_reb + row.opp_d_reb == 0:
        return 0.0
    else:
        return round(100 * (row.d_reb + row.o_reb) / (row.d_reb + row.o_reb + row.opp_o_reb + row.opp_d_reb), 2)

def calculateftr(row):
    if row.t2_int + row.t3_int == 0:
        return 0.0
    else:
        return round(row.t1_int*100/(row.t2_int + row.t3_int), 2)

def calculatepir(row):
    return calculatepoints(row)-(row.t1_int-row.t1_con)-(row.t2_int-row.t2_con)-(row.t3_int-row.t3_con)+row.o_reb+row.d_reb+row.ast+row.rob-row.per+row.blk-row.blk_a-row.foul+row.foul_f

def calculatepossessions(row):
    if row.o_reb + row.opp_d_reb == 0:
        reb_p1 = 0
    else:
        reb_p1 = row.o_reb / (row.o_reb + row.opp_d_reb)

    if row.opp_o_reb + row.d_reb == 0:
        reb_p2 = 0
    else:
        reb_p2 = row.opp_o_reb / (row.opp_o_reb + row.d_reb)

    team_fga = row.t2_int + row.t3_int
    team_fgm = row.t2_con + row.t3_con
    opp_fga = row.opp_t2_int + row.opp_t3_int
    opp_fgm = row.opp_t2_con + row.opp_t3_con

    return round(0.5 * ((team_fga + 0.4 * row.t1_int - 1.07 * (reb_p1) * (team_fga - team_fgm) + row.per) + (opp_fga + 0.4 * row.opp_t1_int - 1.07 * (reb_p2) * (opp_fga - opp_fgm) + row.opp_per)), 2)

def calculateoer(row):
    possessions = calculatepossessions(row)
    if possessions == 0:
        return 0.0
    else:
        points = calculatepoints(row)
        return round(100*(points / possessions), 2)

def calculateder(row):
    possessions = calculatepossessions(row)
    if possessions == 0:
        return 0.0
    else:
        points = calculatepoints_a(row)
        return round(100*(points / possessions), 2)

def calculatepace(row):
    possessions = calculatepossessions(row)
    return round((40 * 60 * possessions) / row.minutes, 2)

def calculatepts_2pt(row):
    points = calculatepoints(row)
    if points == 0:
        return 0.0
    else:
        two_p = 2*row.t2_con
        return round(100*two_p/points, 2)

def calculatepts_3pt(row):
    points = calculatepoints(row)
    if points == 0:
        return 0.0
    else:
        three_p = 3*row.t3_con
        return round(100*three_p/points, 2)

def calculatepts_1pt(row):
    points = calculatepoints(row)
    if points == 0:
        return 0.0
    else:
        one_p = row.t1_con
        return round(100*one_p/points, 2)

def calculatefga_2pt(row):
    if row.t2_int + row.t3_int == 0:
        return 0.0
    else:
        return round(row.t2_int*100/(row.t2_int + row.t3_int), 2)

def calculatefga_3pt(row):
    if row.t2_int + row.t3_int == 0:
        return 0.0
    else:
        return round(row.t3_int*100/(row.t2_int + row.t3_int), 2)

def calculateMRpts(row):
    points = calculatepoints(row)
    if points == 0:
        return 0.0
    else:
        return round(row.mr_points*100/points, 2)

def calculatePITP(row):
    points = calculatepoints(row)
    if points == 0:
        return 0.0
    else:
        return round(row.pitp*100/points, 2)

def calculatepts_fb(row):
    points = calculatepoints(row)
    if points == 0:
        return 0.0
    else:
        return round(row.p_fastbreak*100/points, 2)

def calculatepts_offtov(row):
    points = calculatepoints(row)
    if points == 0:
        return 0.0
    else:
        return round(row.p_off_tov*100/points, 2)

def maketraditional(df, format):

    # Points, total rebounds and plusminus
    df['points'] = df.apply(calculatepoints, axis=1)
    df['reb'] = df.apply(lambda row: row.o_reb + row.d_reb, axis=1)
    df['+/-'] = df.apply(lambda x: calculateplusminus(x,1), axis=1)

    # Percentages
    df['T1%'] = df.apply(lambda x: calculatepercentage(x['t1_con'],x['t1_int']), axis=1)
    df['T2%'] = df.apply(lambda x: calculatepercentage(x['t2_con'],x['t2_int']), axis=1)
    df['T3%'] = df.apply(lambda x: calculatepercentage(x['t3_con'],x['t3_int']), axis=1)

    if format == "mean":
        df['points'] = df.apply(lambda row: round(row.points/row.games, 2), axis=1)
        df['minutes'] = df.apply(lambda row: round(row.minutes/row.games, 2), axis=1)
        df['t1_int'] = df.apply(lambda row: round(row.t1_int/row.games, 2), axis=1)
        df['t1_con'] = df.apply(lambda row: round(row.t1_con/row.games, 2), axis=1)
        df['t2_int'] = df.apply(lambda row: round(row.t2_int/row.games, 2), axis=1)
        df['t2_con'] = df.apply(lambda row: round(row.t2_con/row.games, 2), axis=1)
        df['t3_int'] = df.apply(lambda row: round(row.t3_int/row.games, 2), axis=1)
        df['t3_con'] = df.apply(lambda row: round(row.t3_con/row.games, 2), axis=1)
        df['o_reb'] = df.apply(lambda row: round(row.o_reb/row.games, 2), axis=1)
        df['d_reb'] = df.apply(lambda row: round(row.d_reb/row.games, 2), axis=1)
        df['reb'] = df.apply(lambda row: round(row.reb/row.games, 2), axis=1)
        df['ast'] = df.apply(lambda row: round(row.ast/row.games, 2), axis=1)
        df['rob'] = df.apply(lambda row: round(row.rob/row.games, 2), axis=1)
        df['per'] = df.apply(lambda row: round(row.per/row.games, 2), axis=1)
        df['blk'] = df.apply(lambda row: round(row.blk/row.games, 2), axis=1)
        df['blk_a'] = df.apply(lambda row: round(row.blk_a/row.games, 2), axis=1)
        df['foul'] = df.apply(lambda row: round(row.foul/row.games, 2), axis=1)
        df['foul_f'] = df.apply(lambda row: round(row.foul_f/row.games, 2), axis=1)
        df['+/-'] = df.apply(lambda row: round(row['+/-']/row.games, 2), axis=1)

    df['minutes'] = df.apply(lambda row: round(row.minutes/60, 1), axis=1)
    # df['minutes'] = pd.to_datetime(df["minutes"], unit='s').dt.strftime("%H:%M:%S")

    # Delete columns
    df.drop(['opp_t1_int', 'opp_t1_con', 'opp_t2_int', 'opp_t2_con', 'opp_t3_int', 'opp_t3_con', 'opp_o_reb', 'opp_d_reb', 'opp_ast', 'opp_per', 'opp_rob', 'opp_blk', 'opp_blk_a', 'opp_foul', 'opp_foul_r', 'mr_points', 'pitp', 'p_off_tov', 'p_fastbreak'], axis=1)

    # Order
    df = df[['players', 'games', 'minutes', 'points', 't1_int', 't1_con', 'T1%', 't2_int', 't2_con', 'T2%', 't3_int', 't3_con', 'T3%', 'o_reb', 'd_reb', 'reb', 'ast', 'rob', 'per', 'blk', 'blk_a', 'foul', 'foul_f', '+/-']]

    return df

def makeadvanced(df, format):

    # Advanced stats
    df['efg%'] = df.apply(calculateefg, axis=1)
    df['ts%'] = df.apply(calculatets, axis=1)
    df['FTRatio'] = df.apply(calculateftr, axis=1)
    df['AST/TO'] = df.apply(asttoratio, axis=1)
    df['AST Ratio'] = df.apply(calculateastratio, axis=1)
    df['TOV%'] = df.apply(calculatetovpercentage, axis = 1)
    df['oreb%'] = df.apply(calculateorebpercentage, axis = 1)
    df['dreb%'] = df.apply(calculatedrebpercentage, axis = 1)
    df['pir'] = df.apply(calculatepir, axis = 1)
    df['reb%'] = df.apply(calculaterebpercentage, axis = 1)
    df['pace'] = df.apply(calculatepace, axis=1)
    df['offrat'] = df.apply(calculateoer, axis=1)
    df['defrat'] = df.apply(calculateder, axis=1)
    df['netrat'] = df.apply(lambda row: round(row.offrat - row.defrat, 2), axis=1)

    if format == "mean":
        df['pir'] = df.apply(lambda row: round(row.pir/row.games, 2), axis=1)
        df['minutes'] = df.apply(lambda row: round(row.minutes/row.games, 2), axis=1)

    df['minutes'] = df.apply(lambda row: round(row.minutes/60, 1), axis=1)
    # df['minutes'] = pd.to_datetime(df["minutes"], unit='s').dt.strftime("%H:%M:%S")

    # Delete columns
    df.drop(['t1_int', 't1_con', 't2_int', 't2_con', 't3_int', 't3_con', 'o_reb', 'd_reb', 'ast', 'rob', 'per', 'blk', 'blk_a', 'foul', 'foul_f' ,'opp_t1_int', 'opp_t1_con', 'opp_t2_int', 'opp_t2_con', 'opp_t3_int', 'opp_t3_con', 'opp_o_reb', 'opp_d_reb', 'opp_ast', 'opp_per', 'opp_rob', 'opp_blk', 'opp_blk_a', 'opp_foul', 'opp_foul_r', 'mr_points', 'pitp', 'p_off_tov', 'p_fastbreak'], axis=1)

    # Order
    df = df[['players', 'games', 'minutes', 'offrat', 'defrat', 'netrat', 'AST/TO', 'AST Ratio', 'oreb%', 'dreb%', 'reb%', 'TOV%', 'efg%', 'ts%', 'FTRatio', 'pace', 'pir']]

    return df

def makescoring(df, format):

    # Scoring stats
    df['%PTS 2PT'] = df.apply(calculatepts_2pt, axis=1)
    df['%PTS 3PT'] = df.apply(calculatepts_3pt, axis=1)
    df['%PTS FT'] = df.apply(calculatepts_1pt, axis=1)
    df['%FGA 2p'] = df.apply(calculatefga_2pt, axis=1)
    df['%FGA 3p'] = df.apply(calculatefga_3pt, axis=1)
    df['%PTS2PT MR'] = df.apply(calculateMRpts, axis=1)
    df['%PTS PITP'] = df.apply(calculatePITP, axis=1)
    df['%PTS FBPS'] = df.apply(calculatepts_fb, axis=1)
    df['%PTS OFFTO'] = df.apply(calculatepts_offtov, axis=1)

    if format == "mean":
        df['minutes'] = df.apply(lambda row: round(row.minutes/row.games, 2), axis=1)

    df['minutes'] = df.apply(lambda row: round(row.minutes/60, 1), axis=1)
    # df['minutes'] = pd.to_datetime(df["minutes"], unit='s').dt.strftime("%H:%M:%S")

    # Delete columns
    df.drop(['t1_int', 't1_con', 't2_int', 't2_con', 't3_int', 't3_con', 'o_reb', 'd_reb', 'ast', 'rob', 'per', 'blk', 'blk_a', 'foul', 'foul_f' ,'opp_t1_int', 'opp_t1_con', 'opp_t2_int', 'opp_t2_con', 'opp_t3_int', 'opp_t3_con', 'opp_o_reb', 'opp_d_reb', 'opp_ast', 'opp_per', 'opp_rob', 'opp_blk', 'opp_blk_a', 'opp_foul', 'opp_foul_r'], axis=1)

    # Order
    df = df[['players', 'games', 'minutes', '%FGA 2p', '%FGA 3p', '%PTS 2PT', '%PTS2PT MR', '%PTS 3PT', '%PTS FBPS', '%PTS FT', '%PTS OFFTO', '%PTS PITP']]

    return df

def makeopponent(df, format):

    # Points, total rebounds and plusminus
    df['opp_points'] = df.apply(calculatepoints_a, axis=1)
    df['opp_reb'] = df.apply(lambda row: row.opp_o_reb + row.opp_d_reb, axis=1)
    df['+/-'] = df.apply(lambda x: calculateplusminus(x,0), axis=1)

    # Percentages
    df['opp_T1%'] = df.apply(lambda x: calculatepercentage(x['opp_t1_con'],x['opp_t1_int']), axis=1)
    df['opp_T2%'] = df.apply(lambda x: calculatepercentage(x['opp_t2_con'],x['opp_t2_int']), axis=1)
    df['opp_T3%'] = df.apply(lambda x: calculatepercentage(x['opp_t3_con'],x['opp_t3_int']), axis=1)

    if format == "mean":
        df['opp_points'] = df.apply(lambda row: round(row.opp_points/row.games, 2), axis=1)
        df['minutes'] = df.apply(lambda row: round(row.minutes/row.games, 2), axis=1)
        df['opp_t1_int'] = df.apply(lambda row: round(row.opp_t1_int/row.games, 2), axis=1)
        df['opp_t1_con'] = df.apply(lambda row: round(row.opp_t1_con/row.games, 2), axis=1)
        df['opp_t2_int'] = df.apply(lambda row: round(row.opp_t2_int/row.games, 2), axis=1)
        df['opp_t2_con'] = df.apply(lambda row: round(row.opp_t2_con/row.games, 2), axis=1)
        df['opp_t3_int'] = df.apply(lambda row: round(row.opp_t3_int/row.games, 2), axis=1)
        df['opp_t3_con'] = df.apply(lambda row: round(row.opp_t3_con/row.games, 2), axis=1)
        df['opp_o_reb'] = df.apply(lambda row: round(row.opp_o_reb/row.games, 2), axis=1)
        df['opp_d_reb'] = df.apply(lambda row: round(row.opp_d_reb/row.games, 2), axis=1)
        df['opp_reb'] = df.apply(lambda row: round(row.opp_reb/row.games, 2), axis=1)
        df['opp_ast'] = df.apply(lambda row: round(row.opp_ast/row.games, 2), axis=1)
        df['opp_rob'] = df.apply(lambda row: round(row.opp_rob/row.games, 2), axis=1)
        df['opp_per'] = df.apply(lambda row: round(row.opp_per/row.games, 2), axis=1)
        df['opp_blk'] = df.apply(lambda row: round(row.opp_blk/row.games, 2), axis=1)
        df['opp_blk_a'] = df.apply(lambda row: round(row.opp_blk_a/row.games, 2), axis=1)
        df['opp_foul'] = df.apply(lambda row: round(row.opp_foul/row.games, 2), axis=1)
        df['opp_foul_r'] = df.apply(lambda row: round(row.opp_foul_r/row.games, 2), axis=1)
        df['+/-'] = df.apply(lambda row: round(row['+/-']/row.games, 2), axis=1)

    df['minutes'] = df.apply(lambda row: round(row.minutes/60, 1), axis=1)
    # df['minutes'] = pd.to_datetime(df["minutes"], unit='s').dt.strftime("%H:%M:%S")

    # Delete columns
    df.drop(['t1_int', 't1_con', 't2_int', 't2_con', 't3_int', 't3_con', 'o_reb', 'd_reb', 'ast', 'rob', 'per', 'blk', 'blk_a', 'foul', 'foul_f', 'mr_points', 'pitp', 'p_off_tov', 'p_fastbreak'], axis=1)

    # Order
    df = df[['players', 'games', 'minutes', 'opp_points', 'opp_t1_int', 'opp_t1_con', 'opp_T1%', 'opp_t2_int', 'opp_t2_con', 'opp_T1%', 'opp_t3_int', 'opp_t3_con', 'opp_T1%', 'opp_o_reb', 'opp_d_reb', 'opp_reb', 'opp_ast', 'opp_per', 'opp_rob', 'opp_blk', 'opp_blk_a', 'opp_foul', 'opp_foul_r', '+/-']]

    return df
