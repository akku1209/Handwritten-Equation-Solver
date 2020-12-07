import tensorflow as tf
import base64
import json
import math
from flask import Flask, render_template, request
from cnn import ConvolutionalNeuralNetwork
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    operation = BytesIO(base64.urlsafe_b64decode(request.form['operation']))
    CNN = ConvolutionalNeuralNetwork()
    operation = CNN.predict(operation)
    n_operation = operation.replace('x','*')
    
    count = n_operation.count('√')
    while(count>0):
        pos = n_operation.find('√')
        if pos!=-1:
            sqrt_buff = ''
            i=1
            while(pos+i<len(n_operation) and n_operation[pos+i].isdigit()):
                sqrt_buff += n_operation[pos+i]
                i=i+1
            root = math.sqrt(int(sqrt_buff))
            n_operation = n_operation.replace('√'+sqrt_buff,str(root))
        count = count-1
        
    return json.dumps({
        'operation': operation,
        #'solution': calculate_operation(operation)
        'solution': eval(n_operation)
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
