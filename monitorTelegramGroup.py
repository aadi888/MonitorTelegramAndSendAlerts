# This script is designed to monitor any telegram group and send alerts to phone number via msgs . This script reads
# messages as per threshold and after that reloads page for new messages and again same process.

# Pre Requisites : 1. Install chromedriver and change path in input params below 2. Twilio create free trial account
# - which will give you $15 equivalent to 1500 free text alerts (if reached limit create another free trial account)
# - Pass account_sid, auth_token and phone numbers below (follow more info here
# https://www.geeksforgeeks.org/python-send-sms-using-twilio/)
# 3. Enter partial keyword/name of the group you want to monitor below

# Run the script via  python monitorTelegramGroup.py (script will run forever - on Mac I was able to let this script
# run in sleep mode not sure about windows)

# NOTE : Script requires first time manual barcode QR code scan from your mobile app - go to browser and type url
# chrome://inspect and hit inspect to finish barcode signing process. Once sign in process is completed exit debug
# panel as headless mode sometimes changes UI elements and script breaks .

# Define/Change your inputs and Twilio configurations below - provided params are example ones
chrome_driver_path = '/Users/Downloads/chromedriver'
account_sid = ''
auth_token = ''
send_msg_from = '+112334567890'
send_msg_to = '+1223332332'
group_partial_name_keyword = 'Dropbox'

# Script code
from selenium import webdriver
import time
from twilio.rest import Client
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--start-fullscreen")
chrome_options.add_argument("--enable-automation")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-browser-side-navigation")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)
driver.get("https://web.telegram.org/")
client = Client(account_sid, auth_token)

def exit():
    driver.quit()

#atexit.register(exit)

def send_msg(msg):
    message = client.messages \
        .create(
        body=msg,
        from_=send_msg_from,
        to=send_msg_to
    )

    print('#########')
    print(msg)
    print('#########')

def reload():
    try:
        print("############### reloading ... ###############")
        # driver.get(driver.current_url)
        # time.sleep(10)
        driver.refresh()
        #time.sleep(10)
        #print("clicking ...")
        wait2 = WebDriverWait(driver, 100)
        wait2.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'"+group_partial_name_keyword+"')]")))
        time.sleep(5)
        element = driver.find_element_by_xpath("//*[contains(text(), '"+group_partial_name_keyword+"')]//ancestor::div[contains(@class, 'chatlist-top') or contains(@class, 'ListItem-button')]//div[contains(@class, 'ripple-container') or contains(@class, 'c-ripple')]")
        #print(element)
        try:
            hover = ActionChains(driver).move_to_element(element)
            hover.click().perform()
        except:
            time.sleep(5)
            hover = ActionChains(driver).move_to_element(element)
            hover.click().perform()
            
        # touch_actions = TouchActions(driver)
        # touch_actions.tap(element).perform()
        # element.click()
        time.sleep(5)
        #print("############### reloading done ... ###############")
    except Exception, e:
        print("############### reloading FAILED , ignoring ###############" + str(e))
        pass

previous_msgs_count = 0
current_msgs_count = 0
is_bubbles = False
combine_msgs = 0
combine_msgs_list = []

wait = WebDriverWait(driver, 100)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'" + group_partial_name_keyword + "')]")))
time.sleep(10)
reload()
count_for_reload = 0
count_for_dead_loop = 0
threshold = 10
while True:
    time.sleep(5)
    if count_for_reload > threshold or count_for_dead_loop > threshold:
        reload()
        count_for_reload = 0
        count_for_dead_loop = 0

    try:
        driver.find_element_by_xpath("//button[@title='Go to bottom']").click()
        print("Clicked Go To successfully")
    except:
        pass

    try:
        current_msgs = driver.find_elements_by_class_name("Message")
        if len(current_msgs) == 0:
            is_bubbles = False
            current_msgs = driver.find_elements_by_class_name("bubble")
            if len(current_msgs) > 5:
                is_bubbles = True
        current_msgs_count = len(current_msgs)
        #print("additional check " + str(current_msgs_count))
    except:
        reload()
        continue

    if current_msgs_count != previous_msgs_count and previous_msgs_count != 0 and current_msgs_count > previous_msgs_count and (current_msgs_count - previous_msgs_count) < 15:
        difference = current_msgs_count - previous_msgs_count
        count_for_reload = count_for_reload + 1
        count_for_dead_loop = 0

        #print("*** New msgs found " + str(difference))
        difference_msgs = current_msgs[-difference:]

        for msg in difference_msgs:
            try:
                if is_bubbles:
                    msg_txt = msg.find_element_by_class_name("message").text.strip().replace("\n", " ")
                else:
                    msg_txt = msg.find_element_by_class_name("text-content").text.strip().replace("\n", " ")

                print(msg_txt)
                msg_txt_tupples = msg_txt.split("\n")[0].lower().split(" ")
                if len(msg_txt) < 9:
                    print("screenshot found")
                    send_msg('Alert Screenshot Found')
                    reload()
                    continue

                if 'na' not in msg_txt_tupples and 'awesomeadmin_us' not in msg_txt_tupples and 'ss' not in msg_txt_tupples and '@awesomeadmin_us' not in msg_txt_tupples and len(msg_txt) > 5:
                    combine_msgs_list.append(msg_txt)
                    combine_msgs = combine_msgs + 1

                    if combine_msgs == 5:
                        #send_msg(''.join(combine_msgs_list))
                        reload()
                        combine_msgs = 0
                        combine_msgs_list = []

                    try:
                        ss_found = msg.find_element_by_xpath("//img[@src][not(contains(@class, 'avatar'))]")
                        send_msg("Screenshot found : " + ss_found)
                        reload()
                    except:
                        pass
                if '/filter' in msg_txt or '/start' in msg_txt:
                    print("Found Filter - refreshing ....")
                    #reload()
            except:
                try:
                    print("In Except - probably attachment")
                    #ss_found = msg.find_element_by_xpath("//img[@src][not(contains(@class, 'avatar'))]")
                    #send_msg("Alert Screenshot found : ")
                    #reload()
                except:
                    pass
                pass
    else:
        count_for_dead_loop = count_for_dead_loop + 1

    previous_msgs_count = current_msgs_count
