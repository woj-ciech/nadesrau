# nadesrau
Detect firearm and nudity on Twitter and Instagram

It uses Tensorflow object detection API and nudity python package. 
Dataset was borrowed from https://github.com/sofwerx/tensorflow-gun-detection and model has been trained in Google ML Cloud to 150k steps with total loss approx 1,4.

# Requirements 
- Tensorflow object detection (https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)
- nudity
- InstagramApi
- colorama
- matplotlib
- tweepy
- Add method to InstagramAPI to retrieve location (https://github.com/LevPasha/Instagram-API-python/pull/492/commits/ed74ee45fb3e3abe6df7f767d3353de6fd897401)

```
pip install -r requirements.txt
```
Fill in API keys for Twitter and credentials for Instagram in lines 33-39

# Usage
```
C:\models-master\research\object_detection>python nadesrau.py -h
Fail to import moviepy. Need only for Video upload.
usage: nadesrau.py [-h] [--twitter] [--instagram]
                   [--stream_location STREAM_LOCATION [STREAM_LOCATION ...]]
                   [--stream_hashtag STREAM_HASHTAG]
                   [--check_user_twitter CHECK_USER_TWITTER]
                   [--check_hashtag CHECK_HASHTAG]
                   [--check_location CHECK_LOCATION]
                   [--check_user_instagram CHECK_USER_INSTAGRAM]
                   [--number NUMBER] [--nudity] [--firearm]

 +-'~`---------------------------------/\--
 ||"""""""""""""""""""""""""""""""" \\\  \/~)
 || asciiart.eu                      \\\  \/_
  |~~~~~~~~-________________-_________________\ ~--_
  !---------|_________       ------~~~~~(--   )--~~
    Gun & nudity       \ /~~~~\~~\   )--- \_ /(
      detection        ||     |  | \   ()   \
   Twitter & Instagram \____/_ / ()\        \
      |||||             `~~~~~~~~~-. \        \
     ||. .||                        \ \  <($)> \
    |||\=/|||                        \ \        \
    |.-- --.|                         \ \        \
    /(.) (.)\                          \ \        \
    \ ) . ( /   medium.com/@woj_ciech   \ \  ()    \|
    '(  v  )`   github.com/woj-ciech    _\_\__====~~~
    \
Example:\python3 nadesrau.py --twitter --stream_hashtag #booty --nudity\
       python3 nadesrau.py --instagram --check_user_instagram kimkardashian --firearm\
       python3 nadesrau.py --twitter --stream_location -169.6 -71.3 177.4 77.4 --firearm\
       python3 nadesrau.py --instagram --check_hashtag kids --nudity

optional arguments:
  -h, --help            show this help message and exit
  --stream_location STREAM_LOCATION [STREAM_LOCATION ...]
                        Twitter location streaming
  --stream_hashtag STREAM_HASHTAG
                        Twitter hashtag streaming
  --check_user_twitter CHECK_USER_TWITTER
                        Check Twitter user
  --check_hashtag CHECK_HASHTAG
                        Check Instagram hastahg
  --check_location CHECK_LOCATION
                        Check Instagram location
  --check_user_instagram CHECK_USER_INSTAGRAM
                        Check Instagram user
  --number NUMBER       Number of pages to retrieve (11 per page)
  --nudity              Detect nudity
  --firearm             Detect firearm
```

# Example
```
C:\models-master\research\object_detection>python nadesrau.py --twitter --stream_hashtag guns --firearm
Fail to import moviepy. Need only for Video upload.
 +-'~`---------------------------------/\--
 ||"""""""""""""""""""""""""""""""" \\\  \/~)
 || asciiart.eu                      \\\  \/_
  |~~~~~~~~-________________-_________________\ ~--_
  !---------|_________       ------~~~~~(--   )--~~
    Gun & nudity       \ /~~~~\~~\   )--- \_ /(
      detection        ||     |  | \   ()   \
   Twitter & Instagram \____/_ / ()\        \
      |||||             `~~~~~~~~~-. \        \
     ||. .||                        \ \  <($)> \
    |||\=/|||                        \ \        \
    |.-- --.|                         \ \        \
    /(.) (.)\                          \ \        \
    \ ) . ( /   medium.com/@woj_ciech   \ \  ()    \|
    '(  v  )`   github.com/woj-ciech    _\_\__====~~~
    \
Example:\python3 nadesrau.py --twitter --stream_hashtag #booty --nudity\
       python3 nadesrau.py --instagram --check_user_instagram kimkardashian --firearm\
       python3 nadesrau.py --twitter --stream_location -169.6 -71.3 177.4 77.4 --firearm\
       python3 nadesrau.py --instagram --check_hashtag kids --nudity
Streaming guns for firearms
[i] Downloading https://pbs.twimg.com/ext_tw_video_thumb/1108882660787658757/pu/img/sPJ2AOe6e8w5qTrG.jpg into hashtags/guns/griffint15.jpg
    Firearm detected
C:\models-master\research\object_detection\venv\lib\site-packages\matplotlib\figure.py:445: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figu
re.
  % get_backend())
    Username: Tishae G....
    Screen name: griffint15
    Text: RT @ILoveBeinBlack: Lmaooo stop playing with guns 🤦🏾‍♂️ https://t.co/jfMWGbrn4m
    Moving to /artifacts
