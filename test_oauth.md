OAuth2 Test Plan
================

Testing our OAuth2 integration to Meetup isn't trivial, but it's important, so I'm 
documenting the steps here.  That way, you can reproduce (hopefully) the same bugs
that I'm seeing.

The better way to do this would be to, you know, write a crazy Selenium test and 
build a test harness for OAuth2 servers and clients.  But we're trying to get this 
site up in a few weeks, not months.

Current Upstream
----------------

We're using seekslush's [django-oauth2 implementation](https://github.com/sleekslush/django-oauth2).  
Most other code I found online actually only implements OAuth 1.0a.

Prerequisites
-------------

1. create a Heroku app
2. install the free SSL add-on for your app
3. create the database and an admin user:

        manage.py syncdb

4. provide sensitive config data via environment variables:

        heroku config DJANGO_SECRET_KEY=something MEETUP_OAUTH2_CLIENT_ID=something MEETUP_REDIRECT_URI=https://yourapp.herokuapp.com/authorize/

5. [register your app with Meetup as an OAuth consumer](http://www.meetup.com/meetup_api/oauth_consumers/).  
   Use the redirect URI pattern in the above example.

Running It
----------

1. login into django via https: https://yourapp.herokuapp.com/admin/

    Yes, this is a crutch, and should not be necessary.

2. get the login link for meetup, and verify the query components: http://yourapp.herokuapp.com/login/
   
    Your client id and redirect URI should show up in the link.

3. Click the link and go to Meetup
4. Authorize the request on Meetup
5. You should be redirected to your bounty board instance


Results
-------

As of this writing, you should receive the error, "Missing client id."  This is because the OAuth2 code
assumes that the authorization and token URLs are different, which is explicitly denied in the spec.

More to come.
