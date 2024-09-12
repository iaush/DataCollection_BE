Initialize Environment:
1) Remove venv folder if needed
2) Create a new python venv: python -m venv venv
3) run : .\venv\Scripts\activate
4) install dependencies on venv : pip install -r requirements.txt
5) create a .env file in /backend folder with the following:
AWS_ACCESS_KEY_ID=<>
AWS_SECRET_ACCESS_KEY=<>
AWS_DEFAULT_REGION=<>

To run application :
1) run : .\venv\Scripts\activate
2) run : uvicorn main:app --host 0.0.0.0 --port 8000 --reload

venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload