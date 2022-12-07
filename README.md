#FOMO.com

Welcome to #FOMO.com!

Ideally, the website should be hosted publicly on a server, but Heroku is no longer available for free, and several of the alternatives such as Dokku aren't able to store persistent data, as in a Postgres database. Nevertheless, the website works perfectly fine as is, only that the SQL database will be stored locally! This README document will walk you through its entire functionality, beginning from a clean slate.

1. SETTING UP
To start, enter the following code into your terminal:
    python3 -c "import os; print(os.urandom(32).hex())"
What you will retrieve is a secret key associated with your Flask server. Go into config.py and replace the string "YOUR_KEY_GOES_HERE" with the key, formatted as a string. Now, enter the following code into your terminal:
    flask run
You're all set! Click into the link that appears to enter the website.

2. REGISTER / LOGIN FUNCTIONALITY
Notice that the path is currently "/login". If you try to enter any paths meant only for users