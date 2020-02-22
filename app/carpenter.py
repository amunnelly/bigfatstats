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

from app.db import dbconnect

class Carpenter(object):
    """
    A helper class for routes.py
    """

    def __init__(self):
        """
        Args:
            self.table (list): a holder for query results
            self.db (psycopg2.connection): a connection object for `psycopg2`
        """
        self.table = []
        self.db = dbconnect.Postgres()

    def make_soccer_table(self, item, competition):
        """
        Runs a query to find all the seasons or teams in the database for a
        particular competition. Returns a list of lists to make the on-page
        formatting easier.

        Args:
            item (str): either a team or a season 
            competition (str): the competition in question
        """
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
        """
        Queries the database to get the season details for a particular season
        and competition. Will write the data to .csv if required.

        Args:
            season (str): The season in question
            competition (str): The competition in question
            csv (bool): Download the data to .csv if required.
        """

        with open("app/queries/points_v_goal_difference.sql") as f:
            q = f.read()
        q = q.format(season, competition)
        # q = q.format("team", "Premier League' or 'Championship")

        rows = self.db.run_query(q)
        rows.sort(key=lambda x: x[1], reverse=True)
        if csv:
            self.create_csv(rows)
        
        return rows

    def create_csv(self, data, filename):
        """
        Writes a .csv to disk that will be used by a d3 graphing function

        Args:
            data (list): the data that is to be written to disk
            filename (str): the name of the csv file to be created.
        """

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
        """
        Helper function for the comment confirmation page
        """
        name = name.split(" ")
        return name[0]

    def log_comment(self, name, email, comment):
        """
        Writes user comments to disk.
        """
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

