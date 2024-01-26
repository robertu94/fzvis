<template>
    <t-space>
    <t-loading :loading="loading" text="loading compressor..." fullscreen />
      <!-- <t-switch v-model="loading"></t-switch> -->

  </t-space>
  
    <div id="data_selection">
        <!-- <p>Enter your Configuration here</p> -->
        <input type="file" id="fileloader" @change="handleFileChange" >
        <t-input id = 'input1' v-model="compressor_id" placeholder='sz' label="compressor_id:"  @enter="update"/>
        <t-input id = 'input5' v-model="compressor_name" placeholder='sz1' label="compressor_name:"  @enter="update"/>
        
        
        <t-textarea auto-width id = 'input2' v-model="early_config" placeholder='early_config:{"pressio:metric":"composite","composite:plugins": ["time","size","error_stat","external"]}' label="early_config:"  @enter="update"/>
        <t-textarea  auto-width id = 'input3' v-model="compressor_config" placeholder='compressor_config:{"pressio:abs": 0.001}' label="compressor_config:"  @enter="update"/>
        <!-- <t-input id = 'input4' v-model="input_data" placeholder='/path_to_input_data' label="path_to_input_data:"  @enter="update"/> -->
        <!-- <t-upload ref="uploadRef" id="fileloader" v-model="files"  :requestMethod="requestSuccessMethod"><t-button theme="primary">upload data</t-button>
             </t-upload> -->
        
        <p id="temp1" ></p>

    </div>
    
    <!-- need a place to upload the inputdata -->
</template>

<script>
import axios from 'axios'
import emitter from './eventBus.js';
import config from './config.json';
// import Npyjs from 'npyjs';
export default {
  name:'DataSelection',
  data(){
      return{
        uploadMethod: 'requestSuccessMethod',
        fileContent:"",
        files:[],
        reader : new FileReader(),
        infoMessage:'',
        file:'',
        loaddata:false,
        host:config.API_HOST,
        port:config.API_PORT,
        loading:false,
        compressor_id:null,
        early_config:null,
        compressor_config:null,
        input_data:null,
        compressor_name:null,
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
    
    handleFileChange(event) {
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
                    // reader = new Npyjs();
                    // n.load("test.npy");
                    // reader.parse(file, (data) => {
                    //     // 'data' 是从 .npy 文件解析出的数据
                    //     console.log(data);
                    // });
                    reader.onload = function(array) {
                        
                        let float32Array = Array.from(new Float32Array(array.target.result));
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
            console.log(this.fileContent)
            // console.log("http://"+this.host+':'+ String(this.port)+'/indexlist')
            axios.post("http://"+this.host+':'+ String(this.port)+'/indexlist',{
                
            'compressor_id':this.compressor_id,
            'early_config':this.early_config,
            'compressor_config':this.compressor_config,
            'input_data':this.fileContent,
            'loaddata':this.loaddata,
            'slice_id':0,
            
            }).then(response=>{
                
                let need1 = response.data
                console.log('接受数据',typeof(need1))
                this.compare_data['compressor_id'].push(this.compressor_name)
                this.compare_data['bound'].push(need1['bound'])
                this.compare_data['metrics'].push(need1['metrics'])
                this.compare_data['input_data']=this.input_data
                document.getElementById('temp1').innerHTML=JSON.stringify(this.compare_data)
                emitter.emit('myEvent', this.compare_data);
                this.loading = false
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
</style>