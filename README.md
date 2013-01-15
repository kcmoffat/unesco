unesco
======
A simple Django quiz app that shows a photo and description of one of the 700+ UNESCO World Heritage Sites, and 
prompts the user for the site's country.  Data is scraped from unesco.org 
using the BeautifulSoup lib in get_unesco_data.py.  MySQL is assumed to be the Django db backend
(setup covered in setup.py).  The app uses Django session management to allow users to leave and return,
resuming the quiz where they left off.
