### Tutorial
## Prerequisites

1.  docker

### Project setup
```
git clone
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
![image](https://github.com/YuxiaoLi1234/fzvis/assets/143280350/9cc69ab6-f1bd-4341-a2ee-be83ed3c19ca)

### Workflow


## run compressor:
  enter the configuration and also the absolute path of your input file. After you have configured all the options, press the Enter key.
  <img width="434" alt="image" src="https://github.com/YuxiaoLi1234/fzvis/assets/143280350/118e1975-5c44-4e41-9665-404b73f382c9">
  ```
  compresoor_id: Please enter the compressor that is supported by libpressio.
  ```
  ```
  early config: Please include your input with single quotation mark, if you are going to include a path in your configuration, please make sure you entered the absolute path.
  ```
  ```
  compressor_config: Please include your input with single quotation mark. 
  ```
  ```
  path_to_input_data: Please enter the absolute path of your input file. Include your input with single quotation mark. Make sure your data format is '.npy'
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









