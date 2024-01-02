# HITCH - A Ridesharing Community

Find it on GitHub: <a href="https://github.com/A-Hoenig/Hitch">HITCH</a>

<img src="./assets/images/screenshot-0.png" alt="Hitch" width="400"/>

## CONTENTS

<!-- TABLE OF CONTENTS -->

  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#user-stories">User Stories</a></li>
    <li><a href="#design">Design</a></li>
    <li><a href="#technologies-used">Technologies</a></li>
    <li><a href="#evaluation-and-assessment">Project Evaluation</a></li>
    <li><a href="#repository">Deployment</a></li>
    <li><a href="#future-development">Future Development</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>

### Built With
* [https://www.gitpod.io/](GitPod)

![GitHub last commit](https://img.shields.io/github/last-commit/A-Hoenig/WordDash?color=red&style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/A-Hoenig/WordDash?color=orange&style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/A-Hoenig/WordDash?color=yellow&style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/A-Hoenig/WordDash?color=green&style=for-the-badge)


<!-- ABOUT THE PROJECT -->
## About The Project






## Data Models / Database Design



## Design

### The Rides Page



## Future Development

* option 1
* option 2

## Technologies Used

#### Languages:

PYTHON FOR MAIN APP. HTML, CSS for mock CLI in HEROKU.

* [EDrawMax](https://www.edrawsoft.com/ad/edrawmax-diagram-tool.html?gad_source=1&gclid=CjwKCAiAjfyqBhAsEiwA-UdzJP7WWEuJcqaBE2Vag1b0U3ukJ_MwizjN76YlORg6EU2jBAXaFfTgxxoC2vAQAvD_BwE) - Used to create flowcharts.

* [Git](https://git-scm.com/) - For version control.

* [Github](https://github.com/) - To save and store the files for the website.

* [GitPod](https://gitpod.io/) - IDE used to create the site.

* [Heroku](https://www.heroku.com) - Hosts a mock CLI to run python app

#### Python Libraries:
| Library        | Needed For |
| :-------------- | :------ |
|gspread|google sheet manipulation|
|from google.oauth2.service_account import Credentials|authenticate google sheets|
|html|decode special characters from trivia site|
|requests|used for trivia API query|
|json|used to parse the recieved dictionary|
|os|needed to be able to clear CLI|
|random|needed to randomize questions answers|
|time|used to pause app long enough for user to read feedback|
|getpass|allow password entry without showing input text|
|from pyfiglet import Figlet|ASCII font art generator|
|from datetime import date|format date string for google sheet data|

<p align="right">(<a href="#contents">back to top</a>)</p>

<!-- GETTING STARTED -->
## Running the app

The finished app is hosted with HEROKU here:
<br>
<a href="https://MEGA-QUIZ-c93f32d70f60.herokuapp.com/">MEGA-QUIZ</a>
<br/>

For full app functionality, a google sheet needs to be set up with API credentials as well.
A step by step guide on how to do this can be referenced [Here (README_googleAPI)](README_googleAPI.md)

once the google sheet is created,

1. Fork or clone the repository and enter your IDE
2. add the creds.json file to the root directory
2. In the terminal / command line type: **python3 run.py** to run the app on your IDE

## Repository

###  **Deploying to Heroku**

1. Go to [Heroku](https://id.heroku.com/login), create account if you don't have and log in.

2. Head to your dashboard and click "New", then "Create new app"

    <details>
    <summary>New / Create New App</summary>
              
    ![New/CreateNewApp](/assets/images/deployment/step1-create-new-app.png)  

    </details>

3. Next step is to give your app a name and to choose region. After that click on "Create app".

    <details>
    <summary>Name / Region / Create</summary>
              
    ![Name/Region/Create](/assets/images/deployment/step2.png)  

    </details>

4. After that head to "Settings" tab which you can find on top of your Heroku page and under the "Config Vars" set your Key/Value Pairs.

    <details>
    <summary>CREDS / PORT</summary>
              
    ![CREDS/PORT](/assets/images/deployment/step3.png)  

    </details>

    First Key = **CREDS**. Value: Paste content of **creds.json** file  
    Second Key = **PORT**. Value: **8000**

5. Then in the "Buildpacks" section you will need to add buildpacks. Pay attention to the order in which you add buildpacks you need. In my case I had to add Python first and nodejs second.

    <details>
    <summary>Buildpacks</summary>
              
    ![Buildpacks](/assets/images/deployment/step4.png)  

    </details>

6. First add "Python", by clicking on Python icon and then click on "Add Buildpack".

    <details>
    <summary>Python</summary>
              
    ![Python](/assets/images/deployment/step5-python.png)  

    </details>

7. Then add "nodejs", by clicking on nodejs icon and then click on "Add Buildpack".

    <details>
    <summary>nodejs</summary>
              
    ![nodejs](/assets/images/deployment/step6-nodejs.png)  

    </details>

8. Then head to "Deployment" tab which you can also find on top of your Heroku page and under "Deployment method" click on "GitHub"(in my case that's where my repository is).

    <details>
    <summary>GitHub</summary>
              
    ![GitHub](/assets/images/deployment/step7-github.png)  

    </details>

9. After that, just under the "Deployment method" section is "Connect to GitHub" section where you need to find your repository and then click on "Connect".

    <details>
    <summary>Connect</summary>
              
    ![Connect](/assets/images/deployment/step8.png)  

    </details>

10. Just under "Connect to GitHub" section is "Automatic deploys" section where you can click on "Enable Automatic Deploys" if that's what you want and just under is "Manual Deploy" section, where you need to click on "Deploy Manually".

    <details>
    <summary>Enable Automatic Deploys / Deploy Manually</summary>
              
    ![EnableAutomaticDeploys/DeployManually](/assets/images/deployment/step9-deployment-type.png)  

    </details>

### Local Development

#### How to Fork

To fork the repository:

1. Log in (or sign up) to Github.
2. Go to the repository for this project, [A-Hoenig/megaquiz](https://github.com/A-Hoenig/megaquiz)
3. Click the Fork button in the top right corner.
4. Drag and drop the CREDS.json file into the root directory
5. Make sure to add CREDS.json to the .gitignore file to prevent the secure key being commited to github
6. To run the quiz type: **python3 run.py** in the command line / terminal

#### How to Clone

To clone the repository:

1. Log in (or sign up) to GitHub.
2. Go to the repository for this project, [A-Hoenig/megaquiz](https://github.com/A-Hoenig/megaquiz)
3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.
4. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.
5. Type 'git clone' into the terminal and then paste the link you copied in step 3. Press enter.
6. Ensure the CREDS.json file is uploaded and ignored as mentioned above.

<p align="right">(<a href="#contents">back to top</a>)</p>

## Testing

### Validator Testing

#### PYTHON
  - No errors were returned when passing through the official [CI pep8 Linter](https://pep8ci.herokuapp.com/)
<img src="./assets/images/linter-result.png" alt="Linter" width="700"/>

## Manual Testing

### 1. GENERAL TESTS / LOGIC
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
|App starts after run.py|Enter command in CLI|Verified OK|


### 2. MENU TESTS
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
|Main Menu displays correct in CLI|start app|Verified OK|


### 3. LOGIN / USER ACCOUNT TESTS
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
|User can log in|input dummy user and pw|Verified OK|
|Password entry is checked|typed correct and wrong pw|Verified OK|
|Wrong password x3 = back to menu|type 3 wrong pw|Verified OK|
|Password blank entry rejected|Type enter without text|Verified OK|
|User recognized|logged in correectly|Verified OK|
|Username validation rejects special characters|input @$_ etc|Verified OK|
|Unreconized User triggers 'create new'|typed a new username|Verified OK|
|New user can enter password|new user name + password input|Verified OK|
|New password is checked matching|typed wrong and correct repeat pw|Verified OK|
|Feedback given to user|typed all options|Verified OK|
|User can create a new profile|select 8 and chose user+PW|Verified OK|
|New user name checked available|input known and unknown name|Verified OK|

### 4. API TESTS
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
||||
||||


### 5. OTHER TESTS
| Feature/Story       | Action | Result |
| :-------------- |:------ | :------ |
||||
||||


### Browser Compatibility

The deployed app on heroku was tested on most popular browsers for functionality:
* Chrome
* Safari - CI CLI app does not accept keyboard input on macOS/iOS Safari and iOS Chrome!
* Edge
* Opera

### Known Bugs



## Credits

### External Help

* Google / Stackoverflow
* Thanks to https://github.com/AleksandarJavorovic for sharing the instructions on how best to deploy the app on Heroku.

## License

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png) 
<br>
This project is license free and part of Code Institute Full Stack Developer Course.
It is for educational use only.

<!-- CONTACT -->
## Contact

Alex Hönig -  LimeyDeveloper@pm.me

Project Link: [MEGA-QUIZ](https://github.com/A-Hoenig/megaquiz)

## Acknowledgments

I would like to acknowledge the following people:

* Jubril Akolade - My Code Institute Mentor for the guidance.


<p align="right">(<a href="#contents">back to top</a>)</p>