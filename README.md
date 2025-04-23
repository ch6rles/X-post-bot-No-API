# X-post-bot-No-API
This python bot will use AI to post tweets to your twitter account with no API
We will use ***twikit*** to connect to your twitter account without an API and ***pollinations.ai*** to use LLMs without an API
Before using, do the following:
```
pip install -r requirements.txt
```
Afterwards, make sure to write your values in for **twitter_username**, **twitter_email**, and **twitter_password**


# *Important Step*
In twikit you have to change the proxy connections since we wont be using any. 
Navigate to your client.py file in twikit 

![image](https://github.com/user-attachments/assets/92135907-6799-4dda-a909-2c72323282b9)

Set self.http to AsyncClient(**kwargs)




