import os
from flask import Flask, request
from flask_cors import CORS
import json
from pathlib import Path
import numpy as np
from argparse import ArgumentParser
import libpressio
import math
# a way to upload the input data is needed
app = Flask(__name__)
CORS(app)

@app.route('/indexlist',methods=["GET","POST"])

def indexlist():
    global input_data
    def replace_unsupported_values(obj):
        if isinstance(obj, dict):
            return {k: replace_unsupported_values(v) for k, v in obj.items()}
        elif obj == math.inf:
            return "Infinity"  
        elif obj == - math.inf:
            return "-Infinity"  
        
        elif obj == None:
            return 'null'
        elif isinstance(obj, float) and math.isnan(obj): return 'null'
        else:
            return obj
        
    def comparing_compressor(arguments):
        global input_data
        input_data = arguments['input_data']
        configs = {
                "compressor_id": arguments["compressor_id"],
                "input_data": input_data
        }
        
        def run_compressor(args):
            global input_data
            compressor = libpressio.PressioCompressor.from_config({
                "compressor_id": args['compressor_id'],
                
            })
            decomp_data = input_data.copy()
            comp_data = compressor.encode(input_data)
            decomp_data = compressor.decode(comp_data, decomp_data)
            metrics = compressor.get_metrics()
            metrics1 = replace_unsupported_values(metrics)
            return {'compressor_id': configs["compressor_id"], 'metrics': metrics1}
        result = run_compressor(configs)
        print(result)
        return result
    print('yes')
    if request.method == 'POST':
       
        if request.form:
            loaddata = eval(request.form['loaddata'])
        else:
            loaddata = 1
        print(loaddata)

        if loaddata==0:
            file = request.files['file']
            if file:
                input_data = np.load(file)
            else:
                input_data = None

            compressor_id = request.form['compressor_id']
            compressor_name = request.form['compressor_name']
            selected_metrics = json.loads(request.form.get('selected_metrics', '{}'))
            configration = {'compressor_id':compressor_id, 
                            'input_data':input_data
                            }
        
            output = comparing_compressor(configration)
            return json.loads(json.dumps(output,indent=2))
        
        else:
            slice_number = eval(json.loads(request.data)['slice_number'])
            slice_width = eval(json.loads(request.data)['slice_width'])
            slice_height = eval(json.loads(request.data)['slice_height'])
            sliced_id = eval(json.loads(request.data)['slice_id'])
            array = input_data.reshape(slice_number,slice_width,slice_height)[sliced_id].tolist()
            return json.dumps(array)
    else:
        return 'configuration is illegal'

parser = ArgumentParser(description="enter your HOST/POST.",
                                     usage="path/to/main.py [OPTIONAL ARGUMENTS] <HOST> <PORT> <configfile>")

parser.add_argument('--HOST', nargs='?', help='HOST_address', default="localhost")
parser.add_argument('--PORT', nargs='?', help='PORT_address', default="5000")

parser.add_argument('--configfile', nargs='?', help='your_config_file', default=None)

if __name__ == '__main__':
    input_data = None
    input = parser.parse_args()
    if not any(vars(input).values()):
        parser.print_help()
    print(Path(__file__).parent)
    api_host = os.getenv('HOST', '0.0.0.0')
    api_port = int(os.getenv('PORT', '5000'))
    config = {
        "API_HOST": api_host,
        
        "API_PORT": api_port
        }
    with open('config.json', 'w') as json_file:
        json.dump(config, json_file, indent=4)
    app.run(host=api_host,port = api_port,debug=True)
