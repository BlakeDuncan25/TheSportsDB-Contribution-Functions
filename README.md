# Examples:

Import Packages
```
import TheSportsDBFunctions as spdb
import pandas as pd
```

Set path for downloads along with login information.
```
path = "/Users/blakeduncan/Downloads"
username = "username"
password = "password"
```

Login
```
spdb.thesportsdb_login(username, password)
```

Add Future Fixtures
```
event_csv = pd.read_csv("/Users/blakeduncan/Downloads/events.csv")

league = event_csv.league.tolist()
date = event_csv.date.tolist()
starttime = event_csv.starttime.tolist()
season = event_csv.season.tolist()
hometeam = event_csv.hometeam.tolist()
awayteam = event_csv.awayteam.tolist()
week = event_csv.week.tolist()

spdb.add_event(league, date, starttime, season, hometeam, awayteam, week)
```

Add Past Events with Scores
```
score_csv = pd.read_csv("/Users/blakeduncan/Downloads/scores.csv")

league = score_csv.league.tolist()
date = score_csv.date.tolist()
starttime = score_csv.starttime.tolist()
season = score_csv.season.tolist()
hometeam = score_csv.hometeam.tolist()
awayteam = score_csv.awayteam.tolist()
homescore = score_csv.homescore.tolist()
awayscore = score_csv.awayscore.tolist()
week = score_csv.week.tolist()

spdb.add_score(league, date, starttime, season, hometeam, awayteam, homescore, awayscore, week)
```

Add Players
```
player_csv = pd.read_csv("/Users/blakeduncan/Downloads/players.csv")

team = player_csv.team.tolist()
player = player_csv.player.tolist()
dob = player_csv.dob.tolist()
position = player_csv.position.tolist()
nationality = player_csv.nationality.tolist()
height = player_csv.height.tolist()
weight = player_csv.weight.tolist()
team_name = player_csv.team_name.tolist()
image_url = player_csv.image_url.tolist()

spdb.add_player(path, team, player, dob, position, nationality, height, weight, team_name, image_url)
```

Add Teams
```
team_csv = pd.read_csv("/Users/blakeduncan/Downloads/teams.csv")

league = team_csv.league.tolist()
full_team_name = team_csv.full_team_name.tolist()
country = team_csv.country.tolist()
api_id = team_csv.api_id.tolist()
year_established = team_csv.year_established.tolist()
stadium = team_csv.stadium.tolist()
stadium_location = team_csv.stadium_location.tolist()
stadium_capacity = team_csv.stadium_capacity.tolist()
wiki_team = team_csv.wiki_team.tolist()
wiki_stadium = team_csv.wiki_stadium.tolist()
badge_url = team_csv.badge_url.tolist()

spdb.create_team(
    path,
    username,
    password,
    league,
    full_team_name,
    country,
    api_id,
    year_established,
    stadium,
    stadium_location,
    stadium_capacity,
    wiki_team,
    wiki_stadium,
    badge_url,
)
```

Format Image to Badge Dimensions
```
team = "Team Name"
image_url = "https://www.google.com/your_image.png"

spdb.save_badge_png(path, team, image_url)
```

Upload Team Fan Art
```
fan_art_csv = pd.read_csv("/Users/blakeduncan/Downloads/fan_art.csv")

team = fan_art_csv.team.tolist()
fanart1 = fan_art_csv.fanart1.tolist()
fanart2 = fan_art_csv.fanart2.tolist()
fanart3 = fan_art_csv.fanart3.tolist()
fanart4 = fan_art_csv.fanart4.tolist()

spdb.upload_team_fan_art(path, team, fanart1, fanart2, fanart3, fanart4)
```
