<template>
    <div class="more-information">
      <h1>Destaques das nossas obras de arte</h1>
      <Obras :obras="obras" @cadastrar="$emit('cadastrar')"/>
    </div>
  </template>
  
  <script>
  import Obras from '../components/Obras.vue'
  
  export default {
    name: 'MoreInformation',
    props: {
      obras: {
        type: Array,
        required: true,
        default: () => []
      }
    },
    components: {
      Obras
    }
  }
  </script>
  
  <style scoped>
  .more-information {
    margin-top: 8rem;
    text-align: center;
    margin-bottom: 20px;
  }
  
  h1 {
    margin-bottom: 2rem;
  }
  </style>