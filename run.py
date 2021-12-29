from app import app
from app import routes
from app import databaseCreate

databaseCreate.create()

if __name__ == '__main__':
    from waitress import serve
    print("Server running on port 8080...")
    serve(app,host='0.0.0.0', port=8080)
    
