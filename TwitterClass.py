import tweepy
from tweepy import OAuthHandler
import os
from nudity import Nudity
from colorama import Fore
from urllib.request import urlopen
from urllib.request import  urlretrieve
from datetime import datetime
import utilsy

nudity = Nudity()
utilssy = utilsy.Utilsy()

#hashtag = ""

class Twitter:
    def __init__(self,consumer_key,consumer_secret,access_token,access_secret):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)
        hashtag = ""
        self.hashtag = hashtag

    def check_user(self, username, stop, nude=False,firearm=False):


            tweets = self.api.user_timeline(screen_name=username,
                                   count=200, include_rts=False,
                                   exclude_replies=True,
                                            include_entities=True)

            if not os.path.exists("users"):
                os.mkdir("users")


            if not os.path.exists("users/"+username):
                os.mkdir("users/"+username)

            if not os.path.exists("users/"+username+"/artifacts"):
                os.mkdir("users/"+username+"/artifacts")

            c = 0
            if nude:
                for tweet in tweets:
                    try:

                        print(
                            "[i] Downloading " + tweet.entities['media'][0]['media_url_https'] + Fore.YELLOW +" to " + "users "+username + "/image" + str(
                                c) + ".jpg" + Fore.RESET)

                        urlretrieve( tweet.entities['media'][0]['media_url_https'], "users/"+username + "/image" + str(c) + ".jpg")
                        score = nudity.score("users/"+username + "/image" + str(c) + ".jpg")
                        print("Detected score: " + Fore.CYAN + str(round(score, 4)) + Fore.RESET)
                        if score > 0.5:
                            print(Fore.RED + "    Found nude" + Fore.RESET)
                            print("    Timestamp: " + Fore.RED + str(tweet.created_at) + Fore.RESET)
                            print("         Text: " + Fore.RED + tweet.text + Fore.RESET)
                            print("    Moving to /artifacts")
                            os.rename("users/"+username + "/image" + str(c) + ".jpg", "users/"+username + "/artifacts/image" + str(c) + ".jpg")
                        c = c + 1
                    except Exception as e:
                        pass

                    if c == stop:
                        break
            if firearm:
                for tweet in tweets:
                    try:
                        if 'media' in tweet.entities:
                            if 'media_url_https' in tweet.entities['media'][0]:
                                print(
                                    "[i] Downloading " + tweet.entities['media'][0][
                                        'media_url_https'] + Fore.YELLOW + " to " + "users/"+username + "/image" + str(
                                        c) + ".jpg" + Fore.RESET)

                                urlretrieve(tweet.entities['media'][0]['media_url_https'], "users/"+username + "/image" + str(c) + ".jpg")
                                print("[i] Processing image...")
                                utilssy.detect_firearm("users/"+username + "/image" + str(c) + ".jpg", "users/"+username + "/artifacts/image" + str(c) + "_box.jpg")
                                c = c + 1

                                if c == stop:
                                    break
                        else:
                            pass

                    except Exception as e:
                        print(e.args)




    def stream_hashtags(self, hashtag,nudes=False,firearm=False):
        if not os.path.exists("hashtags/"):
            os.mkdir("hashtags/")

        if not os.path.exists("hashtags/" + hashtag):
            os.mkdir("hashtags/" + hashtag)

        if not os.path.exists("hashtags/" + hashtag + "/" + "artifacts"):
            os.mkdir("hashtags/" + hashtag + "/" + "artifacts")

        if firearm:
            myStreamListener = MyStreamListener(hashtag=hashtag, firearm=True)
            myStream = tweepy.Stream(auth=self.api.auth, listener=myStreamListener)
            myStream.filter(track=[hashtag])
        elif nudes:
            myStreamListener = MyStreamListener(hashtag=hashtag, nude=True)
            myStream = tweepy.Stream(auth=self.api.auth, listener=myStreamListener)
            myStream.filter(track=[hashtag])

    def stream_location(self, location, firearm=False,nudes=False):
        if not os.path.exists("location/"):
            os.mkdir("location/")

        if not os.path.exists("location/" + str(location[0])+","+str(location[1])):
            os.mkdir("location/"+ str(location[0])+","+str(location[1]))

        if not os.path.exists("location/" + str(location[0])+","+str(location[1]) + "/artifacts"):
            os.mkdir("location/"+ str(location[0])+","+str(location[1]) + "/artifacts")

        try:
            if nudes:

                myStreamListener = MyStreamListener(location=str(location[0])+","+str(location[1]), nude=nudes)
                myStream = tweepy.Stream(auth=self.api.auth, listener=myStreamListener)

                myStream.filter(locations=location)
            elif firearm:
                myStreamListener = MyStreamListener(location=str(location[0]) + "," + str(location[1]), firearm=True)
                myStream = tweepy.Stream(auth=self.api.auth, listener=myStreamListener)

                myStream.filter(locations=location)
        except Exception as e:
            print("Unknown error, try again")
            print(e.args)

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, hashtag=None,location=None,nude=False,firearm=False):
        super().__init__()
        self.counter = 0
        self.hashtag = hashtag
        self.location = location
        self.nude = nude
        self.firearm = firearm

    def on_error(self, status_code):
        print(status_code)

    def on_status(self, status):
        self.counter = self.counter + 1

        if self.hashtag:
            if 'media' in status.entities:
                if 'media_url_https' in status.entities['media'][0]:
                    print("[i] Downloading " + status.entities['media'][0][
                        'media_url_https'] + " into " "hashtags/" + self.hashtag + "/" + status.user.screen_name + ".jpg")
                    urlretrieve(status.entities['media'][0]['media_url_https'],"hashtags/" + self.hashtag + "/" + status.user.screen_name + ".jpg")
                    if self.firearm:
                        path = "hashtags/" + self.hashtag + "/" + status.user.screen_name + ".jpg"
                        detection = utilssy.detect_firearm(image_path=path, output_path="hashtags/" + self.hashtag + "/artifacts/" + status.user.screen_name + "_box.jpg")
                        if detection:
                            print("    Username: " + Fore.LIGHTRED_EX + status.user.name + Fore.RESET)
                            print("    Screen name: " + Fore.LIGHTCYAN_EX + status.user.screen_name + Fore.RESET)

                            print("    Text: " + Fore.LIGHTYELLOW_EX + status.text + Fore.RESET)

                            print("    Moving to /artifacts")
                    elif self.nude:
                        try:
                            score = nudity.score("hashtags/"  + self.hashtag +"/"+ status.user.screen_name + ".jpg")
                            print("Detected score: " + Fore.CYAN + str(round(score, 4)) + Fore.RESET)

                            if score > 0.5:
                                print(Fore.RED + "    Found nude" + Fore.RESET)
                                print("    Username: " + Fore.LIGHTRED_EX + status.user.name + Fore.RESET)
                                print("    Screen name: " + Fore.LIGHTCYAN_EX + status.user.screen_name + Fore.RESET)

                                print("    Text: " + Fore.LIGHTYELLOW_EX + status.text + Fore.RESET)

                                print("    Moving to /artifacts")
                                try:
                                    os.rename("hashtags/"  + self.hashtag +"/"+ status.user.screen_name + ".jpg",
                                              "hashtags/" + self.hashtag + "/artifacts/" + status.user.screen_name + ".jpg")
                                except Exception as e:
                                    print(e.args)
                            else:
                                print(Fore.GREEN + "    No nude" + Fore.RESET)

                        except Exception as e:
                            print(e.args)
            else:
                pass
        elif self.location:
            if 'media' in status.entities:
                if 'media_url_https' in status.entities['media'][0]:

                    print("[i] Downloading " + status.entities['media'][0][
                        'media_url_https'] + " into " "location/" + self.location + "/" + status.user.screen_name + ".jpg")
                    urlretrieve(status.entities['media'][0]['media_url_https'],
                                "location/" + self.location + "/" + status.user.screen_name + ".jpg")
                    if self.firearm:
                        path = "location/" + self.location + "/" + status.user.screen_name + ".jpg"
                        utilssy.detect_firearm(image_path=path, output_path="location/" + self.location + "/artifacts/" + status.user.screen_name + "_box.jpg")
                        print("Waiting for tweets")
                    elif self.nude:
                        try:
                            score = nudity.score("location/" +self.location+"/"+ status.user.screen_name + ".jpg")
                            print("Detected score: " + Fore.CYAN + str(round(score, 4)) + Fore.RESET)

                            if score > 0.5:
                                print(Fore.RED + "    Found nude")
                                print(Fore.LIGHTCYAN_EX + "    " + status.place.full_name + Fore.RESET)
                                print(Fore.LIGHTCYAN_EX + "    " + status.user.screen_name + Fore.RESET)

                                print("    Text:" + status.text)

                                print("    Moving to /artifacts")
                                try:
                                    os.rename("location/" +self.location+"/"+ status.user.screen_name + ".jpg",
                                              "location/" +self.location+ "/artifacts/" + status.user.screen_name + ".jpg")
                                except Exception as e:
                                    print(e.args)
                            else:
                                print(Fore.GREEN + "    No nude" + Fore.RESET)

                        except Exception as e:
                            print(e.args)
            else:
                pass
