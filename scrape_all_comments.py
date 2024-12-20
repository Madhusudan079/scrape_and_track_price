import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pickle
from selenium.webdriver.common.action_chains import ActionChains


def save_cookies(driver, filepath):
    with open(filepath, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)


def load_cookies(driver, filepath):
    try:
        with open(filepath, 'rb') as file:
            cookies = pickle.load(file)
            # print(cookies)
            for cookie in cookies:
                driver.add_cookie(cookie)
        return True
    except FileNotFoundError:
        return False


def upload_video_to_facebook(username, password):
    driver = webdriver.Chrome()  # Replace with the correct path to your chromedriver
    cookie_path = "instagram_cookiesss.pkl"

    driver.get("https://www.instagram.com/")  # Replace with Facebook URL if needed
    time.sleep(5)

    login_with_facebook = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[5]/button')
    login_with_facebook.click()
    time.sleep(10)

    try:
        load_cookies(driver, cookie_path)
        driver.refresh()
        time.sleep(5)

        login = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div")
        login.click()
        time.sleep(5)

        search_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div[2]/span/div/a/div")
        search_button.click()
        time.sleep(3)

        search = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/input")
        search.send_keys("rahulsharmaofficial62")
        time.sleep(3)
        action = ActionChains(driver)
        action.send_keys(Keys.ARROW_DOWN).send_keys(Keys.RETURN).perform()
        time.sleep(5)

        # driver.execute_script('window.scrollBy(0, 600);')
        # time.sleep(5)

        click_specific_post = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div/div[1]/div[3]")
        click_specific_post.click()
        time.sleep(3)

        # Initialize a variable to store already loaded comments
        loaded_comments = set()

        comments_elements = driver.find_elements(By.XPATH, "//article//ul//li//span[contains(@class, '_ap3a')]")

        # Filter new comments and avoid duplicates
        for comment_element in comments_elements:
            comment_text = comment_element.text
            if comment_text.lower() not in loaded_comments and "pandit" in comment_text.lower():
                loaded_comments.add(comment_text)
                print(comment_text)

        # Loop to keep scrolling and clicking "Load more comments" button
        while True:
            try:
                # Scroll using END key multiple times to bring the button into view
                for _ in range(8):
                    action.send_keys(Keys.END).perform()
                    time.sleep(1)

                # Find and click "Load more comments" button if it exists
                load_more_button = driver.find_element(By.XPATH, "//article//ul//li//div[contains(@class, '_abm0')]")
                load_more_button.click()
                print("Clicked 'Load more comments' button.")
                time.sleep(2)  # Wait for new comments to load

            except Exception:
                # Break the loop if no "Load more comments" button is found
                print("No more 'Load more comments' button found.")
                break

            # Collect all visible comments
            comments_elementsss = driver.find_elements(By.XPATH, "//article//ul//li//span[contains(@class, '_ap3a')]")

            # Filter new comments and avoid duplicates
            for comment_element in set(comments_elementsss):
                comment_text = comment_element.text
                if comment_text.lower() not in loaded_comments and "pandit" in comment_text.lower():
                    loaded_comments.add(comment_text)
                    print(comment_text)

        print("Finished loading all comments.")
        print(f"Total unique comments containing 'pandit': {len(loaded_comments)}")

    except FileNotFoundError:
        username_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "pass")
        username_input.send_keys(username)
        time.sleep(2)
        password_input.send_keys(password)
        time.sleep(2)
        password_input.send_keys(Keys.RETURN)
        time.sleep(10)

        save_cookies(driver, cookie_path)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()


facebook_username = ''
facebook_password = ''

upload_video_to_facebook(facebook_username, facebook_password)
