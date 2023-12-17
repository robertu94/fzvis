### Tutorial
## Prerequisites

1.  libpressio
2.  nodejs, vue
3.  python (flask, flask_cors, json, numpy)

## Project setup
```
cd to the path that you git clone the code
run `npm install`
```

### Compiles and hot-reloads for development
## Set up configure
enter your ip address and port in config.json

```
run `npm run serve` to start vue.
```

```
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
  After running all the compressors you need for visualization, click draw on view D. The reuslt in view D should be like the figure below:
  
<img width="1038" alt="image" src="https://github.com/YuxiaoLi1234/fzvis/assets/143280350/4e6f1403-e7be-4e2f-97d8-ffbc21801ae3">







