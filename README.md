# ITekako-QA-Automation-Test
Base technologies used: Python 3.11 and Selenium 4.7.2

If not already, install Python 3.11 to machine.
Create directory for the project.
Create a git repository.
Pull project from git repository to project folder.
Update Chrome and Firefox on system to the latest stable version.

***If OS is not Windows 64, download Chrome driver and Geckodriver for the latest browser version for your OS.
***Put them to Drivers folder in the project folder.
***In project file /base/webdriverfactory.py, edit executable_path for Chrome and Firefox (line 20 and 23), so that extension is adequate

In terminal, navigate to the location of the project.
Create and activate virtual env. there.
Use pip to install all the packages from requirements.txt file

To run the tests, use code:
py.test -v /tests/forma_test.py --browser firefox
py.test -v /test/preporuka_test.py --browser firefox
py.test -v /test/meni_i_kolica_test.py --browser firefox
(to run on Chrome, just type chrome instead of firefox)
(to run individual tests from test run add -k "=testname="

automation.log file is created in root directory of the project after first test, and is expanded with each next.
Logs most of actions as Info, and results as Warning or Error.

To save log as HTML file, add --html=FILENAME.html
