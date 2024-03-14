import requests
from bs4 import BeautifulSoup
import json
from flask import jsonify
import re
from urllib.parse import quote
import json
import sqlite3

login_url = "https://edu.mines-rabat.ma/" 

pattern = r"(E[0-9])\w+"

def get_session(username,password):
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


def get_student_data(session=None):
    if session is not None :
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
        return jsonify({"status": "success", "name": name.replace('  ',' ').strip(), "email" : email ,"id": username, "phone_number": phone_number, "filliere": filliere, "cartenationale": cartenational , 'image':picture})
    else :
        return  jsonify({"status": "failed" , "error message":"failed to retrieve data "})
        
    
    
def get_student_grades(session=None):
    if session is not None:
        grades = {}
        dashoboard = session.get('https://edu.mines-rabat.ma/user/dashboard')
        soupkhra = BeautifulSoup(dashoboard.content,'html.parser')
        grades_link = soupkhra.find(id="academic_button")['href']
        grades_soup = BeautifulSoup(session.get(login_url+grades_link).content,'html.parser')
        tables = grades_soup.find_all('table')

# Loop through each table
        semestre = ""
        for table in tables:
            # Extract the module name from the first row
            # Find all rows containing data
            rows = table.find_all('tr', class_=lambda x: x and ('tr-odd' in x or 'bg-success' in x))
            module = ""
            # Loop through each row
            for row in rows:
                # Extract the elements and grades
                columns = row.find_all('td')

                # Extracting the element name
                
                element_name = columns[0].text.strip()
                
                if element_name[0] == "S" :
                    semestre = element_name
                    grades[semestre] = {}
                else : 
                    absence = columns[1].text.strip()
                    note_av_ratt = columns[2].text.strip()
                    note_ratt = columns[3].text.strip()
                    moyenne = columns[4].text.strip()
                    resultat = columns[5].text.strip()
                        
                    if element_name[0] == "M":
                        module = element_name.replace("'",r"\'")
                        grades[semestre][module] = {"moyenne" : moyenne , "resultat" : resultat}
                        
                    else :
                        element = element_name.replace("'",r"\'")
                        coefficient = re.search(r'\((.*?)\)' , element_name).group(1)
                        grades[semestre][module][element] = {"absence": absence, "note_av_ratt": note_av_ratt, "note_ratt": note_ratt , "coefficient": coefficient }
                    # Extracting the grades
                    

                # Print the extracted data
                
        print(grades)
        grades = json.dumps(grades)
        return jsonify(grades)
                
    else :
        return  jsonify(str({"status": "failed" , "error message":"failed to retrieve data "}))
    
def create_cookie(username , cookietosave):
    con = sqlite3.connect("sessions.db")
    cur = con.cursor()
    existence_check = cur.execute("SELECT * FROM sessions WHERE username = ?",(username,))
    if existence_check.fetchone() is not None:
        cur.execute("DELETE FROM sessions WHERE username = ?",(username,))
    res = cur.execute("INSERT INTO sessions (username,cookie) VALUES (?,?)",(username,str(cookietosave)))
    con.commit()
    con.close()

    
def get_cookie(username):
    con = sqlite3.connect("sessions.db")
    cur = con.cursor()
    res = cur.execute("SELECT cookie FROM sessions WHERE username = ?",(username,))
    s = res.fetchone()[0]
    s = s.replace("\'", "\"")
    cookie = json.loads(s)
    return cookie


