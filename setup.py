from MySQLdb import connect
import get_unesco_data

# First create a MySQL db on localhost to store scraped UNESCO site data.
# $sudo mysql -u root -p
# ->CREATE DATABASE site_data
# ->CHARACTER SET utf8
# ->COLLATE utf8_general_ci;

# Run the following line to get all available UNESCO site data.  Takes approx. 2 hours.
# unesco_data = get_unesco_data("http://whc.unesco.org/en/list/", 1, 1404)

# Store the retrieved data on localhost.
# Make sure you have python-mysqldb installed first
# $sudo apt-get install python-mysqldb
db = connect(host = "localhost", user = "root", passwd = "*****", db = "site_data", charset='utf8')
c = db.cursor()
c.executemany(
    """INSERT INTO sites (unesco_id, name, country, site_url, image_url, brief_desc, long_desc, is_404, is_complete)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
    unesco_data
)
c.close()
db.commit()
db.close()

# Next create a dummy MySQL db to be used by django:
# $sudo mysql -u root -p
# ->CREATE DATABASE unesco
# ->CHARACTER SET utf8
# ->COLLATE utf8_general_ci;
 
# Now run 'python manage.py syncdb' in project directory and insert scraped site_data:
# $sudo mysql -u root -p
# ->insert into unesco.quiz_country (name)
# ->select distinct country from site_data.sites where is_complete = 1 order by country;

# ->insert into unesco.quiz_site (unesco_id, name, country_id, site_url, image_url, brief_desc, long_desc, is_404, is_complete)
# ->select unesco_id, name, (select id from unesco.quiz_country c where c.name = sites.country), site_url, image_url, brief_desc, long_desc, is_404, is_complete
# ->from site_data.sites where is_complete = 1;
