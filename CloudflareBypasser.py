import time
from DrissionPage import ChromiumPage


class CloudflareBypasser:
    def __init__(self, driver: ChromiumPage, max_retries=-1, log=True):
        self.driver = driver
        self.max_retries = max_retries
        self.log = log

    def locate_cf_button(self):
        try:
            sr = self.driver.ele('.:h2 spacer-bottom')
            div1 = sr.next().children()[0]
            div2 = div1.children()[0]
            shadow = div2.shadow_root
            iframe = shadow.ele('t:iframe')
            body = iframe.ele("t:body")
            sr = body.shadow_root
            main_div = sr.child('.:main-wrapper')
            main_content = main_div.child('#content')
            main_grid = main_content.children()[0]
            time.sleep(5)
            cbc = main_grid.children()[0]
            cbl = cbc.children()[0]
            return cbl.children('t:input')[0]
        except:
            self.log_message('Error locating button')
            pass
        return None


    def log_message(self, message):
        if self.log:
            print(message)

    def click_verification_button(self):
        try:
            button = self.locate_cf_button()
            if button:
                self.log_message("Verification button found. Attempting to click.")
                button.click()
            else:
                self.log_message("Verification button not found.")

        except Exception as e:
            self.log_message(f"Error clicking verification button: {e}")

    def is_bypassed(self):
        try:
            title = self.driver.title.lower()
            return "just a moment" not in title
        except Exception as e:
            self.log_message(f"Error checking page title: {e}")
            return False

    def bypass(self):
        try_count = 0

        while not self.is_bypassed():
            if 0 < self.max_retries + 1 <= try_count:
                self.log_message("Exceeded maximum retries. Bypass failed.")
                break

            self.log_message(
                f"Attempt {try_count + 1}: Verification page detected. Trying to bypass..."
            )
            self.click_verification_button()

            try_count += 1
            time.sleep(2)

        if self.is_bypassed():
            self.log_message("Bypass successful.")
        else:
            self.log_message("Bypass failed.")
