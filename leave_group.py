from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import argparse
import pickle

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument("disable-gpu")
global driver
driver = webdriver.Chrome('chromedriver', options=chrome_options)

def login_page(url,email,password):
    try:
        driver.get(url)
        # get_login_email = driver.find_element_by_xpath("//input[@name='email']")
        get_login_email = driver.find_element(by=By.XPATH, value="//input[@name='email']")
        get_login_email.send_keys(email)
        time.sleep(2)
        # get_login_pass = driver.find_element_by_xpath("//input[@name='pass']")
        get_login_pass = driver.find_element(by=By.XPATH, value="//input[@name='pass']")
        get_login_pass.send_keys(password)
        time.sleep(2)
        # get_login_btn = driver.find_element_by_xpath("//input[@name='input']")
        get_login_btn = driver.find_element(by=By.XPATH, value="//input[@value='Log In']")
        get_login_btn.click()

        get_cookies = driver.get_cookies() 
        pickle.dump( get_cookies , open("cookiesFB.pkl","wb"))

        return get_cookies
    except Exception as e:
        print(e)
        return False

def get_group_link(url,cookies):
    driver.get(url)

    for cookie in cookies:
        driver.add_cookie(cookie)

    time.sleep(5)
    driver.get(url + "/groups/?seemore")

    store_link = []
    targeted_group = [lgroup.strip().lower() for lgroup in open('targeted_group.txt', 'r')]
    try:
        list_groups = driver.find_elements(by=By.XPATH, value="//div[2]/h3[text()='Groups You Are In']/following-sibling::ul/li")
        for llink in range(len(list_groups)):
            group_elem = driver.find_element(by=By.XPATH, value=f"//li[{llink+1}]//tr/td/a")
            group_link = group_elem.get_attribute('href')
            group_name = group_elem.text
            if group_name.lower() in targeted_group:
                store_link.append(group_link)
    except:
        store_link = 0
    return store_link

def do_leave_group(link):
    driver.get(link) # go to page

    get_group_name = driver.find_element(By.XPATH, value="//header/table//table//h1/div").text

    get_group_id = driver.find_element(By.XPATH, value="//h3[text()='Group Menu']/following-sibling::ul/li[2]//a[text()='Info']") # get group id by pointing to 'info' a element
    get_group_id = get_group_id.get_attribute('href')
    get_group_id = get_group_id.split('/')[-1].split('?')[0]

    # return get_group_id
    time.sleep(3)
    driver.get(f"https://mbasic.facebook.com/group/leave/?group_id={get_group_id}")
    time.sleep(3)

    try:
        driver.find_element(By.XPATH, value="//input[@value='Leave Group']").click()

        return get_group_name
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":

    main_url = "https://mbasic.facebook.com"

    parser = argparse.ArgumentParser(description="Facebook Leave Group (for lazy person)")
    parser.add_argument('--email', dest='email', type=str, required=True)
    parser.add_argument('--pwd', dest='pwd', type=str, required=True)

    args = parser.parse_args()

    email = args.email
    password = args.pwd

    try:
        login = pickle.load(open("cookiesFB.pkl", "rb"))
        print("Using Cookies")
    except:
        print("login session started")
        login = login_page(main_url,email,password)        
    
    if len(login) > 0:
        print("now getting group url")
        grouplinks = get_group_link(main_url, login)
        print(grouplinks)

        if len(grouplinks) > 0:
            print("\n")
            print("leaving group")
            for link in grouplinks:
                do_leave = do_leave_group(link)
                if do_leave:
                    print(f"You have successfully left from {do_leave} Group")
        else:
            print("group not found")

    driver.close()