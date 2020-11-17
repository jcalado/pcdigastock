# Install dependencies

pip install -r requirements

# Configure

links.txt
Add URLs for the items you want to monitor. One per line.

config.py
Add your pushover app token and client key.

# Run

python scrape.py

# Ouput

## Terminal output
![Terminal output](https://github.com/jcalado/pcdigastock/raw/master/screenshots/output.png "Terminal output")

## Pushover notification on your device
Will warn about how many products are out of stock or inform that everything is awesome!
