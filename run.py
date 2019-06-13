import locale

import api


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

server = api.make_flask_server()

app = server.flask_app
api = server.flask_api

if __name__ == '__main__':
    app.run(debug=True)
