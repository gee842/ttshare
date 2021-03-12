from app.flaskapp import app
if __name__ == "__main__":
    app.config['JSON_SORT_KEYS'] = False
    app.run(host='0.0.0.0', port=8001)

#5103618