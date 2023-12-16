import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import sys
import json
import libpressio
from pathlib import Path
# 1. 生成50x50的数据集åç
if __name__ == '__main__':
    arguments = sys.argv
    #print(arguments)
    bound = 0.001
    compressor_id = arguments[1]
    #early_config = {arguments[2].split('=')[0]:arguments[2].split('=')[1]}
    early_config = eval(arguments[2])
    #early_config = {i.split('=')[0]:i.split("=")[1] for i in str(arguments[2]).split('+')}
    #print(type(early_config))
    #compressor_config = {arguments[3].split('=')[0]:arguments[3].split('=')[1]}
    #print(str(arguments[3]),'ahjkhhxoihjaeoijsd')
    compressor_config = eval(arguments[3])
    #compressor_config = {i.split('=')[0]:i.split("=")[1] for i in str(arguments[3]).split(',')}
    input_data_path = arguments[4]
    #print(compressor_id, early_config, compressor_config,input_data_path)
    width,height,num_blob = 600,600,6
    compressor = libpressio.PressioCompressor.from_config({
        # configure which compressor to use
        "compressor_id": compressor_id,
        # configure the set of metrics to be gathered
        "early_config": early_config,
        # configure SZ
        "compressor_config": compressor_config})
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    x,y = np.meshgrid(x, y)
    x = x.flatten()
    y = y.flatten()
    # input_data = np.zeros_like(x)
    input_data = np.load(input_data_path)   
    def run_compressor():
        compressor = libpressio.PressioCompressor.from_config({
        # configure which compressor to use
            "compressor_id": compressor_id,
        # configure the set of metrics to be gathered
            "early_config": early_config,
            # configure the compressor
            "compressor_config": compressor_config
        })

    # run compressor to determine metrics
        decomp_data = input_data.copy()
        comp_data = compressor.encode(input_data)   
        decomp_data = compressor.decode(comp_data, decomp_data)
        metrics = compressor.get_metrics()

        return {"compressor_id": compressor_id,"bound": bound,"metrics": metrics}  

    result = run_compressor()
    compressor_id,bound,metrics = result['compressor_id'],result['bound'],result['metrics']
    print(f"bound={bound:1.0e}, metrics={json.dumps(metrics, indent=4)}")                                           
