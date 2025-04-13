<template>
  <div>
    <CabecalhoHome/>
    <MoreInformation/>
    <p>Abaixo os cadastros</p>
    <button class="Button" @click="type = (!type)">Deseja Cadastrar?</button>
    <FormsCadCliente v-if="type" />
    <Contacts/>
    <Footer/>
  </div>
</template>

<script>
import CabecalhoHome from '../components/CabecalhoHome.vue'
import MoreInformation from '../components/MoreInformation.vue'
import Contacts from '../components/Contacts.vue'
import Footer from '../components/Footer.vue'
import Cadastros from '../components/Cadastros.vue'
import FormsCadCliente from '../components/FormsCadCliente.vue'

export default {
  name: 'HomeView',
  data(){
    return{
      type: false
    }
  },
  components: {
    CabecalhoHome,
    MoreInformation,
    Contacts,
    Footer,
    Cadastros,
    FormsCadCliente
  }
}
</script>

<style >

button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #2980b9;
  }
</style>