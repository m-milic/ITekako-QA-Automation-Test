import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
from datetime import datetime
import datetime
import random
import time


class FormaPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _link = "//a[@href = '/reserve']"
    _organizer = "//input[@placeholder = 'Who is organizing birthday']"
    _celebrant = "//input[@placeholder = 'Who is having birthday']"
    _age = "age"  # ID
    _date = "date"  # ID
    _time = "time"  # ID
    _people = "persons"  # ID
    _people_options = ["//option[@value='1']", "//option[@value='2']", "//option[@value='3']", "//option[@value='4']"]
    _finish = "//a[@href = '#ex1']"
    _allergies_active = "//div[@class = 'form-group grid-container']"

    # Storage
    alergies_options = {"y": "Yes", "n": "No", "m": "Maybe"}
    alergies_buttons = {"w": "alg1", "c": "alg2", "f": "alg3", "m": "alg4", "s": "alg5", "g": "alg6"}
    alergies_ls = {"w": "Wallnuts", "c": "Chestnuts", "f": "Fish", "m": "Meat", "s": "Shrimp", "g": "Gluten"}
    conf_expected = {"cbr": "", "orr": "", "agr": "", "dtr": "", "tmr": "", "gur": "", "alr": ""}
    no_of_ppl = ["2-5", "6-10", "11-20", "21+"]
    now = datetime.datetime.now()
    ls_expected = dict()

    def openPage(self):
        """
        Opens the Problem 1 page by clicking on a header link from the homepage
        """
        r = self.elementClick(self._link)
        return r

    def enterOrganizer(self, name = "Milos Milic"):
        """
        Enters 'name' str into the Organizer field.
        Sends Enter key after, so the text is saved to websites' local storage.
        Also inputs it into internal expected Local Storage, and expected Confirmation Window dictionaries,
        for later comparison/checking.
        """
        a = self.getElement(self._organizer)
        r = bool(a)
        r = r and bool(self.sendKeys(name, element=a))
        r = r and bool(self.sendEnter(element=a))
        self.ls_expected["Organizer"] = name
        self.conf_expected["orr"] = name
        return r

    def enterCelebrant(self, name = "Milic Milos"):
        """
        Enters 'name' str into the Birthday Person field.
        Sends Enter key after, so the text is saved to websites' local storage.
        Also inputs it into internal expected Local Storage, and expected Confirmation Window dictionaries,
        for later comparison/checking.
        """
        a = self.getElement(self._celebrant)
        r = bool(a)
        r = r and bool(self.sendKeys(name, element=a))
        r = r and bool(self.sendEnter(element=a))
        self.ls_expected["Birthday_Person"] = name
        self.conf_expected["cbr"] = name
        return r

    def enterAge(self, age = "32"):
        """
        Enters 'age' str into the Age of Birthday Person field.
        Sends Enter key after, so the text is saved to websites' local storage.
        Also inputs it into internal expected Local Storage, and expected Confirmation Window dictionaries,
        for later comparison/checking.
        """
        a = self.getElement(self._age, locatorType= 'ID')
        r = bool(a)
        r = r and bool(self.sendKeys(age, element=a))
        r = r and bool(self.sendEnter(element=a))
        self.ls_expected["Age"] = age
        self.conf_expected["agr"] = age
        return r

    def enterDate(self, d=""):
        """
        Enters 'd' str into the When field.
        Also inputs it into internal expected Local Storage, and expected Confirmation Window dictionaries,
        for later comparison/checking.
        Because element doesn't accept sending keys, instead the element is clicked first,
        and keys are 'sent' to no specific element, using action_chains.
        """
        if not d:
            d = self.now
        else:
            d = datetime.date(int(d[0:3]), int(d[4:5]), int(d[6:7]))
        dateLS = d.strftime("%Y-%m-%d")
        dateSend = d.strftime("%m%d%Y")
        a = self.getElement(self._date, locatorType='ID')
        r = bool(a)
        r = r and bool(self.elementClick(element=a))
        r = r and bool(self.typeKeys(dateSend))
        self.ls_expected["Date"] = dateLS
        self.conf_expected["dtr"] = dateLS
        return r

    def enterTime(self, t=""):
        """
        Enters 't' str into the At What Time field.
        Also inputs it into internal expected Local Storage, and expected Confirmation Window dictionaries,
        for later comparison/checking.
        Because element doesn't accept sending keys, instead the element is clicked first,
        and keys are 'sent' to no specific element, using action_chains.
        Time is being sent in two parts - numbers and AM PM separately, because Chrome didn't want to do it if at once.
        """
        if not t:
            t = self.now
        else:
            t = datetime.date(int(t[0:1]), int(t[2:3]))
        timeLS = t.strftime("%H:%M")
        timeSend1 = t.strftime("%I:%M")
        timeSend2 = t.strftime("%p")
        a = self.getElement(self._time, locatorType= 'ID')
        r = bool(a)
        r = r and bool(self.elementClick(element = a))
        r = r and bool(self.typeKeys(timeSend1))
        r = r and bool(self.typeKeys(timeSend2))
        self.ls_expected["Time"] = timeLS
        self.conf_expected["tmr"] = timeLS
        return r

    def selectPeople(self, option=2):
        """
        Selects 'option' in How many people will attend field, by clicking on it, and then on item from dropdown.
        Also inputs selected data into internal expected Local Storage, and expected Confirmation Window dictionaries,
        for later comparison/checking.
        """
        o = option-1
        r = bool(self.elementClick(self._people, locatorType= 'ID'))
        r = r and bool(self.elementClick(self._people_options[o]))
        value = self.no_of_ppl[o]
        self.ls_expected["Number_Of_People"] = value
        self.conf_expected["gur"] = value
        return r

    def selectIfAlergies(self, answer = "y"):
        """
        Selects one of 3 options in Do You Have any Alergies section, by clicking on it.
        Also inputs selected data into internal expected Local Storage, and expected Confirmation Window dictionaries,
        for later comparison/checking.
        """
        locator = "alg_" + answer
        r = self.elementClick(locator, locatorType='ID')
        self.ls_expected["alergy"] = self.alergies_options[answer]
        self.conf_expected["alr"] = self.alergies_options[answer]
        return r

    def checkAllergiesActive(self):
        """
        Checks is checkbox fields in the Which section are active (and alergies can be input).
        Does this by checking if section with classname exists, since classname changes when its active/deactivated.
        """
        a = self.isElementPresent(self._allergies_active)
        return a

    def checkAlergy(self, altype = "w"):
        """
        Checks the selected alergy checkbox, by clicking on it.
        Default is Wallnuts, other can be input when calling the function, using their first letter.
        Also inputs selected data into internal expected Local Storage, and expected Confirmation Window dictionaries,
        for later comparison/checking.
        """
        altype = altype.lower()
        el = self.getElement(self.alergies_buttons[altype], locatorType="ID")
        r = bool(el)
        r = r and bool(self.elementClick(element = el))
        tx = self.alergies_ls[altype]
        if "alergies" not in self.ls_expected:
            self.ls_expected["alergies"] = tx
        else:
            self.ls_expected["alergies"] += ("," + tx)
        return r

    def checkAlergies(self, n=0):
        """
        Checks 'n' random Alergies in the Which section.
        If no number is input, then checks random of 1 to 6 random alergies.
        If Alergies are not active, returns info message.
        """
        r = self.checkAllergiesActive()
        if r:
            if not n:
                n = random.randint(1, 6)
            a = random.sample(sorted(self.alergies_buttons), n)
            for i in a:
                r = r and self.checkAlergy(i)
        else:
            self.log.warning("Cannot select any alergies, since No is checked in the alergies question!")
            r = False
        return r

    def clickFinish(self):
        """
        Scrolls down and clicks Finish button.
        """
        self.webScroll()
        r = bool(self.elementClick(self._finish))
        return r

    def enterAllFields(self):
        r = self.selectIfAlergies()
        r = r and self.enterOrganizer()
        r = r and self.enterCelebrant()
        r = r and self.enterAge()
        r = r and self.enterDate()
        r = r and self.enterTime()
        r = r and self.selectPeople()
        r = r and self.checkAlergies()
        return r

    def checkLocalStorage(self):
        """
        Fetches local storage of the webpage, and compares it to the expected local storage.
        Does this by checking if all the key:value pairs existing in expected LS, are present in the websites' LS.
        (cannot simply compare dictionaries, cause getlocalstorage returns LS functions in the dictionary as well)
        For any element that does not match, logs its expected name and value.
        Finally, if there were elements not matching, displays how many incorrect entries were there.
        """
        c = 0
        b = self.getLocalStorage()
        a = self.ls_expected
        for i in a:
            if a[i] == b[i]:
                continue
            self.log.info(i + ":" + a[i] + " is not in the Local Storage!")
            c += 1
        if c:
            self.log.info("Local storage is not as expected. There are: "+str(c)+" incorrect entries")
        else:
            self.log.info("Local storage is as expected")
        return not bool(c)

    def checkConfirmation(self):
        """
        Compares expected confirmation window data, to the displayed conf. window data.
        Does this by checking value text of each row in the Conf Window, and comparing it to expected Conf Window data.
        For any element that does not match, logs its expected name and value.
        Finally, if there were elements not matching, displays how many incorrect entries were there.
        (since conf. window always displays all rows and in same order, regardless of if data were entered,
        function assumes they are same order and checks them by index, not by title)
        /// Confirmation window doesn't display selected alergies, so these are not checked. ///
        """
        x = ["Celebrant", "Organizer", "Age", "Date", "Time", "Guests", "Alergies"]
        c, j = 0, 0
        ce = self.conf_expected
        for i in ce:
            a = ce[i]
            b = self.getText(i, locatorType="ID", info=str(a))
            if not a == b:
                c += 1
                self.log.info("Incorrect confirmation data for " + x[j] + " is: " + str(b) + " , instead of " + a)
            j += 1
        if c:
            self.log.info("Confirmation window is not correct. There are: " + str(c) + " incorrect entries")
        else:
            self.log.info("Confirmation window is as expected")
        return not bool(c)
