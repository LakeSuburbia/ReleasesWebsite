import requests
import pandas as pd
import sys, os

# initialise dataframe with csv
csv = pd.read_csv(os.path.realpath("releasesplatform/resources/legacy_releases.csv"))

# csv cleanup
csv.rename(columns=csv.iloc[0])
csv.columns = csv.columns.str.lower()

# releases

#releases cleanup
releases = csv[["date", "title", "artist"]]
releases = releases[releases["date"].notna()]
releases = releases[releases["title"].notna()]
releases = releases[releases["artist"].notna()]
releases["date"] = releases["date"].str.replace(r"^([\d]{1,2})-([\d)]{1,2})-(\d\d\d\d)$", "\\3-\\2-\\1", regex=True)

for index, release in enumerate(releases.itertuples()):
    # format the JSON data
    releaseJSON = {
        "release_date": release.date,
        "artist": release.artist,
        "title": release.title
    }

    # send the data out!
    req = requests.post('http://127.0.0.1:8000/restapi/releases/', releaseJSON, auth=('ADMIN', 'ADMIN'))
    print("release", index, "result:", req)

#scores

# scores cleanup
scores = csv.drop(csv.columns[[0, 1, 3, 4]], axis=1)
scores.dropna(axis=0, how='all', inplace=True)

for release in scores.head(1).itertuples(index=False):
    print(release)
    release = release._asdict()
    title = release.pop('title')
    for index, user in enumerate(release):
        if release[user] != "nan":
            scoreJSON = {
                "user": user,
                "release": title,
                "score": release[user]
            }
            req = requests.post('http://127.0.0.1:8000/restapi/scores/', scoreJSON, auth=('ADMIN', 'ADMIN'))
            print("release", index, "result:", req)
