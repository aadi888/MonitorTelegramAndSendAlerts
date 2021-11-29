# MonitorTelegramAndSendAlerts
This script is designed to monitor any telegram group and send alerts to phone number via msgs . This script reads
messages as per threshold and after that reloads page for new messages and again same process.

Pre Requisites : 
1. Install chromedriver and change path in input params below 
2. Twilio create free trial account- which will give you $15 equivalent to 1500 free text alerts (if reached limit create another free trial account)
   Pass account_sid, auth_token and phone numbers below (follow more info here https://www.geeksforgeeks.org/python-send-sms-using-twilio/)
3. Enter partial keyword/name of the group you want to monitor below

Run the script via  python monitorTelegramGroup.py (script will run forever - on Mac I was able to let this script
run in sleep mode not sure about windows)

NOTE : Script requires first time manual barcode QR code scan from your mobile app - go to browser and type url
chrome://inspect and hit inspect to finish barcode signing process. Once sign in process is completed exit debug panel as headless mode sometimes changes UI elements and script breaks .
