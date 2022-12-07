#FOMO.com

Welcome to #FOMO.com!

Ideally, the website should be hosted publicly on a server, but Heroku is no longer available for free, and several of the alternatives such as Dokku aren't able to store persistent data, as in a Postgres database. Nevertheless, the website works perfectly fine as is, only that the SQL database will be stored locally! This README document will walk you through its entire functionality, beginning from a clean slate.

1. SET UP.
Install all the requirements in requirements.txt.
To start, enter the following code into your terminal:
    python3 -c "import os; print(os.urandom(32).hex())"
What you will retrieve is a secret key associated with your Flask server. Go into config.py and replace the string "YOUR_KEY_GOES_HERE" with the key, formatted as a string. Now, enter the following code into your terminal:
    flask run
You're all set! Click into the link that appears to enter the website.

***** POPULATING THE DATABASE FROM SCRATCH *****
The Flask application references a database <fomo>.db within the instance folder; it gets created if not already there when the application is run for the first time. Right now, in its stead is a database called <test>.db, so when the application is run as is, <fomo>.db will be created. This is intentional; the following instructions are so that YOU can populate the database yourself in the testing process. However, if you'd like to see it with an already populated database, feel free to rename <test>.db into <fomo>.db.

2. REGISTER AS A USER.
When the site loads, you will be automatically directed to the Login page. Note that if you try to enter any paths meant only for users such as "/parties", "/host", or "/", for example, you will be re-routed to the login page. Notice that when logged out, the navigation bar only has two routes: Register and Login. From the Login page, let's click "Create an account" to create a new account. Notice that you can toggle between registering as a User and an Organization using the hyperlink below the "Register" button. Let's register as a User first. Leaving any field blank, or providing an invalid email address, will cause the form to fail in submissions. Let's register using the following credentials:
    Name: Angela
    Email: a@gmail.com
    Password: a (or anything convenient for you to test!)
We're all logged in! Notice that the nav bar now contains 4 items: Home, Organizations, Parties, and Log Out. For now, let's Log Out.

3. REGISTER AS AN ORGANIZATION.
Let's go to the register page, but now as an organization. You can use the hyperlinks to get there or follow the path "register/org". Again, all fields must be completed for the form to be validated, so go ahead and use these, or come up with your own if you wish:
    Name: Lemonade Lovers Club
    Photo URL: https://tinyurl.com/eb6uj249
    Description: We love drinking lemonade!
    Email: lemonade@gmail.com
    Password: l
To help visualize the "Organizations" page better, log out and register another organization with these credentials:
    Name: Grass Association
    Photo URL: https://tinyurl.com/v8h6ktjj
    Description: Touching grass is our passion.
    Email: grass@gmail.com
    Password: g

4. HOST A PARTY.
When logged in as an organization, note that the additional "Host a Party" hyperlink appears on the navigation bar. Now, while still logged in as the Grass Association, click on the link and let's host a party! Leaving any field blank, or providing a date-time later than the current moment, will be rejected. Fill in the form with this info:
    Name: Roll On The Grass 2022
    Date: 20/12/2022
    Time: 2:00PM
    Duration: 2
    Location: Sever Yard
    Photo URL: https://tinyurl.com/mrysnffe
    Description: Our fifth rendition of Roll on the Grass, it's time to get close with nature!
To help visualise the "Parties" page better, let's pencil in another event:
    Name: Pick Your Favorite Leaf
    Date: 15/12/2022
    Time: 10:00AM
    Duration: 1.5
    Location: Boston Commons
    Photo URL: https://tinyurl.com/k2yu5852
    Description: We walk all around Boston Commons just to find a leaf that means something to us.

5. HOST A PARTY IN THE PAST (FOR TESTING PURPOSES).
Some functionality requires that a party has happened in the past. To test this, go into "forms.py", and comment out lines 21-30, which is the validate function within the HostPartyForm. This disables the validation mechanism that prevents past parties from being hosted. Reload the site, then log out and log into the Lemonade organization to host a party using this information:
    Name: Lemon Squeezing Competition
    Date: 15/11/2022
    Time: 9:00PM
    Duration: 3
    Location: Matthews Basement
    Photo URL: https://tinyurl.com/5n8fmah9
    Description: How hard can you squeeze...?
Once done, go back and un-comment the code in forms.py. When redirected to the homepage, you should notice that the Lemonade event isn't shown on the homepage -- as it shouldn't be, since it has already happened.

6. EXPLORE ALL THE PAGES.
Now, the populating of the database is done! Now, let's explore as a user, so log out and log into Angela's account (though it's fine to do this as an organization, which is simply a user with extra privileges).

Go to Organizations through the navigation bar, and take a look at all the organizations; click the hyperlinks to go into the page of any one organization, where you'll see their information and the parties they've hosted / will be hosting.

Now, go to Parties through the navigation bar, and take a look at all the upcoming and past parties; click the hyperlinks to go into the page of any one party, where you'll see its information and a Comments section! If you're on one of the parties happening in the future, you'll notice that there's no option to review the party. But head over to the one that's already happened, and you'll see such an option exists!

7. MAKE A REVIEW.
Once on the page of the past party (the Lemonade event), check out the review section, which is another form to be filled out. Fill it out multiple times if you wish (like a true fan), and watch the average ratings for music, vibes and drinks change!