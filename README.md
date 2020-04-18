# Primenowslot
A python script for refreshing the amazon prime checkout page to find whether there are available slots or not

### Credit
This repo is modified based on this work:
https://github.com/benh57/PrimeNowNotifier

The main changes are:
1. When slots are open, it will pop-up a notification to the macOS notification center. 
2. Use the wxpython framework to make the IO within the browser functioning normally
3. Use multithreading, so that the browser won't freeze during sleeping

### Requirement
- CEFpython3
- wxpython
- beautifulsoup4

### Usage
 1. Go to notification center setting in MacOS and set the notification from Script Editor to "Alerts" (optional)
 ![Image of Notification Setting](https://github.com/ruochiz/Primenowslot/blob/master/figs/fig2.png)
 2. ```$ pythonw primenow.py --enable-say --username=<your-amazon-email> --password=<your-password> --sleep=<seconds-between-refresh>```
    - After you install wxpython, you should use pythonw instead of python
    - The username and password options are optional. You can type in them later
 3. After loading the page, navigate to the checkout page
 4. Wait for the notification for new slots~
 
 ![Image of Notification](https://github.com/ruochiz/Primenowslot/blob/master/figs/fig1.png)
 
 5. For those who are addicted to Oatly oat milk. Run oatly.py for checking if it's in stock again...
