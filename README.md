# Twitter Analysis Service

## Overview
This project is a web service for analyzing Twitter data. It provides APIs for user recommendations and other Twitter-related analytics.

## Table of Contents
- [Twitter Analysis Service](#twitter-analysis-service)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Project Structure](#project-structure)
  - [Setup](#setup)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
  - [API Endpoints](#api-endpoints)
  - [Troubleshooting](#troubleshooting)
  - [Future improvements](#future-improvements)

## Prerequisites
- Docker and Docker Compose
- Python 3.9+
- PostgreSQL

## Project Structure
twitter_analysis_service/
├── app/
│   ├── api/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── init.py
│   ├── config.py
│   └── main.py
├── etl/
│   ├── init.py
│   ├── etl_process.py
│   └── run_etl.py
├── tests/
│   ├── init.py
│   └── conftest.py
├── .env
├── .gitignore
├── create_test_db.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run_tests.sh
└── README.md

## Setup

1. Clone the repository:

git clone https://github.com/Jaman-dedy/twitter_analysis_service.git
cd twitter_analysis_service

2. Create a `.env` file in the project root and add the following:

```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=twitter_analysis
```

3. Build the Docker images:
```
docker-compose build
```

## Running the Application

1. Start the services:
```
docker-compose up
```

2. The API will be available at `http://localhost:8000`.

3. To stop the services:

```
docker-compose down
```

## Running Tests

1. Ensure the database service is running:

`./run_tests.sh`

This script will:
- Set up a virtual environment
- Install dependencies
- Run pytest

## API Endpoints
List of all endpoints
![alt text](image.png)

- `GET /`: Welcome message
- `GET /api/recommendations/q2`: User recommendations
- Query Parameters:
 - `user_id`: string
 - `type`: string (reply, retweet, or both)
 - `phrase`: string (percent-encoded)
 - `hashtag`: string


```js

http://localhost:8000/api/recommendations/q2?user_id=2401535519&type=retweet&phrase=سكس&hashtag=سكس

```


```js
TeamCoolCloud,1234-0000-0001
2391861971	sexwm19		RT @nek_salb: سكس محارم جامد مصري 

http://t.co/ilO1qoGIIN
 
#روابط_سكس #سكس #سكس_عربي #سكس_ورعان #سكس_خليجي #ورعان  #محارم
255969599	T_88866	انا انا وانت انت وهم هم وكلن لنفسه (#تحبني_أحبك) ♡	RT @18ssoo18: سكس إيطالي
http://t.co/Qhc0dlsjn9

#محارم #سكس_عربي #افلام_سكس #سكس #سكس_خليجي #زب #كس #افلام #زب #عنيف #رتويت #فحل #مشتهيه #…
805927515877494784	14marcoo		RT @Unictam2: يدخله كذه في #سكس

الفيلم كامل
👇
https://t.co/kadDXHc2vo   

#سكس
 #سكس ☕☃️ سكس

https://t.co/0iPLrt8Vo9 

https://t.co/a38sq…
768592441536544770	gttrrea		RT @saoasasmaa: شاهد مقطع سكس فرنسى جديد

#محارم نيك سكس

🌈 https://t.co/6YYzLyzdrY 🌈

🎬📲 https://t.co/pGSx7Fei7k;

سكس ورعان #سكس #محارم…
811991048964702208	sameha481		RT @sasohot8: مموس مصرية خبرة من منطة شعبية
 مقاطع #سكس 😍

🔥 https://t.co/44ohamWS3X📱🎬

🔥https://t.co/9RvApdcc13 📱🎬

#افلام_سكس #سكس_عربي
809853426502946817	memo19988888	i was there , in the dark . living among the dead . praying in silance .	RT @qahbbatsex: بزازها مثالية
   ❌
🔞✅https://t.co/Y8WXxmBJvN 

#سكس

🔰
 🎱 
🇽️🇪️🇸️

🏁https://t.co/0clBP2tW17 
سكس ورعان
محارم
#افلام_سكس
مساج
791619294442430464	dao_kss		RT @gens24haiu: عامل النظافه بالديسكو ينيك مراهقه
🇳️🇷️🇴️🇵️ #سكس

🔰
https://t.co/J1w4NIvU6Y
https://t.co/zR8nEWlr8y

مقاطع سكس
افلام سكس متر…
770969016894717952	TyjfxdTrojan	ممحونه	RT @ughpi81: بنت مصريه تتناك  في الحمام ?

? https://t.co/oiJrH5jAEl 

? https://t.co/Z64C719kBV 

#افلام_سكس
#سكس

#نيك افلام سكس اجنبي
2896822242	surialolo		RT @oreserDS: مقطع جديد بنت طيزها حلوه نايمه على بطنها

سكس ورعان
http://t.co/n3M3ZMjPEs

نيك الطيز
http://t.co/blzUyj3OpH

#سكس_عربي #سكس …
2395204487	sexwm33		RT @_3RBi_: #سكس_عربي *مميز*
×اللحق قبل الحذف

http://t.co/hTe6L3IJYp
http://t.co/tBXamdn146

#سكس #نيك #نيج #مص #زب #افلام_سكس http://t.co…
125307657	mjiof	احَبُ الُبُنَاتّ اكثٌرً شَيّ بُسّ تّعّبُتّ خِلُاصّ كلُ شَيّ ابُيّ هّمُ الُوٌرًعّيّنَ ابُيّ وٌشَميّلُاتّ وٌيّنَهّمُ وٌسّوٌالُبُ خِلُ يّجَوٌبُسّ ُ	RT @TetoM388: “@Dr__porn: شايب ينيك شقراء في الحديقه ورا الشجره 
 http://t.co/RsnSyXiT6a
#ريتويت_سكس  #افلام_سكس
#روابط_سكس #ريتويت_للمزيد”
816433992291536896	9YNYana7PweGeFD		RT @kulaginmalei15: خال ينيك ممحونتين مصريات

📺
🔞💥https://t.co/S8jUx5rd7O💥

#سكس

🔞
💥https://t.co/50iHiSCSxt;💥 
🇽️🇪️🇸️

📺
ورعان
#افلام_سكس…
815955479386095618	iyvxty		RT @d6dom: سكس نيك سمرا خلفي من خال ولا احلى

https://t.co/slXbseu2mK

#سكس
https://t.co/phK2uqqLtR
lk
https://t.co/YRiYZzcYa0
815229986361593856	sose57614302		RT @dgnkrgtj: كس وطيز بنت لبنانية عسل تتناك براحة
 🏮🌱https://t.co/SNezjCLCSE

💢💢💢🏁💢 #سكس
⛳️https://t.co/rfqYokZp4G
مشتهيه
#افلام_سكس
خلفي
811441818156101632	pornooxsx		RT @kulaginmalei15: عراقيه تنتاك من ورع خلفي

📺
🔞💥https://t.co/S8jUx5rd7O💥

#سكس

🔞
💥https://t.co/50iHiSCSxt;💥 
🇽️🇪️🇸️

📺
ورعان
#افلام_سكس…
810569543433256960	A8dda8jjRafio		RT @frew49: سكس ورعان اجنبي برازيلي

🔥https://t.co/jbKdNQMB2C 📱🎬

🔥https://t.co/gTo8Lrr3hT 📱🎬

#سكس  #ورعان
805930050608570369	14orangee		RT @30panadol: سكس صغار مثير حصري BRAZZERS

👇
الفيلم من هنا
https://t.co/vJHhnudhXv      

#سكس
سعودي
https://t.co/MxAbMrrjQq 

https://t.c…
766979571157569536	mnjhccc		RT @eerrcg1: مش لاقيه حد يطفى نااار جسمها

🌈 https://t.co/tPv0iw1ihj 🌈

#محارم نيك سكس

🌈 https://t.co/LsvfcFHYSv 🌈

افلام سكس #نيك #محارم…
2512160929	FddfvdcCfvfv		RT @a7_altaif2233: بشوفف كم تستآههل ريتويت ' يَ ححلوين #افلام_سكس_نيك_ورع_نيك_ورعان_سكس_صغار_اغتصاب_ #آبي_آقوى_رتويت http://t.co/3o3AhlJ3lA
2402594345	6_3rb12		RT @nek_salb: ورعان سعوديين 
لعشاق الورعان طبعا

http://t.co/1HrtgtfoRE

#سكس #سكس_عربي #محارم #نيك #ديوث #سالب http://t.co/TD1XIsMFfN
2351221983	aljubail4	صصوري بالبآيو السالب الججاد يجي خاص أوصافي ٢٤/١٦٣/٥٢  ••|| ـالجبيل ـالصنآعية ||••	RT @Mzyoon86: فلمين برابط واحد - ساعه ونص من المجون 👍

http://t.co/A2Tmy0Enjd

#سكس  #فلم_سكس  #نيك  #نيج  #مص #لحس
2291995602	zoom2540		RT @Dyooth_x: وش رايكم في طيز أختي
#محارم #ديوث #دياثه #ديوث_اختي #حملة_مليون_ديوث #تجسس_محارم #قحبه #قحاب #قحبات #سكس #سكسية #نيك http://t…
815689902281134080	nfqxo		RT @zdtak: مولع تتساحق مع صديقتها وتكب 

 https://t.co/4Q2n5sGc0F  

 #سكس 
 https://t.co/X6YExfVdRX  

 https://t.co/aULL0JBAYk
 37181
812949250627817472	TXsPCFUfaf8kdZj		RT @sasohot1: كتكوته 18 سنة تخلع ملط وتلعب في كسها
الفيلم👇
🍵https://t.co/VaLuKlEzXS

#سكس

نسخة الفيلم 👇
🐝https://t.co/o42cBtDoIw

https://…
805111043462725632	reem_haleem	صغيرة ولكن اعشق الجنس	RT @bob_gamda: تشوف زبره على موبايل بنتها

مشاهدة 👇
👸https://t.co/Mg3ecMSL9f

#سكس

لينك خاص بالموبايل👇
🐭https://t.co/Qy0my2U4Eh

https://t…
791264133039751170	clips_sex_2016	سكس سعودي
سكس عربي
مقاطع سكس عربي
مقاطع سكس سعودي
تحميل مقطع سكس
سكس ممحونات
افلام و قصص محارم
صور و مقاطع سكس
افلام نيك محارم
سكس محارم و ورعان	RT @guipygu: مصريه تمص زبر عشيقها ?

? https://t.co/YzAcG0Isrs

? https://t.co/jnOog2jzQP

#نياكه
#محارم

#نيك افلام سكس اجنبي
2514812369	44_kk1		RT @mm7onhana: فلم سكس روعة #ريتويت للمزيد رابط الفلم هنا =&gt; http://t.co/JDYj3VIW62
http://t.co/rusBS7kyZQ
2480258504	tbglp1		RT @saraalmsrya: تعارف وزواج دلوعه احب الرياضه والمطالعه والرقص 
http://t.co/F3ImE66JOI
#طيز #قحبه #كس #مكوه #نيك #جنس #ممحونه #سكس #porn #…
2444149864	mnolh1234	انا منال 37 سنه الرياض جاده  والسهر ب50 سوا والباقي بعد السهره	RT @marwa_marwa25: او زبك كبير وعريض تستاهل هل ورده 
#ريتويت #حصريات_مروه #ممحونه #شرموطه #نيك #سكس #زب http://t.co/nJ0j12Bys7
2437165788	Seeexawy		RT @FlmSex1: http://t.co/ZxuzdTJJfE  http://t.co/iaR380xt9t #نياكه #طيز #خلفي #افلام_سكس #ممحونه #صدر #ورعان #كس #ديوث #سالب #قحبه #خلفي #س…
2435606010	MohammedAlyam1i		RT @FlmSex1: http://t.co/94A9a1sPCk  http://t.co/q3SWeYJx6i #نياكه #طيز #خلفي #افلام_سكس #ممحونه #صدر #ورعان #كس #ديوث #سالب #قحبه #خلفي #س…
2422953088	hdhdxxl1		RT @Fa7il655556: #رتويت_سكس لزبيان سحاق http://t.co/xmO68nyB2e اولاد للي طلب http://t.co/7chBCAsqqc
```
- `test-db-connection`: To test if the connexion was established with the data base
```js
{
	"status": "Database connection successful"
}
```

- `Check db status `

```js
{
	"users": 55422,
	"tweets": 39092,
	"hashtags": 67799,
	"user_interactions": 20429,
	"hashtag_scores": 47322,
	"hashtag_frequencies": 35414
}
```
- `clear-database`

```js
{
	"message": "All data has been cleared from the database"
}
```

- `run-etl`
```js
{
	"message": "ETL process started in the background"
}

```

- `etl-status`

```js
{
	"status": "ETL completed",
	"total_duration": "45.25 seconds",
	"users_processed": 55422,
	"tweets_processed": 39092,
	"hashtags_processed": 67799
}
```


For detailed API documentation, visit `http://localhost:8000/docs` when the application is running.



## Troubleshooting

- If you encounter database connection issues, ensure the PostgreSQL service is running and the connection details in `.env` are correct.
- For import errors when running tests, make sure you're using the virtual environment and the `PYTHONPATH` is set correctly.
- If changes are not reflected, try rebuilding the Docker images:

## Future improvements

1. Advanced User Recommendations:
   - Implement machine learning models for more accurate recommendations.

2. Trend Detection:
   - Implement algorithms to detect emerging trends in real-time.
   - Provide visualizations of trending topics and their evolution.

3. Content Categorization:
   - Use natural language processing to categorize tweet content into topics.
   - Provide analytics on the distribution of topics for users or hashtags.

4. Real-time Processing:
   - Implement a streaming data pipeline for real-time tweet analysis.
   - Use technologies like Apache Kafka or AWS Kinesis for data streaming.