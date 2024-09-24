from flask import Flask, jsonify, request 
  
app = Flask(__name__) 
  
  
@app.route('/hello', methods=['GET']) 
def helloworld(): 
    if(request.method == 'GET'): 
        data = {"data": "Hello World"} 
        return jsonify(data) 
  
  
if __name__ == '__runserver__': 
    app.run(debug=True) 