import time

import utilities.custom_logger as cl
import logging
from base.basepage import BasePage

class PreporukaPage(BasePage):


    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators and storage

    _link = "//a[@href = '/questionaire']"
    _result = "recHeader"  # ID - text je rezultat
    _rmm = "readmymind"  # ID

    pozitivni = list("btn"+str(i) for i in range(1,18,2))       # List of ID locators for positive/left buttons
    negativni = list("btn"+str(i) for i in range(2,19,2))       # List of ID locators for negative/right buttons
    odabrani = list("resultText"+str(i) for i in range(1,10))   # List of CLASS locators for selected answers
    odgovori = ["Avocado Benedict", "Strawberry Sundae", "Soy Salmon", "Culiflower Dipper", "Blonde"]


    def openPage(self):
        """
        Opens the Problem 2 page by clicking on a header link from the homepage
        """
        r = self.elementClick(self._link)
        return r

    def clickPozitivni(self, l = 9):
        """
        Clicks on all positive/left answers
        """
        r = True
        for i in range(l):
            r = r and bool(self.elementClick(self.pozitivni[i], locatorType="ID"))
        return r

    def clickNegativni(self, l = 0):
        """
        Clicks on all negative/right answers
        """
        r = True
        for i in range(l, 9):
            r = r and bool(self.elementClick(self.negativni[i], locatorType="ID"))
        return r

    def clcikAndVerifyAll(self, b="pozitivni"):
        """
        Clicks on all answers of selected type, and verifies if text in selected answer field is correct.
        By default, clicks/checks positive, if selected when calling, then negative.
        """
        b = b.lower()
        c = self.pozitivni
        r = True
        if b == "negativni":
            c = self.negativni
        for i in range(9):
            el = self.getElement(c[i], locatorType="ID")
            r = r and bool(self.elementClick(element = el))
            sel = self.getText(element = el, info = ("Odabrani odgovor na pitanje " + str(i+1)))
            res = self.getText(self.odabrani[i], locatorType="CLASS",
                               info = ("Prikazani odgovor na pitanje " + str(i+1)))
            valid = sel == res
            r = r and bool(el) and bool(sel) and bool(res)
            self.log.info("Clicked: " + sel)
            self.log.info("Displayed: " + res)
            self.log.info("Left button on question " + str(i+1) + " is correct?" + str(valid))
        return r


    def clickRMM(self):
        """
        Clicks on Read My Mind button
        """
        r = bool(self.elementClick(self._rmm, locatorType="id"))
        return r

    def clearAll(self):
        """
        Clears all displayed answer fields.
        Since they are not saved in LS but HTML, this is done by clearing innerHTML of fields.
        """
        r = True
        for i in range(len(self.odabrani)):
            r = r and bool(self.clearInnerHtml(self.odabrani[i], locatorType="Class"))
        return r

    def getFinal(self):
        """
        Fetches the title of the displayed final result, and returns it
        """
        a = self.getText(self._result, locatorType="ID", info = "Rezultat")
        return a # and r

    def verifyFinal(self, answer):
        """
        Verifies if the title of the displayed final result is as expected.
        (by comparing it to itmes in list -odgovori-
        """
        r = answer == self.getFinal()
        return r

    def verifyAllOptions(self):
        """
        Runs a sequence of entering answers + activating RMM + verifying result, for all 5 different result options.
        Does this by selecting 0, 2, 4, 6, 8 left answers in first 0-8 questions, and right answers for the rest of Q.
        (since the method is as described, it does not actually check if 9th question left answer works as expected,
        but this can also be easily done if needed)
        """
        r = True
        for i in range(5):
            r = r and bool(self.resetCook())
            time.sleep(1)
            r = r and bool(self.clearAll())
            r = r and bool(self.clickPozitivni(i*2))
            r = r and bool(self.clickNegativni(i*2))
            r = r and bool(self.clickRMM())
            r = r and bool(self.verifyFinal(self.odgovori[i]))
            if r:
                self.log.warning("Option " + self.odgovori[i] + " is displayed, as expected!")
            else:
                self.log.warning("Option " + self.odgovori[i] + " was expected, but not displayed!")
        return r