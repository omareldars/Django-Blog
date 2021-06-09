# Team Django-Blog for ITI-Intake 41
ITI Intake-41 Open-Source Track, 9-months Diploma

# Team Members:
1- Omar Abd El-Aziz <br /> 
2- Ahmed El-Baiomy <br /> 
3- Ekhlas Mohamed <br /> 
4- Asmaa El-Alfy <br /> 
5- Eslam El-Shaabany <br /> 

# Project Features:
      => User-Privilege:
1- User Can Add Posts. <br /> 
2- User Can Delete his own Posts. <br /> 
3- User Can Comment and Reply on his posts and others also. <br /> 
4- User Can Like and Dis-like on his posts and others also. <br /> 
5- User Can Subscribe Categories of his own interest. <br /> 
6- User Can navigate to posts related to those categories. <br /> 
7- User Can Create Tags of his own interest on Creating posts and subscribe them. <br /> 
8- User Can navigate to posts related to those Tags. <br /> 
9- Comments and Replies will be filterd upon specific list of words and if  <br /> 
    one word of this list exists, it will be replaced with *'s of word length. <br /> 
10- User Can Edit his own Profile Settings. <br /> 
11- User Can Search by post-title, tag or category. <br /> 

      => Administrative-Privilege:
1- Admin Can do Anything on the system, but cannot login as super-user. <br /> 
2- User Can be promoted to Admin or Super-User. <br /> 
3- Posts with more than 10 Dis-likes will be auto-deleted. <br /> 
4- Categories and Forbidden words can only be created with admin or super-admin privilege. <br /> 
5- Admin Can Block or Un-Block Users, blocked users cannot log into the system. <br /> 



# Feature Work
1- Add Email Feature to subscribe for specific categories and get notifications for them. <br /> 
2- User will be auto-blocked on reaching specific number of forbidden words. <br /> 
3- User will be auto-deleted on reaching specific number of reptitve blocks. <br /> 
4- Deploy on one of the Hosting Services, thus it can be reached online. <br /> 



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
-> Its time to enjoy our website, and if you have any comments or features you want to add, <br /> 
    just tell us. :D
