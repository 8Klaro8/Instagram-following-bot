# imports ----------------------------------------------------------------------
import random
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import undetected_chromedriver as uc
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller


# Basic datas----------------------------------------------------------
DRIVER_PATH = r'DRIVER_PATH'
LINK = 'https://www.instagram.com/'
RANDOM_NUM = random.randrange(1,2)
EMAIL = 'MYEMAIL'
PASSWORD ='MYPASSWORD'
Fb_Password = 'MY_FB_PASS'
Fb_email = 'MY_FB_EMAIL'



# creating Bot class
class InstaBot:
    def __init__(self):
        self.opions = uc.ChromeOptions()
        self.opions.add_argument('--disable-save-password-bubble')
        self.driver = uc.Chrome(options=self.opions)
        self.action = ActionChains(self.driver)
        # free_proxies = self.get_free_proxies()
        # print(free_proxies)

    # Get procies if necessary for login - currently unused
    def get_free_proxies(self):
        self.driver.get('https://sslproxies.org')

        table = self.driver.find_element(By.TAG_NAME, 'table')
        thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
        tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

        headers = []
        for th in thead:
            headers.append(th.text.strip())

        proxies = []
        for tr in tbody:
            proxy_data = {}
            tds = tr.find_elements(By.TAG_NAME, 'td')
            for i in range(len(headers)):
                proxy_data[headers[i]] = tds[i].text.strip()
            proxies.append(proxy_data)

        return proxies

# logging in by facebook
    def facebook_log_in(self):
        self.driver.get(LINK)
        self.wait()
        try:
            cookies_buttons = self.driver.find_elements(By.TAG_NAME, value='button')
            for button in cookies_buttons:
                if 'Only' in button.text:
                    button.click()
        except:
            pass
        self.wait()
        self.wait()

        #login with facebook------------------------------
        login_button_options = self.driver.find_elements(By.TAG_NAME, value='button')
        for each in login_button_options:
            # search button based on its text
            if each.text == 'Log in with Facebook':
                each.click()

        facebook_cookie_button = self.driver.find_elements(By.TAG_NAME, value='button')
        for each in facebook_cookie_button:
            # click on cookies
            if each.text == 'Only Allow Essential Cookies':
                each.click()
        self.wait()
        email_input_facebook = self.driver.find_elements(By.TAG_NAME, value='input')
        # finds and gets input fields for login credentials
        for je in email_input_facebook:
            if je.get_attribute('placeholder') == 'Email address or phone number':
                self.action.move_to_element(je).click(je).send_keys(Fb_email).perform()
            elif je.get_attribute('placeholder') == 'Password':
                self.action.move_to_element(je).click(je).send_keys(Fb_Password).perform()
        self.wait()
        fb_login_button_options = self.driver.find_elements(By.TAG_NAME, value='button')
        for ev in fb_login_button_options:
            if ev.get_attribute('type') == 'submit':
                ev.click()
                self.wait()
                try:
                    login_link = self.driver.find_element(By.CLASS_NAME, value='loginLink')
                    self.wait()
                    login_link.click()
                    self.email_login()
                except:
                    reject_notification = self.driver.find_element(By.XPATH,
                                                                   value='/html/body/div[5]/div/div/div/div[3]/butt'
                                                                         'on[2]').click()
                    print('logged in')


    def email_login(self):
        # login with email------------------------------
        self.wait()
        try:
            login_inputs = self.driver.find_elements(By.TAG_NAME, value='input')
            self.wait()
            for inp in login_inputs:
                # goes up in the hierarchi to find the elemnt I need
                if 'Phone' in inp.find_element(By.XPATH, value='..').text:
                    self.action.move_to_element(inp).click(inp).send_keys(EMAIL).perform()
                    self.wait()
                else:
                    inp.send_keys(PASSWORD)
                    self.wait()
            self.wait()
            login_with_email_button = self.driver.find_element(By.XPATH, value='/html/body/div[1]/section/main/div/'
                                                                               'div/div[1]/div/form/div/div[3]/butt'
                                                                               'on').click()
        except:
            print('logged in already')
        self.wait()

    # currently used for unfollow, previously followed accounts
    def find_followers(self):
        # print if I am in the function or not
        print('before search')
        search_input_options = self.driver.find_elements(By.TAG_NAME, value='input')
        self.wait()
        # finding ipnut field by palceholder
        if 'Search' in search_input_options[0].get_attribute('placeholder').title():
            self.wait()
            print(search_input_options[0].get_attribute('placeholder').title())
            # TODO set preference easier to use - arg
            self.action.move_to_element(search_input_options[0]).click(search_input_options[0]).send_keys(
                'catloversclub').perform()
            self.wait()
            results = self.driver.find_elements(By.TAG_NAME, value='a')
            for each in results:
                # selects what we need based on the set preference
                if 'catlove' in each.text.split('\n')[0]:
                    each.click()
                    break
            self.wait()
            follwoers = self.driver.find_elements(By.TAG_NAME, value='a')
            for link in follwoers:
                if ' followers' in link.text:
                    link.click()
            self.wait()
            ul = self.driver.find_elements(By.TAG_NAME, value='ul')
            followers_list = ul[1]
            follower_buttons = followers_list.find_elements(By.TAG_NAME, value='button')
            last_button_element = ''
            for button in follower_buttons:
                if 'Following' or 'Requested' in button.text:
                    button.click()
                    self.wait()
                    unfollow_buttons = self.driver.find_elements(By.TAG_NAME, value='button')
                    # unfollows
                    for unf_button in unfollow_buttons:
                            unf_button[0].click()
                            self.wait()
                else:
                    button.click()
                    last_button_element = button
                    self.wait()
            # scrolls until the last interacted button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", last_button_element)
            print('all done')

    def get_to_followers(self):
        print('entered find followers_v2')
        #try turn off notification when logged in
        self.turn_off_notification_when_logged_in()
        #search for search input bar------------------------
        self.wait()
        search_bar = self.driver.find_elements(By.TAG_NAME, value='input')
        for input_options in search_bar:
            # finding appropriate input by placeholder
            if 'Search' in input_options.get_attribute('placeholder'):
                my_searchbar = input_options
                # TODO set it as an attribute to set preference easier
                my_searchbar.send_keys('catloversclub')
                self.wait()
                self.wait()
                catloversclub = self.driver.find_elements(By.CLASS_NAME, value='-qQT3')
                for each in catloversclub:
                    my_link = each.get_attribute('href')
                    print(my_link)
                    if 'catloversclub' in my_link:
                        each.click()
                        self.wait()
                        self.wait()
                        click_follow = self.driver.find_elements(By.TAG_NAME, value='a')
                        for every in click_follow:
                            self.wait()
                            follower_buttons = every.get_attribute('href')
                            # opens follwors tab to find accounts to follow
                            if 'followers' in follower_buttons:
                                every.click()
                                self.wait()
                                self.follow_found_results_v2()
                                # self.follow_found_results()
                                break
                        break

    # follow the results v2 - currently working function!
    def follow_found_results_v2(self):
        round = 0
        for i in range(4):
            round += 1
            follow_members = self.driver.find_element(By.CLASS_NAME, value='jSC57')
            follower_buttons = follow_members.find_elements(By.TAG_NAME, value='button')
            self.action.move_to_element(follower_buttons[-1]).perform()
            self.wait()
        print(len(follower_buttons))
        follow_members = self.driver.find_element(By.CLASS_NAME, value='jSC57')
        follower_buttons = follow_members.find_elements(By.TAG_NAME, value='button')
        self.follow(follower_buttons, round)

        self.wait()


        # False trial---------------------------------------------------------------------------------------

        # last_element = ''
        # for i in range(2):
        #     self.wait()
        #     follower_buttons = follow_members.find_elements(By.TAG_NAME, value='button')
        #     for each in follower_buttons:
        #         self.wait()
        #         if each.text == 'Requested' or each.text == 'Following':
        #             self.driver.execute_script("arguments[0].scrollIntoView();", each)
        #             self.wait()
        #             pass
        #         elif each.text == 'Follow':
        #             self.driver.execute_script("arguments[0].scrollIntoView();", each)
        #             each.click()
        #             self.wait()
        #     self.wait()
        #     print('done')


        # for i in range(2):
        #     for each in follower_buttons:
        #         if each.text == 'Requested' or each.text == 'Following':
        #             self.wait()
        #             pass
        #         elif each.text == 'Follow':
        #             each.click()
        #             self.wait()
        #     self.wait()
        #     last_element = follower_buttons[-1]
        #     self.action.move_to_element(last_element).click(last_element).perform()
        #     self.wait()


