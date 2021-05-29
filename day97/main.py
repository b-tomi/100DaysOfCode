# Podcast Downloader/Uploader

from pathlib import Path
from urllib.request import urlretrieve

import feedparser
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import config

# podcast homepages
# not needed anymore, getting links from the rss feeds instead, but keeping for reference
# URL_BEGINNERS = "http://nihongoconteppei.com"
# URL_INTERMED = "http://teppeisensei.com"
# URL_TEPPNORI = "http://teppeinorikojapanese.com"
# URL_NORIKO = "https://www.japanesewithnoriko.com"

# RSS feeds
RSS_BEGINNERS = "https://nihongoconteppei.com/feed/podcast/"
RSS_INTERMED = "http://teppeisensei.com/index20.rdf"
RSS_TEPPNORI = "https://teppeinorikojapanese.com/feed/podcast/"
RSS_NORIKO = "https://anchor.fm/s/1380f800/podcast/rss"


def find_last_ep(folder):
    """Takes folder as STR and returns the episode number of the most recent file as INT."""
    # TODO: Needs updating once episode number reaches 1000+
    path = Path(folder)
    # convert the generator object in to a list of .mp3 files
    file_list = [p for p in path.glob("*.mp3")]
    last_file = str(file_list[len(file_list) - 1])
    # return just the last three characters before ".mp3"
    return int(last_file[-7:-4])


def get_episodes_list(rss_url, last_ep, is_intermed=False):
    """Takes RSS URL and the number of the last episode and returns a LIST of all more recent ones."""
    list_out = []
    feed = feedparser.parse(rss_url)
    # gets the number of entries
    newest_link = feed.entries[0].enclosures[0].get("href")

    if is_intermed:
        # deal with the occasional case of extra characters at the end of intermed files
        # i.e. Nihongo20con20Teppei23526-8cceb.mp3
        newest_ep = int(newest_link[63:66])
    else:
        # just get the episode number from the file name e.g. "...284.mp3"
        # fix for "Teppeinoriko152-1.mp3", just in case it happens again, also fix in the file names below
        newest_link = newest_link.replace("-1.mp3", ".mp3")
        newest_ep = int(newest_link[-7:-4])

    # add all newer eps into a list
    # deal with the case there are no newer eps
    if newest_ep > last_ep:
        for i in range(0, newest_ep - last_ep):
            list_out.append(feed.entries[i].enclosures[0].get("href"))

    # sort the list (older to newer), doesn't matter if empty
    list_out.sort()
    # then return list of new eps, or just an empty list if there are none
    return list_out


def download_episodes(ep_list, is_intermed=False, is_teppnori=False):
    """Takes a LIST of episodes, downloads and uploads them."""
    # check if the upload directories exist, and create them
    for file in ep_list:
        # intermed/teppnori files have a different file name format, deal with the possible extra characters
        if is_intermed:
            filename = f"{str(file)[41:66]}.mp3"
            target = config.FOLDER_INTERMED + filename
        elif is_teppnori:
            # the fix for "Teppeinoriko152-1.mp3"
            file = file.replace("-1.mp3", ".mp3")
            filename = f"{str(file)[-19:-4]}.mp3"
            target = config.FOLDER_TEPPNORI + filename
        else:
            filename = f"{str(file)[-27:-4]}.mp3"
            target = config.FOLDER_BEGINNERS + filename

        urlretrieve(file, target)
        print(f"Downloaded {filename}")
        # copy the file to the upload folder too
        upload_episode(filename, is_intermed, is_teppnori)
        print(f"Uploaded {filename}")


def upload_episode(file_name, is_intermed, is_teppnori):
    """Takes a file name as STR and uploads in to the appropriate Google Drive folder."""
    if is_intermed:
        source_file = config.FOLDER_INTERMED + file_name
        folder_id = config.UPLOAD_INTERMED
    elif is_teppnori:
        source_file = config.FOLDER_TEPPNORI + file_name
        folder_id = config.UPLOAD_TEPPNORI
    else:
        source_file = config.FOLDER_BEGINNERS + file_name
        folder_id = config.UPLOAD_BEGINNERS

    # upload the file using PyDrive
    file = drive.CreateFile({"title": file_name, "mimeType": "audio/mpeg", "parents": [{"id": folder_id}]})
    file.SetContentFile(source_file)
    file.Upload()


def main():
    # arguments: rss url and the number of the last downloaded episode
    beginners_list = get_episodes_list(RSS_BEGINNERS, find_last_ep(config.FOLDER_BEGINNERS))
    if len(beginners_list) > 0:
        download_episodes(beginners_list)
    else:
        print("No new beginners episodes found.")

    intermed_list = get_episodes_list(RSS_INTERMED, find_last_ep(config.FOLDER_INTERMED), is_intermed=True)
    if len(intermed_list) > 0:
        download_episodes(intermed_list, is_intermed=True)
    else:
        print("No new intermed episodes found.")

    teppnori_list = get_episodes_list(RSS_TEPPNORI, find_last_ep(config.FOLDER_TEPPNORI))
    if len(teppnori_list) > 0:
        download_episodes(teppnori_list, is_teppnori=True)
    else:
        print("No new Teppei & Noriko episodes found.")


# Google Auth and Drive stuff, opens a link in the web browser for authentication
# requires client_secrets.json (downloaded from the Google API Console) in the same folder
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

if __name__ == "__main__":
    main()
