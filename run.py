from iotech import app, socketio

if __name__ == '__main__':
    # app.run(debug=False)
    socketio.run(app, host='127.0.0.1', port=5000)