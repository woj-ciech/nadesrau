from nudity import Nudity
from urllib.request import urlopen
from InstagramAPI import InstagramAPI
import json
from urllib.request import  urlretrieve
import os
from datetime import datetime
from colorama import Fore
import sys
import utilsy

utilssy = utilsy.Utilsy()

class Instagram:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.nudity = Nudity()

        self.instagram_api = InstagramAPI(username, password)
        self.instagram_api.login()
        if self.instagram_api.LastJson['status'] == "fail":
            print(Fore.RED + self.instagram_api.LastJson['message'] + Fore.RED)
            sys.exit()

    def check_location(self, lat, lng, nudes=False,firearm=False):
        self.instagram_api.geosearchLocations(lat, lng)
        print("Looking for photos nearby " + Fore.GREEN + str(lat) + ", " + str(lng) + Fore.RESET)
        last1 = self.instagram_api.LastJson

        if not os.path.exists('location/'):
            os.mkdir('location/')

        print("Places: ")
        for place in last1['venues']:
            if place['address']:
                print(Fore.LIGHTBLUE_EX + place['address'] + Fore.RESET)

        for place in last1['venues']:
            c = 0
            print("Checking " + Fore.LIGHTBLUE_EX + place['address'] + Fore.RESET)
            self.instagram_api.getLocationFeed(place['external_id'])
            last2 = self.instagram_api.LastJson
            # try:
            #     print("Found " + Fore.CYAN + str(len(last2['items'])) + Fore.RESET+ " results")
            # except Exception as e:
            #     break

            if not os.path.exists('location' + "/" + place['address']):
                os.mkdir('location' + "/" + place['address'])

            if not os.path.exists('location' + "/" + place['address'] + "/artifacts"):
                os.mkdir('location/'  + place['address'] + "/artifacts")

            for photo in last2['items']:
                if 'carousel_media' in photo: # only carousel media?
                    try:
                        print("[i] Downloading " + photo['carousel_media'][0]['image_versions2']['candidates'][0][
                            'url'] + " to " + 'location/' + Fore.YELLOW + place['address'] + "/" + photo['user']['username'] + ".jpg" + Fore.RESET)
                        urlretrieve(photo['carousel_media'][0]['image_versions2']['candidates'][0][
                            'url'],'location' + "/" + place['address'] + "/" +photo['user']['username']+ ".jpg")
                        if nudes:
                            score = self.nudity.score('location' + "/" + place['address'] + "/" +photo['user']['username']+ ".jpg")
                            print("Detected score: " + Fore.CYAN + str(round(score, 4)) + Fore.RESET)

                            if score > 0.5:
                                print(Fore.RED + "    Found nude")
                                print(
                                    "    Timestamp: " + Fore.RED + str(
                                        datetime.utcfromtimestamp(photo['taken_at']).strftime('%Y-%m-%d %H:%M:%S')) + Fore.RED)
                                print(Fore.LIGHTCYAN_EX + "    " + photo['user']['username'] + Fore.RESET)

                                if photo['caption'] is not None:
                                    print("    Text:" + photo['caption']['text'])

                                # print("    Text:" + photo['caption']['text'])
                                print("    Moving to /artifacts")
                                try:
                                    os.rename('location' + "/" + place['address'] + "/" + photo['user']['username'] + ".jpg",
                                            'location' + "/" + place['address'] + "/artifacts/" + "" + photo['user']['username'] + ".jpg")
                                except Exception as e:
                                    print (e.args)
                            else:
                                print(Fore.GREEN + "    No nude" + Fore.RESET)
                        elif firearm:
                            detection = utilssy.detect_firearm(
                                image_path="location" + "/" + place['address'] + "/" + photo['user']['username'] + ".jpg",
                                output_path="location" + "/" + place['address'] + "/" + photo['user']['username'] + "_box.jpg")

                            c = c + 1
                    except Exception as e:
                        print(e.with_traceback())

    def check_hashtag(self,hashtag, nudes=False,firearm=False):
        req = urlopen("https://www.instagram.com/explore/tags/" + hashtag + "/?__a=1")
        json_req = json.loads(req.read())
        c = 0

        if not os.path.exists('hashtags'):
            os.mkdir('hashtags')

        if not os.path.exists("hashtags/"+hashtag):
            os.mkdir("hashtags/"+hashtag)

        if not os.path.exists("hashtags/"+hashtag + "/artifacts"):
            os.mkdir("hashtags/"+hashtag + "/artifacts")

        for i in json_req['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']:
            try:
                    print(
                        "[i] Downloading " + i['node']['display_url'] + Fore.YELLOW +" to hashtags/" + hashtag + "/" + i['node']['owner']['id'] + ".jpg" + Fore.RESET)
                    urlretrieve(i['node']['display_url'], "hashtags/"+hashtag + "/"+i['node']['owner']['id'] + ".jpg")
                    if nudes:
                        score = self.nudity.score("hashtags/"+ hashtag + "/" +i['node']['owner']['id'] + ".jpg")
                        print("Detected score: " + Fore.CYAN + str(round(score, 4)) + Fore.RESET)
                        if score > 0.5:
                            print(Fore.RED + "    Found nude" + Fore.RESET)
                            print("    Timestamp: " + Fore.RED + str(
                                datetime.utcfromtimestamp(i['node']['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S')) + Fore.RESET)
                            # print("    Access:" + i['node']['accessibility_caption'])
                            print("    Owner: " + Fore.LIGHTMAGENTA_EX + i['node']['owner']['id'] + Fore.RESET)
                            self.instagram_api.getUsernameInfo(i['node']['owner']['id'])
                            print("         Username: " + Fore.RED + self.instagram_api.LastJson['user']['username'] + Fore.RESET)
                            print("         Full name: " + Fore.LIGHTRED_EX + self.instagram_api.LastJson['user']['full_name'] + Fore.RESET)
                            print("         Bio: " + self.instagram_api.LastJson['user']['biography'])
                            print("         Url: " + self.instagram_api.LastJson['user']['external_url'])
                            print("    Moving to /artifacts")
                            os.rename("hashtags/"+hashtag + "/" +i['node']['owner']['id'] + ".jpg", "hashtags/"+hashtag + "/artifacts/" +self.instagram_api.LastJson['user']['username']+ ".jpg")

                    elif firearm:
                        self.instagram_api.getUsernameInfo(i['node']['owner']['id'])
                        detection = utilssy.detect_firearm(image_path="hashtags/" + hashtag + "/"+i['node']['owner']['id'] + ".jpg",
                                               output_path="hashtags/" + hashtag + "/artifacts/"+ self.instagram_api.LastJson['user']['username'] + "_box.jpg")
                        if detection:
                            print("    Timestamp: " + Fore.RED + str(
                                datetime.utcfromtimestamp(i['node']['taken_at_timestamp']).strftime(
                                    '%Y-%m-%d %H:%M:%S')) + Fore.RESET)
                            # print("    Access:" + i['node']['accessibility_caption'])
                            print("    Owner: " + Fore.LIGHTMAGENTA_EX + i['node']['owner']['id'] + Fore.RESET)
                            self.instagram_api.getUsernameInfo(i['node']['owner']['id'])
                            print("         Username: " + Fore.RED + self.instagram_api.LastJson['user'][
                                'username'] + Fore.RESET)
                            print("         Full name: " + Fore.LIGHTRED_EX + self.instagram_api.LastJson['user'][
                                'full_name'] + Fore.RESET)
                            print("         Bio: " + self.instagram_api.LastJson['user']['biography'])
                            print("         Url: " + self.instagram_api.LastJson['user']['external_url'])
                            print("    Moving to /artifacts")
            except Exception as e:
               print(e.with_traceback())


            c = c + 1

    def check_user(self, username, stop, nudes=False,firearm=False):
        url = "https://www.instagram.com/web/search/topsearch/?context=blended&query=" + username + "&rank_token=0.3953592318270893&count=1"
        response = urlopen(url)
        respJSON = json.loads(response.read())
        try:
            user_id = str(respJSON['users'][0].get("user").get("pk"))
        except Exception as e:
            print(e.args)
            sys.exit()

        if not os.path.exists('users'):
            os.mkdir('users')

        if not os.path.exists("users/" + username):
            os.mkdir("users/" + username)

        if not os.path.exists("users/" + username+"/artifacts"):
            os.mkdir("users/" + username+"/artifacts")

        self.instagram_api.getUsernameInfo(user_id)
        ########PRINT INFO#############
        print(self.instagram_api.LastJson['user']['username'])
        print(self.instagram_api.LastJson['user']['full_name'])
        print(self.instagram_api.LastJson['user']['biography'])
        print(self.instagram_api.LastJson['user']['external_url'])

        nextmaxid = ""
        rating = []
        c = 0

        while c < stop:
            self.instagram_api.getUserFeed(user_id, nextmaxid)

            for i in self.instagram_api.LastJson['items']:
                try:
                    print("[i] Downloading " + i['image_versions2']['candidates'][0][
                        'url'] + Fore.YELLOW +  " to " +"users/"+ username + "/image"+str(c) + ".jpg" + Fore.RESET)
                    urlretrieve(i['image_versions2']['candidates'][0]['url'],"users/" + username + "/" + "/image"+str(c) + ".jpg")

                    if nudes:
                        score = self.nudity.score("users/" +username + "/"  + "/image"+str(c) + ".jpg")
                        rating.append(score)
                        print("Detected score: " + Fore.CYAN + str(round(score, 4)) + Fore.RESET)
                        if score > 0.5:
                            print(Fore.RED + "    Found nude" + Fore.RESET)
                            print("    Timestamp: " + Fore.RED + str(
                                datetime.utcfromtimestamp(i['taken_at']).strftime(
                                    '%Y-%m-%d %H:%M:%S')) + Fore.RESET)
                            print("    Text: " + i['caption']['text'])
                            print("    Moving to /artifacts")
                            os.rename("users/" +username + "/image" + str(c) + ".jpg",
                                      "users/" + username + "/artifacts/image" + str(c) + ".jpg")


                        else:
                            c = c + 1

                    elif firearm:
                        detection = utilssy.detect_firearm(
                            image_path="users/" + username + "/" +  "/image"+str(c)  + ".jpg",
                            output_path="users/" + username + "/artifacts/" + "/image"+str(c) + "_box.jpg")
                        if detection:
                            print("    Timestamp: " + Fore.RED + str(
                                datetime.utcfromtimestamp(i['taken_at']).strftime(
                                    '%Y-%m-%d %H:%M:%S')) + Fore.RESET)
                            print("    Text: " + i['caption']['text'])
                            print("    Moving to /artifacts")
                            c = c + 1
                        else:
                            c = c + 1

                except Exception as e:
                    print(e.args)


            nextmaxid = self.instagram_api.LastJson['next_max_id']
                ######CAROUSEL media
                # if help == 0:
                #     try:
                #         print("[i] Downloading " + i['image_versions2']['candidates'][0][
                #             'url'] + " into +" + ig_username + "/image" + str(c) + ".jpg")
                #         urlretrieve(i['carousel_media'][0]['image_versions2']['candidates'][0]['url'], "image" + str(c) + ".jpg")
                #         score = nudity.score(ig_username + "/image" + str(c) + ".jpg")
                #         print("Detected score: " + str(round(score, 4)))
                #         # print(nudity.has(ig_username + "/image" + str(c) + ".jpg"))
                #         if nudity.has(ig_username+"image" + str(c) + ".jpg"):
                #             print ("Found photo with " + str(round(score, 4)) + ". Moving to /artifacts")
                #             os.rename(ig_username + "/image" + str(c) + ".jpg", ig_username + "/artifacts/image" + str(c) + ".jpg")
                #         # print(round(score, 4))
                #         rating.append(score)
                #     # print(nudity.has("image" + str(c) + ".jpg"))
                #     except Exception as e:
                #         print(e.args)

                # print (c)

        if nudes:
            avg = sum(rating) / len(rating)
            # avg = np.mean(rating)
            print("Whoregrade: " + str(avg))