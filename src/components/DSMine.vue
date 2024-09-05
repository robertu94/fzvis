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
        <t-select id='compressor-select' v-model="compressor_id" :options="compressorOptions" label="Compressor:" />
        <t-input v-model="bound" label="Bound:" placeholder="bound" />
        </div>
        <!--<t-select id='compressor-select' v-model="compressor_id" :options="compressorOptions" label="Compressor Name:" />-->
        <div id="metric-selection" :class="closed">
        <t-cascader v-model="selectedMetrics" :options="compressorMetrics" multiple label="Select Metrics:"
          placeholder="Select Compressor Metrics" :popup-props="{ trigger: 'click'}"/> 
        </div>
        <div class="button-group2">
          <t-button @click="saveConfiguration">Save <br> Configuration</t-button>
          <t-button @click="confirmConfiguration">Confirm <br> Configuration</t-button>
          <t-button id='update_button' @click="submitConfiguration">Submit</t-button>
        </div>
        <div v-if="showConfigWindow" class="config-window">
          <h4> Saved Configuration </h4>
          <p><strong> Compressor ID: </strong>{{ savedConfigurations[selectedSaveSlot].compressor_id }}</p>
          <p><strong> Bound: </strong>{{ savedConfigurations[selectedSaveSlot].compressor_config['pressio:abs'] }}</p>
          <p><strong> Metrics: </strong>{{ savedConfigurations[selectedSaveSlot].early_config['composite:plugins'].join(', ') }}</p>
          <t-button @click="editConfiguration">Edit</t-button>
          <t-button @click="cancelConfiguration">Cancel</t-button>
        </div>
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
        host:config.API_HOST,
        port:config.API_PORT,
        loading:false,
        compressor_id:'',
        bound:null,
        input_data:null,
        msg:'',
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
          label: 'Composite',
          children: [
            { label: 'Compression Rate', value: 'compression_rate' },
            { label: 'Compression Rate Many', value: 'compression_rate_many' },
            { label: 'Decompression Rate', value: 'decompression_rate' },
            { label: 'Decompression Rate Many', value: 'decompression_rate_many' }
          ]
        },
        {
          label: 'Error Stat',
          children: [
            { label: 'Average Difference', value: 'average_difference' },
            { label: 'Average Error', value: 'average_error' },
            { label: 'Difference Range', value: 'difference_range' },
            { label: 'Error Range', value: 'error_range' },
            { label: 'Max Error', value: 'max_error' },
            { label: 'Max REL Error', value: 'max_rel_error' },
            { label: 'Min Error', value: 'min_error' },
            { label: 'Min REL Error', value: 'min_rel_error' },
            { label: 'MSE', value: 'mse' },
            { label: 'N', value: 'n' },
            { label: 'PSNR', value: 'psnr' },
            { label: 'RMSE', value: 'rmse' },
            { label: 'Value Max', value: 'value_max' },
            { label: 'Value Mean', value: 'value_mean' },
            { label: 'Value Min', value: 'value_min' },
            { label: 'Value Range', value: 'value_range' },
            { label: 'Value STD', value: 'value_std' }
          ]
        },
        {
          label: 'Size',
          children: [
            { label: 'Bit Rate', value: 'bit_rate' },
            { label: 'Compressed Size', value: 'compressed_size' },
            { label: 'Compression Ratio', value: 'compression_ratio' },
            { label: 'De-Compressed Size', value: 'decompressed_size' },
            { label: 'Un-Compressed Size', value: 'uncompressed_size' }
          ]
        },
        {
          label: 'Time',
          children: [
            { label: 'Check Options', value: 'check_options' },
            { label: 'Compress', value: 'compress' },
            { label: 'Compress Many', value: 'compress_many' },
            { label: 'Decompress', value: 'decompress' },
            { label: 'De-Compress Many', value: 'decompress_many' },
            { label: 'Get Options', value: 'get_options' },
            { label: 'Set Options', value: 'set_options' }
          ]
        }
      ],
    };   
  },
  computed: {
    flattenedCompressorMetrics() {
        return this.compressorMetrics.map(category => {
        return {
          label: category.label,
          options: category.children.map(metric => ({
            label: metric.label,
            value: metric.value
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
                "composite:plugins": this.selectedMetrics,
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
            this.formData = new FormData();
            console.log('Compressor ID:', this.compressor_id);
            console.log('Bound:', this.bound);
            console.log('Early Config:', this.savedConfigurations.map(config => config.early_config));
            console.log('Compressor Config:', this.savedConfigurations.map(config => config.compressor_config));
            
            this.formData.append('compressor_id', this.compressor_id);
            this.formData.append('early_config', JSON.stringify(this.savedConfigurations.map(config => config.early_config)));
            this.formData.append('compressor_config', JSON.stringify(this.savedConfigurations.map(config => config.compressor_config)));
            this.formData.append('loaddata', this.loaddata);
            this.formData.append('slice_id', 0);
    
            console.log(this.formData);
            axios.post("http://" + this.host + ':' + String(this.port) + '/indexlist', this.formData)
              .then(response => {
                let need1 = response.data;
                console.log('C-error part', typeof (need1));
                this.compare_data['compressor_id'].push(this.compressor_id);
                this.compare_data['bound'].push(need1['bound']);
                this.compare_data['metrics'].push(need1['metrics']);
                this.compare_data['input_data'] = this.input_data;
                document.getElementById('temp1').innerHTML = JSON.stringify(this.compare_data);
                emitter.emit('myEvent', this.compare_data);
                this.loading = false;
              })
              .catch((error) => {
                this.loading = false;
                alert('illegal input');
                console.log(error);
              });
          }
        }  
      }
    }
  </script>
  