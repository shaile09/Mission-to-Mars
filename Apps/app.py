from flask import Flask, render_template
from flask_pymongo import PyMongo
import Scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/app"
mongo = PyMongo(app)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = Scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run()
