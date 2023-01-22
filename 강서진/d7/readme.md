* app_data.py
* app_image.py --> relative paths instead of abspath because i use both school laptop and my desktop and they got mixed up 

---01.16.2023---
* blueprints to bind several apps into one. tried to use application factory, but my files were not that organized so i gave up

---01.17.2023 day---
* api.py, join.html, login.html, base.html, ...
* join-login-logout works
* decided not to use jQuery, Ajax scripts because i'm dumb

---01.18.2023 night---
* working on app_post.py, post.html, content.html ...
* added {% if ~ %} in base.html to show login errors & show username at the nav bar when logged in
* sqlalchemy weakref error --> solved via downgrade to 2.5.1, added to requirements.txt
* another error where db table is not automatically generated like it says in models.py --> solved via creating the table by hand.

---01.19.2023 day---
* app_post.py, post.html, content.html, blog.html, edit.html, profile.html, 
* inserting post, delete post works seamlessly - but updating post does not work as intended --> gonna make it work by using both insert & delete
* made all pages usable only when logged in. --> had to account for the part where session['login'] does not exist yet
* made all pages have GUEST appear on top left when they're not logged in yet. 
* profile page now has "Your Recent Posts", where it shows your recent posts.
