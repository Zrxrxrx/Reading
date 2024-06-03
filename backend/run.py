from app.app import create_app
from config import *

if __name__ == '__main__':
    app = create_app()
    app.run(debug=DEBUG, port=PORT)