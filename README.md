# Website-scraper

# Setup Guide: How to Configure Your System to Run the Web Scraper

Step 1: Install Python
First, ensure Python 3.x is installed on your system.

✅ Check if Python is Installed
Open your Command Prompt (Windows) or Terminal (Mac/Linux) and run:
python --version
or
python3 --version

If Python is installed, it will show something like:

Python 3.10.6

#  Step 2: Set Up a Virtual Environment (Optional, but Recommended)
python -m venv scraper_env

Activate the environment:

✅ Windows (Command Prompt)
scraper_env\Scripts\activate

✅ Mac/Linux
source scraper_env/bin/activate

Your terminal should now show something like:
(scraper_env) C:\Users\YourUsername>

# 🛠 Step 3: Install Required Python Libraries
Run the following to install the necessary packages:
pip install requests beautifulsoup4 pandas lxml openpyxl

# 🛠 Step 4: Create the Python Script
1️⃣ Open any text editor (VS Code, Notepad++, Sublime, etc.)
2️⃣ Copy and paste the scraper code (from previous response)
3️⃣ Save the file as scraper.py

# 🛠 Step 5: Run the Scraper
Now, in the same terminal where the virtual environment is activated, run:
python scraper.py
🔹 Enter the website URL when prompted
🔹 The script will scrape the title & practice areas
🔹 Data will be saved as scraped_practice_areas.xlsx

# 🛠 Step 6: Open the Excel File
Locate scraped_practice_areas.xlsx in the same folder where scraper.py is saved.
📂 Open it in Excel, Google Sheets, or any spreadsheet tool to view results.
