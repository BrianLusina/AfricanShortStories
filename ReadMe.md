# African Short Stories

This is a website featuring some of Africa's best short stories titled Hadithi. The site has a sample of 10 short stories and allows the user the ability to share each story on social media. Even make a comment on each story.

Technologies used:
+ HTML
+ CSS
+ JavaScript jQuery library

## setup with Heroku
Run this in terminal:

``` sh
$ heroku addons:add heroku-postgresql:hobby-dev
```

Setup DATABASE_URL variable

``` sh
$ heroku pg:promote HEROKU_POSTGRESQL_<COLOR>_URL
```

Initialize the database locally

``` sh
$ python manage.py init_app
```
> this will initialize the application's db with Postgres

Initialize the db on Heroku

``` sh
$ heroku run python manage.py init_app
```
> creates an initial db on Heroku

