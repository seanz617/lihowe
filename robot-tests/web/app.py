from flask import Flask

app=Flask(__name__)

@app.route('/report')
def first_flask():
    return '/home/workspace/robot-tests/report/report.html' 

if __name__ == '__main__':
    app.run(host="192.168.50.206", port=5000, debug=True)