[i] Downloading https://pbs.twimg.com/ext_tw_video_thumb/1108889991214587904/pu/img/v__BQ4M7_UTjQP44.jpg into hashtags/guns/longmicropenis.jpg
No firearms detected
[i] Downloading https://pbs.twimg.com/media/D2QPn8PWkAAQJGf.jpg into hashtags/guns/WGAL.jpg
No firearms detected
[i] Downloading https://pbs.twimg.com/media/D2MqBKyWwAAc4RX.jpg into hashtags/guns/StephenMcLbrtrn.jpg
No firearms detected
[i] Downloading https://pbs.twimg.com/media/D2IYxnbXQAE7AMl.jpg into hashtags/guns/CarlosJocGomez.jpg
No firearms detected
[i] Downloading https://pbs.twimg.com/tweet_video_thumb/D2QP2vsX0AAgMwh.jpg into hashtags/guns/GABguy66.jpg
No firearms detected
[i] Downloading https://pbs.twimg.com/tweet_video_thumb/D2QQCwKWwAAIIvd.jpg into hashtags/guns/Remedi_RPM.jpg
    Firearm detected
    Username: Oli Remedi
    Screen name: Remedi_RPM
    Text: @rosspeacock @JohnWickMovie Guns, lots of guns. Nice direct reference there! https://t.co/KqQI5eUebB
    Moving to /artifacts
[...]
```

```
C:\models-master\research\object_detection>python nadesrau.py --instagram --check_user_instagram squat4datbody --nudity --number 1
Fail to import moviepy. Need only for Video upload.
 +-'~`---------------------------------/\--
 ||"""""""""""""""""""""""""""""""" \\\  \/~)
 || asciiart.eu                      \\\  \/_
  |~~~~~~~~-________________-_________________\ ~--_
  !---------|_________       ------~~~~~(--   )--~~
    Gun & nudity       \ /~~~~\~~\   )--- \_ /(
      detection        ||     |  | \   ()   \
   Twitter & Instagram \____/_ / ()\        \
      |||||             `~~~~~~~~~-. \        \
     ||. .||                        \ \  <($)> \
    |||\=/|||                        \ \        \
    |.-- --.|                         \ \        \
    /(.) (.)\                          \ \        \
    \ ) . ( /   medium.com/@woj_ciech   \ \  ()    \|
    '(  v  )`   github.com/woj-ciech    _\_\__====~~~
    \
Example:\python3 nadesrau.py --twitter --stream_hashtag #booty --nudity\
       python3 nadesrau.py --instagram --check_user_instagram kimkardashian --firearm\
       python3 nadesrau.py --twitter --stream_location -169.6 -71.3 177.4 77.4 --firearm\
       python3 nadesrau.py --instagram --check_hashtag kids --nudity
Request return 429 error!
{'message': 'Please wait a few minutes before you try again.', 'status': 'fail'}
Request return 404 error!
Login success!

Checking last 2 pages of squat4datbody for nudes
squat4datbody
Power Of The Booty
🥇 #Booty Connoisseur
📲 DM & Tag for Features
📸 Photographer
📍 South FL
👇 My Favorite Fitness Suppliments
http://shop.teamxnd.com/squat4datbody/Home
[i] Downloading https://scontent-frt3-2.cdninstagram.com/vp/74f3424ff48f4383d1c0b66d0365f2ba/5D48B1DB/t51.2885-15/sh0.08/e35/p750x750/53375621_394419411339740_7834832402014544329_n.jpg?_
nc_ht=scontent-frt3-2.cdninstagram.com&ig_cache_key=MjAwNDU1NTYzNTgyMDUxNDUzMg%3D%3D.2 to users/squat4datbody/image0.jpg
Detected score: 0.9717
    Found nude
    Timestamp: 2019-03-21 15:21:14
    Text: Show @missemilymorgan some ❤️on her BOOTY gains!
@missemilymorgan
@missemilymorgan
    Moving to /artifacts
[i] Downloading https://scontent-frt3-2.cdninstagram.com/vp/f66a53d6c91b84f2fcb8589c02ffbed4/5D1488C4/t51.2885-15/sh0.08/e35/p750x750/52435303_2099739970266661_9078398841521010466_n.jpg?
_nc_ht=scontent-frt3-2.cdninstagram.com&ig_cache_key=MjAwMzgzMjEyMDU3ODIzMTkwNw%3D%3D.2 to users/squat4datbody/image0.jpg
Detected score: 0.0266
[...]
[i] Downloading https://scontent-frt3-2.cdninstagram.com/vp/31b02c9b1cfccdb49d35ab29baa49946/5C96CC58/t51.2885-15/e15/52481048_326772511518115_2904375443973453617_n.jpg?_nc_ht=scontent-f
rt3-2.cdninstagram.com to users/squat4datbody/image7.jpg
Detected score: 0.0557
Whoregrade: 0.2909354302785389

```

Following directory structure is created for each category, inside of 'artifacts' folder, every detected assset is placed

![](https://i.imgur.com/oUSEL3V.jpg)

# Output
![](https://i.imgur.com/GRvcorx.jpg)

![](https://i.imgur.com/TxgU77S.jpg)

# Additional
Be prepared for disturbing content, not for gentle people.
Tested on Windows 7 and 10.
