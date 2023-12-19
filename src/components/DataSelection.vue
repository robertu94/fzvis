<template>
    <t-space>
    <t-loading :loading="loading" text="loading compressor..." fullscreen />
      <!-- <t-switch v-model="loading"></t-switch> -->

  </t-space>
    <div id="data_selection">
        <p>Enter your Configuration here</p>

        <t-input id = 'input1' v-model="compressor_id" placeholder='sz' label="compressor_id:"  @enter="update"/>
        <t-input id = 'input5' v-model="compressor_name" placeholder='sz1' label="compressor_name:"  @enter="update"/>

        <t-input id = 'input2' v-model="early_config" placeholder='{"pressio:metric":"composite","composite:plugins": ["time","size","error_stat","external"]}' label="early_config:"  @enter="update"/>
        <t-input id = 'input3' v-model="compressor_config" placeholder='{"pressio:abs": 0.001}' label="compressor_config:"  @enter="update"/>
        <t-input id = 'input4' v-model="input_data" placeholder='/home/yli/lyx/libpressio/test1/libpressio_tutorial/exercises/datasets/CLOUDf48.bin.f32' label="path_to_input_data:"  @enter="update"/>
        <!-- <t-alert theme="error" :message="infoMessage">  </t-alert> -->
        
        <p id="temp1" ></p>

    </div>

    <!-- need a place to upload the inputdata -->
</template>

<script>
import axios from 'axios'
import emitter from './eventBus.js';
import config from '../../config.json';

export default {
  name:'DataSelection',
  data(){
      return{
        infoMessage:'',
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
  
  methods:{
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
            
            axios.post("http://"+this.host+':'+ String(this.port)+'/indexlist',{
                
            'compressor_id':this.compressor_id,
            'early_config':this.early_config,
            'compressor_config':this.compressor_config,
            'input_data':this.input_data,
            'loaddata':this.loaddata,
            'slice_id':0
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
    height: 26%;
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
    top:25%;
    left:10%
}
#input3{
    position:absolute;
    width:70%;
    top:45%;
    left:10%
}

#input4{
    position:absolute;
    width:70%;
    top:65%;
    left:10%
}
#input5{
    position:absolute;
    width:70%;
    top:85%;
    left:10%
}
p{
    position:absolute;
    left:10%
}
#temp1{
    display: none;
}
</style>