from selenium import webdriver
import time

# Fonction pour ajouter les instructions à la page
def add_instructions(driver, instructions_text):
    instructions_script = """
    var instructionsDiv = document.createElement('div');
    instructionsDiv.style.backgroundColor = '#f5f5f5';
    instructionsDiv.style.color = 'black';
    instructionsDiv.style.padding = '10px';
    instructionsDiv.style.position = 'fixed';
    instructionsDiv.style.bottom = '0';
    instructionsDiv.style.left = '0';
    instructionsDiv.style.width = '100%';
    instructionsDiv.style.zIndex = '9999';
    instructionsDiv.innerHTML = arguments[0];
    document.body.insertBefore(instructionsDiv, document.body.firstChild);
    """
    driver.execute_script(instructions_script, instructions_text)

# Utiliser Chrome en mode non-headless pour débogage
driver = webdriver.Chrome()

# Ouvrir le portail des développeurs de Discord
driver.get('https://discord.com/developers/applications')

# Attendre quelques secondes pour laisser la page se charger
driver.implicitly_wait(10)

# Instructions génériques
login_instructions = """
<h3>Instructions:</h3>
<p>1. Log in with your Discord credentials.</p>
<p>2. Press the Log In button.</p>
"""
portal_instructions = """
<h3>Instructions:</h3>
<p>1. Click on New Application.</p>
<p>2. Give it the name of your Rich Presence.</p>
<p>3. Agree the Discord ToS and Policy.</p>
<p>4. Finally click on Create</p>
"""
information_instructions = """
<h3>Instructions:</h3>
<p>1. Copy the application ID</p>
<p>2. Go into the Rich Presence tab at the left</p>
"""
richpresence_instructions = """
<h3>Instructions:</h3>
<p>1. Click on Add Image, name it "large" and upload your desired image (it will be the large image of the rich presence).</p>
<p>2. Click again on Add Image, name it "small" and upload your desired image (it will be the small image of the rich presence).</p>
<p>3. Now close this window and fill in the form in the command prompt, your client id is the one you copied. (If you didn't, go on https://discord.com/developers/applications, select your application and click copy.</p>
"""

refreshed_login = False
refreshed_information = False
refreshed_richpresence = False
refreshed_application = False

while True:
    # Récupérer l'URL actuelle
    current_url = driver.current_url

    # Vérifier l'URL pour afficher les étapes à suivre
    if 'login' in current_url:
        if(refreshed_login == False):
            driver.refresh()
            refreshed_login = True
            refreshed_information = False
            refreshed_richpresence = False
            refreshed_application = False
        add_instructions(driver, login_instructions)
    elif 'information' in current_url:
        if(refreshed_information == False):
            driver.refresh()
            refreshed_login = False
            refreshed_information = True
            refreshed_richpresence = False
            refreshed_application = False
        add_instructions(driver, information_instructions) 
    elif 'rich-presence' in current_url:
        if(refreshed_richpresence == False):
            driver.refresh()
            refreshed_login = False
            refreshed_information = False
            refreshed_richpresence = True
            refreshed_application = False
        add_instructions(driver, richpresence_instructions) 
    elif 'application' in current_url:
        if(refreshed_application == False):
            driver.refresh()
            refreshed_login = False
            refreshed_information = False
            refreshed_richpresence = False
            refreshed_application = True
        add_instructions(driver, portal_instructions)
        
    # Attendre un peu avant de vérifier à nouveau l'URL
    time.sleep(1)
