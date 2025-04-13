<template>
  <div>
    <CabecalhoHome/>
    <MoreInformation :obras="obrasFormatadas" @cadastrar="scrollToCadastro"/>
    
    <button class="Button" @click="scrollToCadastro">Cadastre-se e começe a comprar!</button>
    <FormsCadCliente v-if="type" ref="cadastroForm" :highlight="highlightCadastro"/>
    <Contacts/>
    <Footer/>
  </div>
</template>

<script>
import CabecalhoHome from '../components/CabecalhoHome.vue'
import MoreInformation from '../components/MoreInformation.vue'
import Contacts from '../components/Contacts.vue'
import Footer from '../components/Footer.vue'
import FormsCadCliente from '../components/FormsCadCliente.vue'
import axios from 'axios'

export default {
  name: 'HomeView',
  data() {
    return {
      type: false,
      obras: [],
      highlightCadastro: false  // Adicionado esta linha
    }
  },
  components: {
    CabecalhoHome,
    MoreInformation,
    Contacts,
    Footer,
    FormsCadCliente
  },
  computed: {
    obrasFormatadas() {
      return this.obras.map(obra => ({
        imagem: obra.Imagem ? `data:${obra.TipoArquivo};base64,${obra.Imagem}` : 'caminho/para/imagem-padrao.jpg',
        nome: obra.nome,
        informacoes: obra.informacoes
      }));
    }
  },
  methods: {  // Corrigido - movido o scrollToCadastro para dentro de methods
    async carregarObras() {
      try {
        const response = await axios.get('http://localhost:5000/obras');
        this.obras = response.data;
      } catch (error) {
        console.error('Erro ao carregar obras:', error);
      }
    },
    scrollToCadastro() {
      this.type = true; // Garante que o formulário está visível
      
      this.$nextTick(() => {
        // Adiciona classe de destaque
        this.highlightCadastro = true;
        
        // Rola até o formulário
        const element = this.$refs.cadastroForm.$el;
        element.scrollIntoView({ behavior: 'smooth' });
        
        // Remove o destaque após 3 segundos
        setTimeout(() => {
          this.highlightCadastro = false;
        }, 3000);
      });
    }
  },
  created() {
    this.carregarObras();
  }
}
</script>

<style>
button {
  margin-top: 45px;
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

.obras-section {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.obras-section h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

/* Adicione isso para garantir que o scroll suave funcione em todos os navegadores */
html {
  scroll-behavior: smooth;
}
</style>