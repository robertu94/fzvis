<template>
    <t-space>
    <t-loading :loading="loading" text="loading compressor..." fullscreen />
      <!-- <t-switch v-model="loading"></t-switch> -->

  </t-space>
  
    <div id="data_selection">
        <!-- <p>Enter your Configuration here</p> -->
        <input type="file" id="fileloader" @change="handleFileChange" >
        <t-input id = 'input1' v-model="compressor_id" placeholder='sz' label="compressor_id:" />
        <t-input id = 'input5' v-model="compressor_name" placeholder='sz1' label="compressor_name:"  />
        
        
        <t-textarea auto-width id = 'input2' v-model="early_config" placeholder='early_config:{"pressio:metric":"composite","composite:plugins": ["time","size","error_stat","external"]}' label="early_config:"  />
        <t-textarea  auto-width id = 'input3' v-model="compressor_config" placeholder='compressor_config:{"pressio:abs": 0.001}' label="compressor_config:"  />
        <!-- <t-input id = 'input4' v-model="input_data" placeholder='/path_to_input_data' label="path_to_input_data:"  @enter="update"/> -->
        <!-- <t-upload ref="uploadRef" id="fileloader" v-model="files"  :requestMethod="requestSuccessMethod"><t-button theme="primary">upload data</t-button>
             </t-upload> -->
        <button id='update_button' @click="update">submit</button>
        <p id="temp1" ></p>

    </div>
    
    <!-- need a place to upload the inputdata -->
</template>

