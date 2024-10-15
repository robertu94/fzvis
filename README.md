### Tutorial
## Prerequisites

1.  docker
2.  docker-compose

### Project setup
```
git clone https://github.com/YuxiaoLi1234/fzvis.git
cd fzvis
run `docker-compose up`
```

### Compiles and hot-reloads for development
## Set up configure
enter your ip address and port in config.json

```
run `npm run serve` to start vue.
```

```
run `pip3 install -r requirements.txt` to setup the python enviroments.
run `python3 src/components/main.py` to run the backend code.
```

```
The dashboard should look like this figure.
```
<img width="1450" alt="Screenshot 2024-10-15 at 7 33 09 PM" src="https://github.com/user-attachments/assets/4ceef310-2008-403f-88a4-1f332e88943f">

### Workflow


## run compressor:
  Enter the configuration. After you have configured all the options, press the Enter key.
  <img width="1446" alt="Screenshot 2024-10-15 at 7 29 53 PM" src="https://github.com/user-attachments/assets/e316561f-f623-4757-851e-4f8ced961ff1">
  ```
  compresoor_id: Please enter the compressor that is supported by libpressio.
  ```
  ```
  You can upload load your file by the fileloader (you can also download the example data "inputfile500.npy/inputfile1000.npy" in the file.
  ```
  ```
  early config: Please include your input with single quotation mark, if you are going to include a path in your configuration, please make sure you entered the absolute path.
  ```
  ```
  compressor_config: Please include your input with single quotation mark. 
  ```
  ```
  
  ```
  ```
  compressor_name: The name for this configuration of compressor.
  ```
  - After running all the compressors you need for visualization, click draw on module D.
  - The reuslt in module D should be like the figure below:
  
<img width="1038" alt="image" src="https://github.com/YuxiaoLi1234/fzvis/assets/143280350/4e6f1403-e7be-4e2f-97d8-ffbc21801ae3">

- You can add a new compressor by enter the configuration in module A, remember to click the button Draw in module D to get the new result.

### Interaction usage:
## Compare Matrics among Compressors.
1. After running all compressors, you need to click on the name of the compressors you want to compare:
<img width="850" alt="image" src="https://github.com/YuxiaoLi1234/fzvis/assets/143280350/be90256f-ad14-4e28-a7d6-9383e85b5734">

2. Click on the compressor_compare button, the result shoule be like the figure below:
<img width="1028" alt="image" src="https://github.com/YuxiaoLi1234/fzvis/assets/143280350/9b62cdaa-fe26-43c6-ac68-f71e1f615407">

(click on the all_compressor button to return to the visualization of barcharts of all of the compressors)
3. Then you could interactively select the parameter and compressor you want in module B.

## Input Data Vis:
- After running the compressors, you can visualize the slice of your input data in module C.
- Make sure that you input your slice_id, format of your inputdata.
- Click on the DataVis button to visualize your data.
- There is a defaultcolormap selector on the top left. You can also add control points by clicking on the colormap for the colormap (under the mode of "add_points")/ drag the existing control points (under the mode of "use current control points").
<img width="424" alt="image" src="https://github.com/YuxiaoLi1234/fzvis/assets/143280350/7bbbc7e4-20fa-49d3-88f3-f701018bc6b0">









