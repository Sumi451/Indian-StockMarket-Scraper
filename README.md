# Indian-StockMarket-Scraper
its a flask file hosted on the aws server for scraping realtime data of Indian Stock Market. Keep in mind it only returns current market price and historical graph for a given Stock symbol.
How to Reconnect and Restart Flask Server on AWS EC2 After Logout

Step 1: SSH back into your AWS EC2 instance
To reconnect to your server, open your terminal (or Command Prompt/PowerShell on Windows) and run the following command:
ssh -i your-key-file.pem ubuntu@your-ec2-public-ip
Replace your-key-file.pem with the path to your actual key file (for example, stock-scraper-key.pem). Replace your-ec2-public-ip with the public IP address of your EC2 instance (you can find this in the AWS EC2 dashboard).

Step 2: Activate your Python Virtual Environment
After logging in, you need to re-activate your virtual environment where all the required libraries are installed.
cd ~    # Go to home directory (or the directory where your project is)
source stock-scraper-env/bin/activate
This activates the virtual environment called stock-scraper-env (change this if your environment has a different name).

Step 3: Run the Flask Server
Once the virtual environment is active, start the Flask application again:
python3 stock_scraper_api.py
This will start your server. Make sure your EC2 security group allows inbound traffic on port 5000.

Optional: Check Your Public IP Address
If your EC2 instance was stopped and restarted, the public IP might have changed (unless you attached an Elastic IP). To check your current public IP, run this command inside your EC2 instance:
curl ifconfig.me

Important Note
    • If you close your terminal or disconnect your SSH session, the Flask server will stop running.
    • To keep the Flask app running even after logout, you could use tools like nohup or tmux. (This is optional if you just want to manually restart the server each time.)

Quick Reference Command Summary
Task
Command
SSH into EC2
ssh -i your-key-file.pem ubuntu@your-ec2-public-ip
Activate Virtual Environment
source stock-scraper-env/bin/activate
Start Flask Server
python3 stock_scraper_api.py
Check Public IP
curl ifconfig.me

This document can be saved as your quick-reference guide for restarting your Flask server after logging out of AWS EC2.

End of Document