# follows the result - account(s)
    def follow(self, follower_buttons, round):
        followed = 0
        for each in follower_buttons:
            # checks if button of current account is already clicked
            if each.text == 'Requested' or each.text == 'Following':
                self.wait()
                continue
                # if it is not cliked the call click func
            elif each.text == 'Follow':
                each.click()
                followed += 1
                self.wait()
        print(f'total follwoed: {followed}')
        print(f'total round: {round}')

    # follows the given results - accounts - currnently inactive func - instead: follow_found_results_v2 - see above
    def follow_found_results(self):
        new_line = '\n'
        account_container = []
        double_counter = 0
        self.wait()
        self.wait()
        ul = self.driver.find_element(By.CLASS_NAME, value='jSC57')
        li_s = ul.find_elements(By.TAG_NAME, value='li')
        self.print_current_lis(li_s, new_line, account_container, double_counter)
        self.wait()
        for i in range(2):
            self.wait()
            last_li_element = li_s[-1]
            self.action.move_to_element(last_li_element).click(last_li_element).perform()
            self.wait()
            li_s = ul.find_elements(By.TAG_NAME, value='li')
            self.wait()
            self.print_current_lis(li_s, new_line, account_container, double_counter)
            self.wait()
        print(len(li_s))
        print(f'double counter: {double_counter}')

# checks if the currently visible account are "stored" or not
    def print_current_lis(self, li_s, new_line, account_container, double_counter):
        for each in li_s:
            if each.text.split(new_line)[0] in account_container:
                double_counter += 1
            elif each.text.split(new_line)[0] not in account_container:
                account_container.append(each.text.split(new_line)[0])
                print(each.text.split(new_line)[0])

# notification turn off when logged in
    def turn_off_notification_when_logged_in(self):
        try:
            buttons = self.driver.find_elements(By.TAG_NAME, value='button')
            for button in buttons:
                if 'Not Now' in button.text:
                    button.click()
                    print('notification turned off')
        except:
            print('there is no notification popup')
    def wait(self):
        time.sleep(RANDOM_NUM)
        self.driver.implicitly_wait(RANDOM_NUM)

# initialling process
if __name__ == '__main__':
    my_bot = InstaBot()
# tries to log in if with facebook
    try:
        my_bot.facebook_log_in()
    except:
        print('Already logged in (dont need to log in this time)')
    # my_bot.find_followers()
    my_bot.wait()
    my_bot.wait()

    # waits until page is loaded
    delay = 3  # seconds
    try:
        myElem = WebDriverWait(my_bot.driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'button')))
        my_bot.get_to_followers()
    except TimeoutException:
        print("Loading took too much time!")
    time.sleep(10000)

