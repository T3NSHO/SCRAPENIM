import requests
from bs4 import BeautifulSoup
from flask import jsonify
import re
from urllib.parse import quote

login_url = "https://edu.mines-rabat.ma/" 

pattern = r"(E[0-9])\w+"

def enim_login(username,password):
    session = requests.Session()
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.content, 'html.parser')
    auth_token = soup.find('input', {'name': 'authenticity_token'})['value']
    
    payload = {
        'user[username]': username,
        'user[password]': password,
        'authenticity_token': auth_token
    }
    
    response = session.post(login_url, data=payload)
    if "Bienvenue" in response.text :
        return {"status": "success"} , session
    else :
        return {"status": "failed"} , None


def check_creds(response , session=None):
    print(response)
    if response['status'] == "success" :
        dashoboard = session.get('https://edu.mines-rabat.ma/user/dashboard')
        soupkhra = BeautifulSoup(dashoboard.content,'html.parser')
        profile = soupkhra.find(id="student_details_button")['href']
        firstname = soupkhra.find(attrs={'class':'profile-link'}).text
        username = soupkhra.find(attrs={'class':'profile-link'})['href']
        match= re.search(pattern,username)
        username = match.group()
        profilepage = session.get(login_url+profile)
        anothersoup = BeautifulSoup(profilepage.content,'html.parser')
        name = anothersoup.find('h5').text
        telephone_tr = anothersoup.find('td', string='Téléphone').find_next_sibling('td')
        picture = anothersoup.findAll('img')[2]['src']
        phone_number = '0'+telephone_tr.text.strip()
        filliere = anothersoup.findAll('h6')[1].text
        cartenational = anothersoup.findAll('h6')[2].text
        email = firstname.replace(' ','').lower() + '.' +name.replace(firstname,'').replace(' ','').lower() + '@enim.ac.ma'
        session.close()
        return jsonify({"status": "success", "name": name.replace('  ',' ').strip(), "email" : email ,"id": username, "phone_number": phone_number, "filliere": filliere, "cartenationale": cartenational , 'image':picture})
    else :
        session.close()
        return  jsonify({"status": "failed" , "error message":"failed to retrieve data "})
        
    
    
def get_grades():
    pass