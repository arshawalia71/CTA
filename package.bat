@echo off

python -m pip install --upgrade pip
pip install virtualenv

virtualenv cta_env
call cta_env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
start python manage.py runserver
start streamlit run cta/main.py
deactivate
pause