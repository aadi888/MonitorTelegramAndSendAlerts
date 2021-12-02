# MonitorTelegramAndSendAlerts
This script is designed to monitor any telegram group and send alerts to phone number via msgs . This script reads
messages as per threshold and after that reloads page for new messages and again same process.

Pre Requisites : 
1. Install chromedriver
2. Twilio create free trial account- which will give you $15 equivalent to 1500 free text alerts 
   (if reached limit create another free trial account) 
   (follow more info here https://www.geeksforgeeks.org/python-send-sms-using-twilio/)
   (Twilio alternative : you can also implement client logic to use google voice api, update client and send_msg logic to achieve this)
3. pip install -U selenium
4. pip install twilio

Run the script via  python monitorTelegramGroup.py (script will run forever - on Mac I was able to let this script
run in sleep mode not sure about windows)

NOTE : Script requires first time manual barcode QR code scan from your mobile app - go to browser and type url
chrome://inspect and hit inspect to finish barcode signing process. Once sign in process is completed exit debug panel as headless mode sometimes changes UI elements and script breaks .