<script>
import axios from 'axios'
import emitter from './eventBus.js';
import config from '../../config.json';
// import Npyjs from 'npyjs';
export default {
  name:'DataSelection',
  data(){
      return{
        uploadMethod: 'requestSuccessMethod',
        fileContent:"",
        formData: new FormData(),
        files:[],
        reader : new FileReader(),
        infoMessage:'',
        file:'',
        loaddata:0,
        host:config.API_HOST,
        port:config.API_PORT,
        loading:false,
        compressor_id:'zfp',
        early_config:'{"pressio:metric":"composite","composite:plugins": ["time","size","error_stat","external"]}',
        compressor_config:'{"pressio:abs": 0.001}',
        input_data:null,
        compressor_name:'zfp1',
        msg:'',
        compare_data:{'compressor_id':[],'bound':[],'metrics':[],'input_data':''},
      };
  },
  computed: {
    requestMethod() {
      return this[this.uploadMethod];
    },
  },
  watch: {
    // 切换上传示例时，重置 files 数据
    uploadMethod() {
      this.files = [];
    },
  },
  methods:{
    
    handleFileChange1(event) {
        const file = event.target.files[0];
        let reader = new FileReader();
        var _this = this;
        if(file){
            var fileName = file.name;
            var fileExtension = fileName.split('.').pop().toLowerCase();
            // const file = event.target.files[0];
            switch(fileExtension) {
                case 'txt':
                    reader.onload = function(array) {
                        
                        _this.fileContent = array.target.result;
                        console.log(array.target.result);
                    };

                    reader.readAsText(file);
                    break;
                case 'json':
                // 处理JSON文件
                    // _this.fileContent = JSON.parse(content);
                    reader.onload = function(array) {
                        
                        _this.fileContent =  JSON.parse(array.target.result);
                        console.log(array);
                    };
                    // console.log('JSON file content:', JSON.parse(content.e.target.result));
                    reader.readAsText(file);
                    break;
                case 'npy':
                    
                    reader.onload = function(arrayBuffer) {
                        let array = arrayBuffer.target.result
                        const dataView = new DataView(array);
                        const decoder = new TextDecoder("ascii");
                        
                        // 魔数和版本号
                        const magic = decoder.decode(new Uint8Array(array.slice(0, 6)));
                        console.log(magic)
                        if (magic !== '\x93NUMPY') {
                            throw new Error('Not a valid .npy file');
                        }
                        
                        const majorVersion = dataView.getUint8(6);
                        // const minorVersion = dataView.getUint8(7);
                        let headerLength, offset;
                        if (majorVersion === 1) {
                            headerLength = dataView.getUint16(8, true); // Assuming little-endian
                            offset = 10;
                        } else if (majorVersion === 2) {
                            headerLength = dataView.getUint32(8, true); // Assuming little-endian
                            offset = 12;
                        } else {
                            throw new Error('Unsupported .npy version');
                        }
                        
                        // 读取头部内容
                        const headerStr = decoder.decode(new Uint8Array(array.slice(offset, offset + headerLength)));
                        console.log("Header:", headerStr);
                        const dataType = headerStr.dataType; // 例如 'float32'
                        const dataOffset = headerStr.dataOffset; // 数据开始的位置
                        const dataLength = headerStr.dataLength; // 数据长度，根据形状计算得出
                        console.log(dataType)
                        let typedArray;
                        switch (dataType) {
                            case 'float32':
                                typedArray = new Float32Array(array, dataOffset, dataLength);
                                break;
                            case 'int32':
                                typedArray = new Int32Array(array, dataOffset, dataLength);
                                break;
                            case 'float64':
                              typedArray = new Float64Array(array, dataOffset, dataLength);
                                  break;
                            // 添加更多数据类型的处理...
                            default:
                                throw new Error('Unsupported data type');
                        }
                        console.log(typedArray)
                        let float32Array = Array.from(new Float64Array(array));
                        // let blob = new Blob([float32Array], { type: 'application/octet-stream' });
                        _this.fileContent = float32Array
                        console.log(float32Array);
                    };

                    reader.readAsArrayBuffer(file);
                    break;
            default:
                // 未知文件类型
                    console.log('Unknown file type');
            }
            // reader.readAsText(file,'UTF-8')
            // reader.onload = e => {
            // content = e.target.result; //要使用读取的内容，所以将读取内容转化成Uint8Array
            // // ints = ints.slice(0, 5000); //截取一段读取的内容
            // // let snippets = new TextDecoder('gb2312').decode(ints); //二进制缓存区内容转化成中文（即也就是读取到的内容）
            
            
            
            // };
            // reader.readAsText(file);

        }
        
        

        // console.log(_this.fileContent) // String 
    },

    handleFileChange(event){
      const _this = this
      // const input = document.getElementById('fileloader');
      const file = event.target.files[0]; // 获取选中的文件
      // const formData = new FormData();
      if(_this.formData.has('file')){
        _this.formData.delete("file");
      }
      _this.formData.append("file", file);
       // 将文件添加到表单数据中
      // _this.fileContent = formData
      // fetch('/upload', { // 假设 '/upload' 是你的后端接口
      //     method: 'POST',
      //     body: formData,
      // })
      // .then(response => response.json())
      // .then(data => console.log(data))
      // .catch(error => console.error('Error:', error));
      console.log(_this.fileContent)
    },

    requestSuccessMethod(file /** UploadFile */) {
      console.log(file, file.raw);
      return new Promise((resolve) => {
        // 控制上传进度
        let percent = 0;
        const percentTimer = setInterval(() => {
          if (percent + 10 < 99) {
            percent += 10;
            this.$refs.uploadRef.uploadFilePercent({ file, percent });
            
          } else {
            clearInterval(percentTimer);
          }
        }, 100);

        const timer = setTimeout(() => {
          // resolve 参数为关键代码
          resolve({ status: 'success', response: { url: 'https://tdesign.gtimg.com/site/avatar.jpg' } });

          clearTimeout(timer);
          clearInterval(percentTimer);
        }, 800);
        console.log(resolve)
        
      });
    },
    requestFailMethod(file /** UploadFile */) {
      console.log(file);
      return new Promise((resolve) => {
        // resolve 参数为关键代码
        resolve({ status: 'fail', error: '上传失败，请检查文件是否符合规范' });
      });
    },
    update:function(){
        
        if(this.compressor_id.length == 0 || this.early_config.length == 0 || this.compressor_config.length == 0){
            
            this.msg = this.$message.info({
                    content: 'input is illegal',
                    theme:"warning",
                    duration: 1000,
                    // 层级控制：非当前场景自由控制开关的关键代码，仅用于测试 API 是否运行正常
                    zIndex: 1001,
                    // 挂载元素控制：非当前场景自由控制开关的关键代码，仅用于测试 API 是否运行正常
                    attach: document.body,
                });
        }
        else{
            // const that = this
            this.loading = true
            // enter 'http://your_ip:5000/indexlist'
            // console.log(this.fileContent)
            // console.log("http://"+this.host+':'+ String(this.port)+'/indexlist')
            // console.log(this.compressor_config)
            // console.log(this.formData['compressord_id'])
            // this.formData['compressord_id'] = this.compressor_id;
            if(this.formData.has('compressor_id')){
              this.formData.delete('compressor_id');
            }
            
            this.formData.append('compressor_id', this.compressor_id);
            
            if(this.formData.has('early_config')){
              this.formData.delete('early_config');
            }
            this.formData.append('early_config', this.early_config);
            if(this.formData.has('compressor_config')){
              this.formData.delete('compressor_config');
            }
            
              this.formData.append('compressor_config', this.compressor_config);
            
            if(this.formData.has('loaddata')){
              this.formData.delete('loaddata');
              
            }
            this.formData.append('loaddata', this.loaddata);
            if(this.formData.has('slice_id')){
              this.formData.delete('slice_id');
              
            }
            this.formData.append('slice_id', 0);
            
            
            
            // this.formData.compressor_id = this.compressor_id
            console.log(this.formData)
            axios.post("http://"+this.host+':'+ String(this.port)+'/indexlist',
              this.formData
            ).then(response=>{
                
                let need1 = response.data
                console.log('接受数据',typeof(need1))
                this.compare_data['compressor_id'].push(this.compressor_name)
                this.compare_data['bound'].push(need1['bound'])
                this.compare_data['metrics'].push(need1['metrics'])
                this.compare_data['input_data']=this.input_data
                document.getElementById('temp1').innerHTML=JSON.stringify(this.compare_data)
                emitter.emit('myEvent', this.compare_data);
                this.loading = false
                //this.formData = new FormData()
            })
            .catch((error)=>{
                this.loading = false
                // this.infoMessage = 'illegal input'
                alert('illegal input');
                console.log(error)
            })
        }
        
    }
  }
}
</script>

<style scoped>
#data_selection{
    border:2px solid #a7b2ac;
    border-radius: 4px;
    position:absolute;
    top:1%;
    left:.7%;
    width: 28%;
    height: 38%;
}
#input1{
    position:absolute;
    width:70%;
    top:5%;
    left:10%
}
#input2{
    position:absolute;
    width:70%;
    top:37%;
    left:10%
}
#input3{
    position:absolute;
    width:70%;
    top:57%;
    left:10%
}

#input4{
    position:absolute;
    width:77%;
    top:70%;
    left:10%
}
#input5{
    position:absolute;
    width:70%;
    top:80%;
    left:10%
}
p{
    position:absolute;
    left:10%
}
#temp1{
    display: none;
}
#fileloader{
    position: absolute;
    top:19%;
    left:10%;
}
#update_button{
  position: absolute;
  
  top:82%;
  left:85%
}
</style>