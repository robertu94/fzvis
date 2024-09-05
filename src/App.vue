<template>
  <InputDataset />
  <StatA />
  <!-- <ParaMeter /> -->
  <DataVis />
  <DataSelection />
</template>

<script>

import StatA from './components/StatA.vue'
// import ParaMeter from './components/ParaMeter.vue'
import DataVis from './components/DataVis.vue'
import DataSelection from './components/DataSelection.vue'
import InputDataset from './components/InputDataset.vue'
export default {
  name: 'App',
  
  components: {
    InputDataset,
    StatA,
    // ParaMeter,
    DataVis,
    DataSelection
  },
  
}
</script>
<style>
html,body,#app{
  height: 100%;
  background-color:lightgrey;
}
</style>
