Initialize Environment:
1) Remove venv folder if needed
2) Create a new python venv: python -m venv venv
3) run : .\venv\Scripts\activate
4) install dependencies on venv : pip install -r requirements.txt


To run application :
1) run : .\venv\Scripts\activate
2) run : uvicorn main:app --host 0.0.0.0 --port 8000 --reload

venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload