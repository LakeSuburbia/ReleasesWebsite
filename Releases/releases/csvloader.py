import requests
import pandas as pd
import pathlib

# initialise dataframe with csv
path = pathlib.Path("C://Users/matt/PycharmProjects/ReleasesWebsite/Releases/releases/ReleasesApp/resources/legacy_releases.csv")
releases = pd.read_csv(path)

# set column names to first row
releases.rename(columns=releases.iloc[0])

# lower case column names
releases.columns = releases.columns.str.lower()

# remove scores
releases = releases[["date", "title", "artist"]]

# remove rows without data in vital columns
releases = releases[releases["date"].notna()]
releases = releases[releases["title"].notna()]
releases = releases[releases["artist"].notna()]

# reformat date
releases["date"] = releases["date"].str.replace(r"^([\d]{1,2})-([\d)]{1,2})-(\d\d\d\d)$", "\\3-\\2-\\1", regex=True)

for release in releases.itertuples():
    # format the JSON data
    releaseJSON = {
        "release_date": release.date,
        "artist": release.artist,
        "title": release.title
    }
    print(releaseJSON)

    # send the data out!
    req = requests.post('http://127.0.0.1:8000/restapi/releases/', releaseJSON, auth=('ADMIN', 'ADMIN'))
    print(req)
