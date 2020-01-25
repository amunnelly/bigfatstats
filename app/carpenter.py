import sys
import os
import csv
import datetime
import glob

db_path = os.path.join(sys.path[0], "app", "db")
c_path = os.path.join(sys.path[0], "app")
csv_path = os.path.join(sys.path[0], "app", "static", "js")
if db_path not in sys.path:
    sys.path.append(db_path)
if c_path not in sys.path:
    sys.path.append(c_path)
if csv_path not in sys.path:
    sys.path.append(csv_path)

import dbconnect

class Carpenter(object):

    def __init__(self):
        self.table = []
        self.db = dbconnect.Postgres("app/db/searcher.json")

    def make_soccer_table(self, item, competition):
        with open("app/queries/select_distinct.sql") as f:
            q = f.read()
        q = q.format(item, competition)
        # q = q.format("team", "Premier League' or 'Championship")

        rows = self.db.run_query(q)
        rows.sort()
        i = 0
        j = 0
        temp = []
        while i < len(rows):
            temp.append(rows[i][0])
            if j < 5:
                j += 1
            else:
                self.table.append(temp)
                temp = []
                j = 0
            i += 1

        return self.table

    def get_season(self, season, competition, csv=False):
        with open("app/queries/points_v_goal_difference.sql") as f:
            q = f.read()
        q = q.format(season, competition)
        # q = q.format("team", "Premier League' or 'Championship")

        rows = self.db.run_query(q)
        rows.sort(key=lambda x: x[1], reverse=True)
        if csv:
            self.create_csv(rows)
        else:
            return rows

    def create_csv(self, data, filename):

        with open(filename, 'w') as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(["team", "points", "gd", "goalsFor", "goalsAgainst"])
            for d in data:
                writer.writerow(d)

    def tidy_data_folder(self):
        csvs = glob.glob('./app/static/js/*.csv')
        for csv in csvs:
            os.remove(csv)


    def get_first_name(self, name):
        name = name.split(" ")
        return name[0]

    def log_comment(self, name, email, comment):
        stars = "*"*80
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        print(os.path.dirname(os.path.abspath(__file__)))
        with open("app/comments/comments.log", "a") as f:
            f.write(now+"\n")
            f.write(name+"\n")
            f.write(email+"\n")
            f.write(comment+"\n")
            f.write("\n"+stars+"\n")

