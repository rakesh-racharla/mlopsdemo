from flask import Flask, request, jsonify
import onnxruntime as rt
import numpy


sess = rt.InferenceSession("Prod_Model/model.onnx")

app = Flask(__name__)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        user_data = request.form['data']
        inf_data = numpy.array(user_data.split(","))
        input_name = sess.get_inputs()[0].name
        label_name = sess.get_outputs()[0].name
        pred_onx = sess.run([label_name], {input_name: numpy.expand_dims(inf_data.astype(numpy.float32), axis=0)})[0]
        return jsonify(str(pred_onx[0][0]))

if __name__ == '__main__':
   app.run(host= '0.0.0.0',port= 5001,debug=True)