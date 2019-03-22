import Instagram
import TwitterClass
import argparse
from argparse import RawTextHelpFormatter
from colorama import Fore

desc1 = ''' +-'~`---------------------------------/\--                      
 ||"""""""""""""""""""""""""""""""" \\\\\\  \/~)
 || asciiart.eu                      \\\\\\  \/_
  |~~~~~~~~-________________-_________________\ ~--_
  !---------|_________       ------~~~~~(--   )--~~
    Gun & nudity       \ /~~~~\~~\   )--- \_ /(
      detection        ||     |  | \   ()   \\
   Twitter & Instagram \\____/_ / ()\        \\
      |||||             `~~~~~~~~~-. \        \\
     ||. .||                        \ \  <($)> \\
    |||\=/|||                        \ \        \\
    |.-- --.|                         \ \        \\
    /(.) (.)\                          \ \        \\
    \ ) . ( /   medium.com/@woj_ciech   \ \  ()    \|
    '(  v  )`   github.com/woj-ciech    _\_\__====~~~
    \\
'''
desc2 = '''Example:\\python3 nadesrau.py --twitter --stream_hashtag #booty --nudity\\
       python3 nadesrau.py --instagram --check_user_instagram kimkardashian --firearm\\
       python3 nadesrau.py --twitter --stream_location -169.6 -71.3 177.4 77.4 --firearm\\
       python3 nadesrau.py --instagram --check_hashtag kids --nudity'''

desc = desc1+desc2

#coord = [-169.6,-71.3,177.4,77.4] # https://boundingbox.klokantech.com

INSTAGRAM_USER = ""
INSTAGRAM_PASSWORD = ""

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

parser = argparse.ArgumentParser(
    description=desc, formatter_class=RawTextHelpFormatter)

group = parser.add_argument_group("Required arguments")

group.add_argument("--twitter", help="Twitter",  action='store_true')
group.add_argument("--instagram", help="Instagram", action='store_true')

parser.add_argument('--stream_location',nargs='+', type=float, help="Twitter location streaming")# https://boundingbox.klokantech.com/
parser.add_argument("--stream_hashtag", help="Twitter hashtag streaming", default="")
parser.add_argument("--check_user_twitter", help="Check Twitter user", default="")

parser.add_argument("--check_hashtag", help="Check Instagram hastahg",default="")
parser.add_argument("--check_location", help="Check Instagram location", default="")#["50.0754926","14.4288119"]
parser.add_argument("--check_user_instagram", help="Check Instagram user", default="")
parser.add_argument("--number", help="Number of pages to retrieve (11 per page)", type=int, default=2)

parser.add_argument("--nudity", help="Detect nudity",action='store_true')
parser.add_argument("--firearm",help="Detect firearm",action='store_true')

###Initialize arguments
args = parser.parse_args()
twitter = args.twitter
instagram = args.instagram
stream_location = args.stream_location
stream_hashtag = args.stream_hashtag
check_user_twitter = args.check_user_twitter
check_hashtag = args.check_hashtag
check_location = args.check_location
check_user_instagram = args.check_user_instagram
firearm = args.firearm
nudes = args.nudity
number = args.number

if twitter:
    print(desc)
    tw = TwitterClass.Twitter(consumer_key, consumer_secret, access_token, access_secret)
    if check_user_twitter:
        if nudes:
            print("Checking last "+str(number) + " photos of user : " + check_user_twitter + " for nudity")
            tw.check_user(check_user_twitter,number, nude=True)
        elif firearm:
            print("Checking last "+str(number) + " photos of user : " + check_user_twitter + " for firearms")
            tw.check_user(check_user_twitter,number,firearm=True)
    elif stream_location:
        if nudes:
            print("Streaming location for nudes")
            print(','.join(map(str, stream_location)))
            tw.stream_location(stream_location, nudes=True)
        elif firearm:
            print("Streaming location for nudes")
            print(','.join(map(str, stream_location)))
            tw.stream_location(stream_location,firearm=True)
    elif stream_hashtag:
        if firearm:
            print("Streaming "+stream_hashtag + " for firearms")
            tw.stream_hashtags(stream_hashtag, firearm=True)
        elif nudes:
            print("Streaming "+stream_hashtag + " for nudes")
            tw.stream_hashtags(stream_hashtag, nudes=nudes)
    else:
        print("3 choices:\n"
              "--" + Fore.GREEN + "stream_location" + Fore.RESET+"\n"
              "--" + Fore.GREEN + "stream_hashtag"+Fore.RESET+"\n"
              "--" + Fore.GREEN + "check_user_twitter"+Fore.RESET+"\n"
              "Pick one")

elif instagram:
    print(desc)
    api = Instagram.Instagram(INSTAGRAM_USER, INSTAGRAM_PASSWORD)
    if check_location:
        check_location = check_location.split(",")
        if firearm:
            print("Checking location " + str(check_location) + " for firearms")
            api.check_location(check_location[0],check_location[1], firearm=True)
        if nudes:
            print("Checking location " + str(check_location) + " for nudes")
            api.check_location(check_location[0],check_location[1], nudes=True)
    elif check_hashtag:
        if firearm:
            print("Checking " + check_hashtag + " for firearms")
            api.check_hashtag(check_hashtag, firearm=True)
        elif nudes:
            print("Checking " + check_hashtag +  " for nudes")
            api.check_hashtag(check_hashtag, nudes=True)
    elif check_user_instagram:
        if nudes:
            print("Checking last " + str(number) + " pages of " + check_user_instagram + " for nudes")
            api.check_user(check_user_instagram, number, nudes=True)
        elif firearm:
            print("Checking last " + str(number) + " pages of " + check_user_instagram + " for firearms")
            api.check_user(check_user_instagram, number, firearm=True)
    else:
        print("3 choices:\n"
              "--" + Fore.GREEN + "check_location" + Fore.RESET+"\n"
              "--" + Fore.GREEN + "check_hashtag"+Fore.RESET+"\n"
              "--" + Fore.GREEN + "check_user_instagram"+Fore.RESET+"\n"
              "Pick one")
else:
    print(desc)

#coord = [-169.6,-71.3,177.4,77.4]
