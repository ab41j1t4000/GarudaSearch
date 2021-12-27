from app import app
from app import routes
from app import databaseCreate

databaseCreate.create()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
