set -o errexit

pip install -r requirements.txt

npm install
npm run build:css

python manage.py collectstatic --no-input --clear

python manage.py migrate
