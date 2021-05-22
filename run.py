from iotech import app, socketio

if __name__ == '__main__':
    # app.run(debug=False)
    socketio.run(app, host='192.168.1.7', port=5000)