# Intro

Matches people to projects, aka "hacks," for colloboration during hack night events.

#  Deploy

1.  Fetch the code via git
2.  Create a heroku app from the git dir:

        cd projectdir/
        heroku apps:create --stack cedar

3.  Do your initial push to heroku:

		git push heroku master

4.  Run `syncdb` to create tables

        heroku run bounty/manage.py syncdb

5.  Apply migrations (see also below):

        heroku run bounty/manage.py migrate board

## Database migrations

Migrations should be versioned in the `board` app's `migrations` dir.  Generate
migrations by running:

    manage.py schemamigration board --auto

Check in the resulting `migrate_*.py` files.

When pushing an update including database migrations, you will want to apply them
in your heroku instance:
    
    heroku run bounty/manage.py migrate board
