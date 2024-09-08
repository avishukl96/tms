requirement - 1

user login (Jwt), register

TMS - Project
    > __pychache__
    >.venv
    >config
        >db.py
    >models
        >index.py
        >user.py
    >routes
        >index.py
        >user.py
    >Schemas
        >index.py
        >user.py

        

requirement - 2

TMS - Project
    > __pychache__
    >.venv
    >config
        >db.py
    >models
        >index.py
        >user.py
        >task.py
    >routes
        >index.py
        >user.py
        >task.py
    >Schemas
        >index.py
        >user.py
        >task.py


  

requirement - 3

TMS - Project
    > __pychache__
    >.venv
    >config
        >db.py
    >models
        >index.py
        >user.py
        >task.py
        >admin.py
    >routes
        >index.py
        >user.py
        >task.py
        >admin.py
    >Schemas
        >index.py
        >user.py
        >task.py
        >admin.py


  





Environment Setup

1. python -m venv venv
2. Source venv/Scripts/activate

Packages

pip install fastapi sqlalchemy pymysql uvicorn
pip install passlib
pip install fastapi[all] sqlalchemy python-jose passlib uvicorn
pip install jwt
pip install bcrypt
pip install pyjwt #encode
pip install pymysql
pip install pydantic[email]


Auto Reload
uvicorn index:app --reload


pip install -r requirements.txt















