<template>
  <div id="input-dataset">
      <div id="input-dataset-container">
      <h3>Upload Input Dataset</h3>
      <input type="file" id="fileloader" @change="handleFileChange">
      <!-- <t-input id='width' label="width:" v-model="width" placeholder=500 @input="emitFileData"/>
      <t-input id='height' label="height:" v-model="height" placeholder=500 @input="emitFileData"/>
      <t-input id='depth' label="depth:" v-model="depth" placeholder=1 @input="emitFileData"/> -->
      <h6 v-if="fileContent">File Loaded: {{ fileContent }}</h6>
      </div>
  </div>
</template>
<style scoped src="@/assets/InputDataset.css"></style>
<script>
import emitter from './eventBus.js';
export default {
name: 'InputDataset',
data() {
  return {
  depth:null,
  width:null,
  height:null,
  fileContent:"",
  formData: new FormData(),
  files:[],
  infoMessage:'',
  file:'',
  uploadMethod: 'requestSuccessMethod',
  };
},
methods:{
handleFileChange(event){
  
  const file = event.target.files[0]; 
  if(this.formData.has('file')){
    this.formData.delete("file");
  }
  this.formData.append("file", file);
  this.fileContent = file.name;
  console.log(this.fileContent)
  this.file = file;
  console.log(this.width)
  this.emitFileData();
  // emitter.emit('file-selected', {"file": file, "width": this.width, "height": this.height, "depth":this.depth});
  
},

emitFileData() {
      if (this.file) {
        console.log("Emitting file data:", this.fileContent);
        emitter.emit('file-selected', {
          file: this.file,
          // width: this.width,
          // height: this.height,
          // depth: this.depth
        });
      }
    },

requestSuccessMethod(file /* UploadFile */) {
  console.log(file, file.raw);
  return new Promise((resolve) => {
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
      resolve({ status: 'success', response: { url: 'https://tdesign.gtimg.com/site/avatar.jpg' } });

      clearTimeout(timer);
      clearInterval(percentTimer);
    }, 800);
    console.log(resolve)
    
  });
},
requestFailMethod(file ) {
  console.log(file);
  return new Promise((resolve) => {
    resolve({ status: 'fail', error: '上传失败，请检查文件是否符合规范' });
  });
},

},
computed: {
requestMethod() {
  return this[this.uploadMethod];
},
},
watch: {
  uploadMethod() {
      this.files = [];
  },
  },
};
</script>

<!-- <style>
#depth{
position: absolute;
top:60%;
left:68%;
z-index:101;
width: 20%

}
#width{
position: absolute;
top:60%;
left:2%;
z-index:101;
width: 20%
}
#height{
position: absolute;
top:60%;
left:38%;
z-index:101;
width: 20%
}
</style> -->

