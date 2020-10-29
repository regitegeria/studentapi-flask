# studentapi-flask
Student API Using Flask And MongoDB

# How to start
1. Create Virtual Environment => virtualenv venv
2. Activate Virtual Environment => source venv/bin/activate
3. Install requirements => pip install -r req.txt
4. Start project => python app.py

# How to start using gunicorn
1. gunicorn -w 3 -b 0.0.0.0:3000 wsgi:app