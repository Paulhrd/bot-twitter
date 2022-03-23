"""HUARD PAUL
Link of the original twitter account: https://twitter.com/Topdelamusic
Bot twitter who tweet the most popular music of the week (french)"""

#You need to enter youtube and twitter api key in the text document called "password.txt"
#api keys available here: https://developer.twitter.com/en and https://developers.google.com/youtube/v3/getting-started

#To full automize the script do a FTP on a VPS and make a cron job that run every week the script
#Documentation tweepy: https://docs.tweepy.org/en/stable/index.html

#for every import: download libs by following the link bellow and remplace "opencv" by the name of the lib
import tweepy   # intaller pycharm: https://www.youtube.com/watch?v=WQeoO7MI0Bs&t=442s
from googleapiclient.discovery import build     #INSTALLER GOOGLE API CLIENT LIBRARY :https://www.youtube.com/c/Coreyms/videos
import requests
import emoji

passwords_folder = open("passwords.txt", "r")
passwords = passwords_folder.readlines()
print(passwords[1])


youtube_api_key = passwords[1]
youtube = build('youtube', 'v3', developerKey=youtube_api_key)


request = youtube.playlistItems().list(
    part='snippet',
    playlistId='PLsa-dEwv56FaoevRy1iSkp2YWt9udgkdJ',
    maxResults=1
)

response = request.execute()
print("this is a response:", response)
items = response.get("items")
print("This is the items: ", items)
snippet = items[0].get("snippet")
print("This is a snippet: ", snippet)
resourceId = snippet.get("resourceId")
print("This is resourceId : ", resourceId)
videoId = resourceId.get("videoId")
print("This is a videoId : ", videoId)
urlvideopart1 = "https://www.youtube.com/watch?v="
urlvideo = urlvideopart1 + videoId
print(urlvideo)

#import pytube
#test for tweet a clip of the music but the format still too big
"""dlink = pytube.YouTube(urlvideo)
streams = dlink.streams.filter(progressive=True).order_by('resolution').desc()
print("telechargement...")
streams[0].download(filename='sample_video.mp4')
print("telechargement complet!")
clip = VideoFileClip("sample_video.mp4").subclip(0,40)
clip.write_videofile("clip_video.mp4")"""


title = snippet.get("title")
print("This is a title : ", title)

fichier = open("data.txt", "r")
if fichier.read() == title:
    fichier.close()
    print("la nouvelle musique est la meme que celle d'avant")
else:
    fichier.close()
    fichier = open("data.txt", "w")
    fichier.write(title)
    fichier.close()

    thumbnails = snippet.get("thumbnails")
    print("this is a thumbnails", thumbnails)
    maxres = thumbnails.get("maxres")
    if maxres is None:
        maxres = thumbnails.get("high")

    print("This is maxres : ", maxres)
    urlimage = maxres.get("url")
    print("This is an urlimage", urlimage)

    responseimage = requests.get(urlimage)
    file = open("sample_image.png", "wb")
    file.write(responseimage.content)
    file.close()
    sampleimage = "sample_image.png"


    API_KEY = passwords[3]
    API_SECRET = passwords[5]
    ACCESS_TOKEN = passwords[7]
    ACCESS_TOKEN_SECRET = passwords[9]

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    Contentemoji = emoji.emojize(":chart_increasing: :fire: :chart_increasing: \n"
                                 "\n")
    ContentInTweet = emoji.emojize(" devient la musique la plus tendance sur Youtube France! :France: \n" 
                                   "\n" 
                                   "Voici le lien youtube de la video: \n"
                                   " :backhand_index_pointing_right: ")
    Tweet = Contentemoji + title + ContentInTweet + urlvideo
    api.update_status_with_media(Tweet, 'sample_image.png')
