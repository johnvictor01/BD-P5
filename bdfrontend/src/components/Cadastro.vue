<template>
    <div>
      <div v-if="type === 1" class="formsCliente">
        <FormsCadCliente/>
      </div>
      <div v-if="type === 2" class="formsAutor">
        <FormsCadAutor/>
      </div>
      <div v-if="type === 3" class="formsColaborator">
        <FormsCadColab/>
      </div>
      <!-- Adicione outros tipos de cadastro conforme necessário -->
    </div>
  </template>
  
  <script>
  import FormsCadCliente from './FormsCadCliente.vue';
  import FormsCadAutor from './FormsCadAutor.vue';
  import FormsCadColab from './FormsCadColab.vue';
  
  
  export default {
    name: 'Cadastro',
    components: {
      FormsCadCliente,
      FormsCadColab,
      FormsCadAutor
    },
    props: {
      type: {
        type: Number,
        default: 0
      }
    }
  }
  </script>
  
  <style scoped>


</style>