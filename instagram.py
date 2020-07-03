from selenium import webdriver                           # selenium
from instagramInfo import email, password                # instagram username=email password=password from instagramInfo.py
import time                                              # time
from selenium.webdriver.common.keys import Keys          # input from keyboards


# instagram class input < username(email), password
# > output followers and follows list. "follows.txt","followers.txt"
class Instagram():
    def __init__(self,email,password):     # inputs
        self.browser = webdriver.Chrome()
        self.email = email
        self.password = password

    def signIn(self):                      # signing In 
        self.browser.get("https://www.instagram.com/accounts/login/")  # login screen url
        time.sleep(3)                                                  # should wait before doing sth because page must load

        # selecting username and password field. using xpath 
        emailInput = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
        passwordInput = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')

        # sending username and password from here
        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        time.sleep(2)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(3)
        # theese 2 click is for pop up windows. maybe dont need just refresh page. maybe* can solve that
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(3)
        self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        time.sleep(2)
        
    
    def getFollowers(self):                                          # Getting followers list and write to file "followers.txt"
        self.browser.get(f"https://www.instagram.com/{self.email}")  # profile url
        time.sleep(2)                                                # w8 for loading page
        # selecting followers link
        followersLink = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        followersLink.click()
        time.sleep(2)

        followersList = self.browser.find_element_by_css_selector("div[role=dialog] ul") # selecting followers list 
        followerCount=len(followersList.find_elements_by_css_selector("li"))             # calc first followers count

        action=webdriver.ActionChains(self.browser)  # need for scrolling

        while True:                                  # scrolling and writing to file followers list
            followersList.click()                                       # selecting page of followers (nf scrolling)
            # theese 4 line for scrolling pressing space key. Normally dont need to write 2 times but. i try and wdn't work so i wrote.
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)

            newCount = len(followersList.find_elements_by_css_selector("li")) # new followers count after scrolling
            if followerCount != newCount: # this if statement need for keep scrolling to last followers
                followerCount=newCount    # after 1 scroll need to be fix firstcount of followers
                time.sleep(1)
            else:
                break                     # when first followers count and new count is same quit this if statement

        followers = followersList.find_elements_by_css_selector("li") # selecting all followers list

        followerListesi = [] # string list

        for follower in followers:
            # "https://******.com/" 26 char we dont need these.  "followersname/" strip "/" = "followersname"          
            link = follower.find_element_by_css_selector("a").get_attribute("href")[26:].strip("/")             
            followerListesi.append(link)   # append followers name to string list           
        

        with open("followers.txt", "w",encoding="UTF-8") as file:
            for item in followerListesi:
                file.write(item + "\n")

    
    def getFollows(self):
        time.sleep(2)
        self.browser.get(f"https://www.instagram.com/{self.email}")
        time.sleep(2)
        followsLink = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
        followsLink.click()
        time.sleep(2)

        followsList = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followCount=len(followsList.find_elements_by_css_selector("li"))

        action=webdriver.ActionChains(self.browser)

        while True:
            followsList.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)
            newCount = len(followsList.find_elements_by_css_selector("li"))
            if followCount != newCount:
                followCount = newCount
                time.sleep(1)
            else:
                break          
        follows = followsList.find_elements_by_css_selector("li")

        followListesi = []

        for follow in follows:
            link = follow.find_element_by_css_selector("a").get_attribute("href")[26:].strip("/")            
            followListesi.append(link)            
        

        with open("follows.txt", "w",encoding="UTF-8") as file:
            for item in followListesi:
                file.write(item + "\n")



tagram = Instagram(email,password)
tagram.signIn()
tagram.getFollowers()
tagram.getFollows()