<template>
  <div>
    <CabecalhoPessoa :tipoUsuario="1" />
    <br>
    <br />
    <!-- Passa obrasNaBiblio como prop para MyBiblio -->
    <MyBiblio v-if="obrasNaBiblio.length > 0" :obras="obrasNaBiblio" />

    <br>
    <br />
    <div>
    <h1 v-if=" compra === false" >Vamos às compras?</h1>
    <p>Com base em seus dados recomendamos a você artes  do tipo: <p class="REC">{{ this.recomendacoes }}</p></p> 
    <p v-if="compra === true" style="color: red; font-size: 1.5rem;">Ops... parece que não tem nenhuma obra disponivel
       para compra no momento!</p>
  </div>
    <div class="Filtros">
      <Filters :obras="obrasDisponiveis" @adicionar-ao-carrinho="adicionarAoCarrinho" />
    </div>
    <div class="Carrinho">
      <Carrinho :itens="itensCarrinho" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import CabecalhoPessoa from '../components/CabecalhoPessoa.vue';
import Filters from '../components/Filters.vue';
import Carrinho from '../components/Carrinho.vue';
import MyBiblio from '../components/MyBiblio.vue';

// Configura o Axios para enviar cookies
axios.defaults.withCredentials = true;

export default {
  name: 'ClientView',
  components: {
    CabecalhoPessoa,
    Filters,
    Carrinho,
    MyBiblio,
  },
  data() {
    return {
      usuarioLogado: null,
      itensCarrinho: [],
      obrasDisponiveis: [], // Armazena as obras disponíveis
      obrasNaBiblio: [], // Armazena as obras da biblioteca
      loading: false,
      compra : true,
      recomendacoes: ""
    };
  },
  methods: {
    async buscarUsuarioLogado() {
      try {
        const response = await axios.get('http://localhost:5000/usuario-logado');
        console.log('Dados do usuário logado:', response.data);  // Depuração
        this.usuarioLogado = response.data;
        console.log('Usuario logado:', this.usuarioLogado);  // Depuração
      } catch (error) {
        console.error('Erro ao buscar dados do usuário:', error);
        alert("Erro ao buscar dados do usuário. Tente novamente.");
        this.$router.push('/LoginClient');  // Redireciona para a página de login em caso de erro
      }
    },
    async buscarRecomendacoes() {
  try {
    const response = await axios.get('http://localhost:5000/recomendacao-cliente-logado');
    console.log("Recomendações recebidas:", response.data);
    this.recomendacoes = response.data.RecomendacoesTexto
    ;
  } catch (error) {
    console.error('Erro ao buscar recomendações:', error);
    this.recomendacoes = "Nenhuma recomendação disponível.";
  }
},


    async buscarObrasDisponiveis() {
      if (!this.usuarioLogado) {
        alert("Usuário não autenticado.");
        this.$router.push('/LoginClient');  // Redireciona para a página de login
        return;
      }
      
      this.loading = true;
      try {
        // Busca as obras disponíveis (não precisa mais passar a matrícula na URL)
        const responseDisponiveis = await axios.get('http://localhost:5000/obras-disponiveis');
        console.log('Obras disponíveis:', responseDisponiveis.data);  // Depuração

        if (responseDisponiveis.data.length === 0) {
          this.obrasDisponiveis = [];  // Define o array de obras como vazio
        } else {
          this.compra = false
          this.obrasDisponiveis = responseDisponiveis.data;
        }

        // Busca as obras da biblioteca (não precisa mais passar a matrícula na URL)
        const responseBiblio = await axios.get('http://localhost:5000/obras-biblio');
        console.log('Obras na biblioteca:', responseBiblio.data);  // Depuração

        if (responseBiblio.data.length === 0) {
          alert("Nenhuma obra na biblioteca.");
          this.obrasNaBiblio = [];  // Define o array de obras como vazio
        } else {
          this.obrasNaBiblio = responseBiblio.data;
        }
      } catch (error) {
        console.error('Erro ao buscar obras:', error);
        if (error.response && error.response.status === 401) {
          alert("Usuário não autenticado ou sessão expirada.");
          this.$router.push('/LoginClient');  // Redireciona para a página de login
        } else {
          alert("Erro ao carregar as obras.");
        }
      } finally {
        this.loading = false;
      }
    },

    adicionarAoCarrinho(obra) {
      const itemExistente = this.itensCarrinho.find((item) => item.ObraID === obra.ObraID);
      if (!itemExistente) {
        this.itensCarrinho.push(obra);
      } else {
        alert("Este item já está no carrinho.");
      }
    }
  },
  async mounted() {
    await this.buscarUsuarioLogado(); 
    await this.buscarRecomendacoes();  
    this.buscarObrasDisponiveis(); 
  }
};
</script>

<style>
p{
  margin-top: 4rem;
  text-decoration: none;

}
p .REC{
  color: #FF5733; /* Cor laranja para o texto "recomendado" */
  font-weight: bold; /* Negrito para o texto "recomendado" */
  font-size: 1.5rem; /* Aumenta o tamanho da fonte */
  text-decoration: underline; /* Sublinha o texto "recomendado" */
}
.Filtros {
  margin-top: 2rem;
}

.Carrinho {
  margin-top: 2rem;
}

/* Estilo para mostrar um carregamento visual */
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

h1 {
  margin-top: 4rem;
}
</style>