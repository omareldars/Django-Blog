# Team Django-Blog for ITI-Intake 41
ITI Intake-41 Open-Source Track, 9-months Diploma

#Team Members:
1- Omar Abd El-Aziz
2- Ahmed El-Baiomy
3- Ekhlas Mohamed
4- Asmaa El-Alfy
5- Eslam El-Shaabany

# Project Features:
      => User-Privilege:
1- User Can Add Posts.
2- User Can Delete his own Posts.
3- User Can Comment and Reply on his posts and others also.
4- User Can Like and Dis-like on his posts and others also.
5- User Can Subscribe Categories of his own interest.
6- User Can navigate to posts related to those categories.
7- User Can Create Tags of his own interest on Creating posts and subscribe them.
8- User Can navigate to posts related to those Tags.
9- Comments and Replies will be filterd upon specific list of words and if 
    one word of this list exists, it will be replaced with *'s of word length.
10- User Can Edit his own Profile Settings.
11- User Can Search by post-title, tag or category
-------
      => Administrative-Privilege:
1- Admin Can do Anything on the system, but cannot login as super-user
2- User Can be promoted to Admin or Super-User.
3- Posts with more than 10 Dis-likes will be auto-deleted.
4- Categories and Forbidden words can only be created with admin or super-admin privilege.
5- Admin Can Block or Un-Block Users, blocked users cannot log into the system.



# Feature Work
1- Add Email Feature to subscribe for specific categories and get notifications for them.
2- User will be auto-blocked on reaching specific number of forbidden words.
3- User will be auto-deleted on reaching specific number of reptitve blocks.
4- Deploy on one of the Hosting Services, thus it can be reached online.



# To Run the project please follow these steps:
# 1- Database Creation
-> Create MySQL DB called "blog"
# 2- Edit Settings File
-> Go to Settings.py file and add your db.user, and db.pass for mysql
# 3- Make The DB-Migrations
-> use command: python3 manage.py makemigrations
-> after that use command: python3 manage.py migrate
# 4- Run The Server
-> use command: python3 manage.py runserver
# 5- For Superuser Creation
-> use command: python3 manage.py createsuperuser
# 6- Enjoy:
-> Its time to enjoy our website, and if you have any comments or features you want to add,
    just tell us. :D
