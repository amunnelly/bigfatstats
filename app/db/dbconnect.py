# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 17:31:35 2020

@author: amunnelly

https://www.postgresqltutorial.com/postgresql-python/connect/
"""

import psycopg2 as psql
import json

class Postgres(object):
    
    def __init__(self, credentials):
        with open(credentials, "r") as f:
            cred = json.load(f)
            
        self.con = psql.connect(host=cred['Host'],
                                database=cred['Database'],
                                user=cred['User'],
                                password=cred['Password'])
        
        
    
    def run_query(self, query):
        self.cur = self.con.cursor()
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows
        

if __name__ == "__main__":
    query = """
    select a.team,
    count(distinct b.season) as PL,
    count(distinct c.season) as Cship
    from points a
    left join points b on a.team = b.team
    left join points c on a.team = c.team
    where b.competition = 'Premier League'
    and c.competition <> 'Premier League'
    group by a.team
    order by a.team;
    """
    x = Postgres("searcher.json")
    x.run_query(query)