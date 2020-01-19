select team as team,
sum(Points) as points,
sum(GoalDifference) as gd,
sum(GoalsFor) as goalsFor,
sum(GoalsAgainst) as goalsAgainst
from points
where season = '{:}'
and Competition = '{:}'
and Country = 'England'
group by team
order by points desc;
