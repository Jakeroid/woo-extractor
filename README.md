Woo Extractor 
=====

This is a simple Python script for scrapping products from the WooCommerce stores.
Output file is standard csv format with product title, description, price and one image.

Installing
-----
git clone https://github.com/Jakeroid/woo-extractor
cd woo-extractor
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt

How to use?
-----

Just run a command ```python main.py https://example.com/```. Don't forget to replace example.com for your target. 