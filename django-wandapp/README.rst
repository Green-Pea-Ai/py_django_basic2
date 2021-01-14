==========
Wandapp
==========

Wandapp is a Django app to conduct Web-based polls.

For each question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "wandapp" to your INSTALLED_APPS setting.py like this::

	INSTALLED_APPS = [
		...
		'wandapp',
	]

2. Include the wandapp URLconf in your project urls.py like this::

	path('wandapp/', include('wandapp.urls')),

3. Run ``python manage.py migrate`` to create the wandapp models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll(you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/wandapp/ to participate in the poll.