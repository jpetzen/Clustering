# Anotacije
## Streamlit+Fastapi+sql lite
Primer anotacije za nadaljno uporabo pri ML. 

---

### Navodila

Najprej v glavnem folderju ustvarimo virtualno okolje.

`source .venv/bin/activate`                                     

Namestimo vse potrebne knjižnice.

`pip install -r requirements.txt`   

Zaženemo bazo.

`python3 -m uvicorn main:app --host 0.0.0.0` 

Ter zaženemo uporabniški umesnik.

`streamlit run UI.py --server.port 8080`                                            

Uporabnik obišče http://195.47.197.50:8080      

---

### Narejeno z
-Streamlit
https://streamlit.io/   

-FastAPI
https://fastapi.tiangolo.com/

-SQLite
https://www.sqlalchemy.org/

---

### Avtor

Jure Potočnik

---

### License
This project is licensed under the MIT License - see the LICENSE.md file for details.
