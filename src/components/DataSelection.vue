<template>
  <t-space>
    <t-loading :loading="loading" text="loading compressor..." fullscreen />
  </t-space>

  <div id="data_selection">
      <!--Enter your Configuration here-->
      
      <div class="saved-configs">
        <div class="saved-configs-container">
        <h3>Saved Configuration</h3>
        <div class="button-group">
          <t-button @click="showSavedConfig(0)">Save1</t-button>
          <t-button @click="showSavedConfig(1)">Save2</t-button>
          <t-button @click="showSavedConfig(2)">Save3</t-button>
        </div>
        </div>
      </div>
      <div class="input-group">
      <t-select id='compressor-select' name="compressor_id" v-model="compressor_id" :options="compressorOptions" label="Compressor:" />
      <t-input name="bound" v-model="bound" label="Bound:" placeholder="bound" />
      </div>
      <!--<t-select id='compressor-select' v-model="compressor_id" :options="compressorOptions" label="Compressor Name:" />-->
      <div id="metric-selection" :class="closed">
      <t-cascader name="selectedMetrics" v-model="selectedMetrics" :options="compressorMetrics" multiple label="Select Metrics:"
        placeholder="Select Compressor Metrics" :popup-props="{ trigger: 'click'}"/> 
      </div>
      <div class="button-group2">
        <t-button @click="saveConfiguration">Save Configuration</t-button>
        <t-button @click="confirmConfiguration">Confirm Configuration</t-button>
        <t-button id='update_button' @click="submitConfiguration">Submit</t-button>
      </div>
      <div v-if="showConfigWindow" class="config-window">
        <h3> Saved Configuration </h3>
        <p><strong> Compressor ID: </strong>{{ savedConfigurations[selectedSaveSlot].compressor_id }}</p>
        <p><strong> Bound: </strong>{{ savedConfigurations[selectedSaveSlot].compressor_config['pressio:abs'] }}</p>
        <p><strong> Metrics: </strong>{{ savedConfigurations[selectedSaveSlot].early_config['composite:plugins'].join(', ') }}</p>
        <t-button @click="editConfiguration">Edit</t-button>
        <t-button @click="cancelConfiguration">Cancel</t-button>
        
      </div>
      <p id="temp1" ></p>
  </div>
