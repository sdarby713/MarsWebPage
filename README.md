# MarsWebPage

The project here was to build a generalized web page about Mars scraped and pulled together from other web pages.

Each element required a slightly different procedure.  The Mars News blurb simply used Beautiful Soup to pull an article_teaser_body from mars.nasa.gov/news.

Obtaining the featured image required starting at www.jpl.nasa.gov/spaceimages/?search=&category=Mars, then using splinter to navigate by partial text first to "FULL IMAGE" then to "more info".  Even then, soup needed to build the full url from a fragment scraped from this page.

The Mars weather report came from a twitter tweet.  Mars Facts started at space-facts.com/mars and pulled a table using soup.find_all which was then converted into an html table.

Finally, Mars Hemisphere images required using splinter to navigate from 
astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars to individual hemisphere web pages to collect their images.

Because this page uses a python flask app, we need to first start it up with the command python app.py, then bring up the page using url localhost:5000
