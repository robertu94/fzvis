import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import json
import numpy as np
import libpressio
from argparse import ArgumentParser
import math

app = Flask(__name__)

CORS(app)

@app.route('/indexlist', methods=["GET", "POST"])

def indexlist():

    global input_data, depth, height, depth

    def replace_unsupported_values(obj):
        if isinstance(obj, dict):
            return {k: replace_unsupported_values(v) for k, v in obj.items()}
        elif obj == math.inf:
            return "Infinity"
        elif obj == -math.inf:
            return "-Infinity"
        elif obj is None:
            return 'null'
        elif isinstance(obj, float) and math.isnan(obj):
            return 'null'
        else:
            return obj
    def comparing_compressor(arguments):
        global  input_data, width, depth, height
        input_data = arguments['input_data']
        print(len(input_data))
        configs = {
            "compressor_id": arguments["compressor_id"],
            "early_config": arguments["early_config"],
            "compressor_config": arguments["compressor_config"],
            "bound": arguments["compressor_config"]["pressio:abs"]
        }
        def run_compressor(args):
            global input_data, width, height, depth

            print("Received early_config:", args['early_config'])
            compressor = libpressio.PressioCompressor.from_config({
                "compressor_id": args['compressor_id'],
                "early_config": args['early_config'],
                "compressor_config": args['compressor_config']
            })
            decomp_data = input_data.copy()
            comp_data = compressor.encode(input_data)
            decomp_data = compressor.decode(comp_data, decomp_data)
            metrics = compressor.get_metrics()
            print("Received early_config 2nd time:", args['early_config'])
            print("Metrics returned by compressor:", metrics)
            metrics1 = replace_unsupported_values(metrics)
            print("Sanitized metrics:", metrics1)
            #return {'compressor_id': configs["compressor_id"], 'bound': configs['bound'], 'metrics': metrics1}
            return {
                "compressor_id": args['compressor_id'],
                "bound": args['bound'],
                "metrics": metrics1
            }
        result = run_compressor(configs)
        print(result)
        # print(result)
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
            width = int(request.form['width'])
            height = int(request.form['height'])
            depth = int(request.form['depth'])
            input_data = np.load(file).reshape(width, height, depth)
            
            compressor_id = request.form['compressor_id']
            early_config = json.loads(request.form.get('early_config'))
            compressor_config = json.loads(request.form.get('compressor_config'))
            configration = {'compressor_id':compressor_id, 
                            'early_config':early_config,
                            'compressor_config':compressor_config,
                            'input_data':input_data
                            }
            print(configration)
            print("Received early_config:", early_config)
            output = comparing_compressor(configration)
            result = {"output": output, "input_data":input_data.tolist()}
            #return json.loads(json.dumps(output,indent=2))
            return result
        else: 
            return 0
            # print(slice_number,sliced_id,slice_width,slice_height,type(input_data),len(input_data))
            
    else:
        return 'configuration is illegal'

parser = ArgumentParser(description="enter your HOST/POST.", usage="path/to/main.py [OPTIONAL ARGUMENTS] <HOST> <PORT> <configfile>")

parser.add_argument('--HOST', nargs='?', help='HOST_address', default="localhost")
parser.add_argument('--PORT', nargs='?', help='PORT_address', default="5000")

parser.add_argument('--configfile', nargs='?', help='your_config_file', default=None)   

if __name__ == '__main__':
    input_data = None
    width = -1
    height = -1
    depth = -1
    input = parser.parse_args()
    if not any(vars(input).values()):
        parser.print_help()
    print(Path(__file__).parent)
    print(input)
    api_host = input.HOST
    api_port = input.PORT
    config = {
        "API_HOST": api_host,
        "API_PORT": api_port
    }
    with open('./config.json', 'w') as json_file:
        json.dump(config, json_file, indent=4)
    app.run(host=api_host, port = api_port, debug=True)