</template>
<style scoped src="@/assets/DataSelection.css"></style>
<script>
import axios from 'axios'
import emitter from './eventBus.js';
import config from '../../config.json';
export default {
name:'DataSelection',
data(){
    return{
      loaddata:0,
      formData: new FormData(),
      host:config.API_HOST,
      port:config.API_PORT,
      loading:false,
      compressor_id:'',
      bound:null,
      input_data:null,
      selectedFile: null,
      msg:'',
      closed: false,
      compare_data:{'compressor_id':[],'bound':[],'metrics':[],'input_data':''},
      compressorOptions: [
      { label: 'SZ', value: 'sz' },
      { label: 'ZFP', value: 'zfp' },
      { label: 'MGARD', value: 'mgard' },
      ],
      selectedMetrics: [],
      savedConfigurations: [
          { compressor_id: '', early_config: {}, compressor_config: {} },
          { compressor_id: '', early_config: {}, compressor_config: {} },
          { compressor_id: '', early_config: {}, compressor_config: {} }
        ],
      selectedSaveSlot: null,
      showConfigWindow: false,
      compressorMetrics: [
      {
        label: 'Composite', value:'composite'
        // children: [
        //   { label: 'Compression Rate', value: 'composite:compression_rate' },
        //   { label: 'Compression Rate Many', value: 'composite:compression_rate_many' },
        //   { label: 'Decompression Rate', value: 'composite:decompression_rate' },
        //   { label: 'Decompression Rate Many', value: 'composite:decompression_rate_many' }
        // ]
      },
      {
        label: 'Error Stat', value:'error_stat'
        // children: [
        //   { label: 'Average Difference', value: 'error_stat:average_difference' },
        //   { label: 'Average Error', value: 'error_stat:average_error' },
        //   { label: 'Difference Range', value: 'error_stat:difference_range' },
        //   { label: 'Error Range', value: 'error_stat:error_range' },
        //   { label: 'Max Error', value: 'error_stat:max_error' },
        //   { label: 'Max REL Error', value: 'error_stat:max_rel_error' },
        //   { label: 'Min Error', value: 'error_stat:min_error' },
        //   { label: 'Min REL Error', value: 'error_stat:min_rel_error' },
        //   { label: 'MSE', value: 'error_stat:mse' },
        //   { label: 'N', value: 'error_stat:n' },
        //   { label: 'PSNR', value: 'error_stat:psnr' },
        //   { label: 'RMSE', value: 'error_stat:rmse' },
        //   { label: 'Value Max', value: 'error_stat:value_max' },
        //   { label: 'Value Mean', value: 'error_stat:value_mean' },
        //   { label: 'Value Min', value: 'error_stat:value_min' },
        //   { label: 'Value Range', value: 'error_stat:value_range' },
        //   { label: 'Value STD', value: 'error_stat:value_std' }
        // ]
      },
      {
        label: 'Size',value:"size"
        // children: [
        //   { label: 'Bit Rate', value: 'bit_rate' },
        //   { label: 'Compressed Size', value: 'compressed_size' },
        //   { label: 'Compression Ratio', value: 'compression_ratio' },
        //   { label: 'De-Compressed Size', value: 'decompressed_size' },
        //   { label: 'Un-Compressed Size', value: 'uncompressed_size' }
        // ]
      },
      {
        label: 'Time', value:"time"
        // children: [
        //   { label: 'Check Options', value: 'check_options' },
        //   { label: 'Compress', value: 'compress' },
        //   { label: 'Compress Many', value: 'compress_many' },
        //   { label: 'Decompress', value: 'decompress' },
        //   { label: 'De-Compress Many', value: 'decompress_many' },
        //   { label: 'Get Options', value: 'get_options' },
        //   { label: 'Set Options', value: 'set_options' }
        // ]
      }
    ],
  };   
},
computed: {
  flattenedCompressorMetrics() {
      return this.compressorMetrics.map(category => {
      return {
        label: category.label,
        options: category.children.map(metrics => ({
          label: metrics.label,
          value: metrics.value
        }))
      };
      });
  },
},
methods: {
    saveConfiguration() {
        for (let i = 0; i < this.savedConfigurations.length; i++) {
          if (this.savedConfigurations[i].compressor_id === '') {
            this.selectedSaveSlot = i;
  
            // Prepare early_config and compressor_config
            const early_config = {
              "pressio:metric": "composite",
              "composite:plugins": [...this.selectedMetrics],
            };
  
            const compressor_config = {
              "pressio:abs": this.bound,
            };
  
            this.savedConfigurations[this.selectedSaveSlot].compressor_id = this.compressor_id;
            this.savedConfigurations[this.selectedSaveSlot].early_config = early_config;
            this.savedConfigurations[this.selectedSaveSlot].compressor_config = compressor_config;
            this.showConfigWindow = true;
            this.$message.success(`Configuration saved to Save${i + 1}`);
            return;
          }
        }
        this.$message.error('All save slots are full. Please edit or delete a save slot to continue.');
      },

    confirmConfiguration() {
      this.$message.success('All configurations confirmed.');
      console.log("Configurations Confimed:", this.savedConfigurations);
    },
    showSavedConfig(slot) {
      this.selectedSaveSlot = slot;
      this.showConfigWindow = true;
    },
    editConfiguration() {
        this.compressor_id = this.savedConfigurations[this.selectedSaveSlot].compressor_id;
        this.bound = this.savedConfigurations[this.selectedSaveSlot].compressor_config['pressio:abs'];
        this.selectedMetrics = [...this.savedConfigurations[this.selectedSaveSlot].early_config['composite:plugins']];
    },
    cancelConfiguration() {
      this.showConfigWindow = false;
    },
    submitConfiguration() {
        const metricsSelected = Object.values(this.selectedMetrics).flat().length > 0;
        if (this.compressor_id.length === 0 || this.bound === null || !metricsSelected) {
          this.msg = this.$message.info({
            content: 'Invalid Input',
            theme: "warning",
            duration: 1000,
            zIndex: 1001,
            attach: document.body,
          });
        } else {
          this.loading = true;
          // this.formData = new FormData();

          const plainMetrics = [...this.selectedMetrics];
          console.log('Plain Metrics:', plainMetrics);

          const early_config = {
              "pressio:metric": "composite",
              "composite:plugins": this.selectedMetrics,
          };
          console.log('Early config metrics:', early_config);
          const compressor_config = {
              "pressio:abs": this.bound, // Use the bound provided by the user
          };

          console.log('Compressor ID:', this.compressor_id);
          console.log('Bound:', this.bound);
          console.log('Early Config:', early_config);
          console.log('Compressor Config:', compressor_config);
          // if(this.formData.has('compressor_id')){
          //     this.formData.delete('compressor_id');
          //   }
          this.formData.append('compressor_id', "sz");
          
          this.formData.append('early_config', JSON.stringify(early_config));
          this.formData.append('compressor_config', JSON.stringify(compressor_config));
          this.formData.append('bound', this.bound);
          this.formData.append('loaddata', this.loaddata);
          this.formData.append('slice_id', 0);
          // // this.formData.append('file', input_data);
          // console.log('Compressor ID1:', this.compressor_id);
          // console.log('Bound1:', this.bound);
          // console.log('Early Config1:', rawEarlyConfig);
          // console.log('Compressor Config1:', rawCompressorConfig);
          console.log("data transfer");
          // emitter.on('file-selected', (data) => {
          //   console.log("data", data);
          //   this.formData.append('file', data);

          // });
          
          // Append the file to formData
          // if (this.selectedFile) {
          //   this.formData.append('file', this.selectedFile);
          // } else {
          //   this.loading = false;
          //   console.log("exist");
          //   return;
          // }
  
          console.log('FormData before submission:', [...this.formData]);
          axios.post("http://" + this.host + ':' + String(this.port) + '/indexlist', this.formData)
            .then(response => {
              //let need1 = response.data;
              this.compare_data['compressor_id'].push(this.compressor_id);
              this.compare_data['bound'].push(response.data['output']['bound']);
              // Ensure you are only pushing the metrics returned from the backend
              if (response.data['output']['metrics']) {
                  this.compare_data['metrics'].push(response.data['output']['metrics']);
              } else {
                  console.warn("Metrics returned from the backend are null or undefined.");
              }

              //this.compare_data['metrics'].push(response.data['metrics']);
              //this.compare_data['metrics'].push(this.early_config);
             this.input_data = response.data['input_data'];
              console.log(this.input_data)
              document.getElementById('temp1').innerHTML = JSON.stringify(this.compare_data);
              emitter.emit('myEvent', this.compare_data);
              emitter.emit('inputdata', {"input_data":this.input_data, "width": this.width, "height":this.height, "depth":this.depth});
              
              this.loading = false;
            })
            .catch((error) => {
              this.loading = false;
              alert('illegal input');
              console.log(error);
            });

        }
        console.log('FormData after submission:', [...this.formData]);
      }
      
    },
    mounted() {
      emitter.on('file-selected', (data) => {
            console.log("datamounted", data);
            this.formData.append('file', data["file"]);
            this.formData.append('width', data["width"]);
            this.formData.append('height', data["height"]);
            this.formData.append('depth', data["depth"]);

          });
    },

    
  }
</script>
