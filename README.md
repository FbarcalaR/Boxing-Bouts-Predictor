# Boxing Bouts Predictor
Project made with python to scrape data from boxrec.com and analyse the bouts using machine learning.

## Data
In this project there are to .csv containing the data:
- **boxing-bouts-data.csv** has been scraped, using this project, from boxrec.com
- **boxing_matches.csv** was taken from another project: https://github.com/EmmS21/SpringboardCapstoneBoxingPredictionWebApp, the creator also has a post where he explains all the project creating process:https://hackernoon.com/d-nr1o32po.
Also, some changes were made during the creation of this project, like changing strings for the boxers stance to a code number and the same for indicate who won the bout.
  
## Scraping
For the scraping part, the projects takes the data from boxrec.com some main parts of this scraping process are:
- A scraper, made with the requests library from python
- Another scraper made using selenium, to try to make the scraper more like a human
- A recaptcha solver, used to solve the recaptchas that the page requests to solve time to time, made following this article: https://ohyicong.medium.com/how-to-bypass-recaptcha-with-python-1d77a87a00d7
- A proxies generator, which just takes a random proxy ip from http_request_randomizer library and returns it converted so the requests library can use it
- A mouse movement script to add a more human look a like
  
Right now, after several requests, boxrec.com could ban the users IP so the page cannot be accessed again

## Machine learning
The machine learning part consists in an unique script wich takes the data from a csv, filters it to get the boxers similar to the inputs of the user and then creates a model to work and train with the given data. Onece the model is trained, the makes a prediction with the given boxers.
Usually, the resulting accuracy is around 70%~80%, but the tests had not too much data to be reliable.

## Improvements
Some improvements for this projects could be:
- Change a bit the scraper, so the users IP does not get banned. Maybe more human like o just using googles cached pages, and change the way it scrapes the data as only the boxers profiles are cached and not all the bouts pages.
- Try different activation functions for the ml script. As this was my first project using this kind of libraries, I am sure there is room for improvement.
