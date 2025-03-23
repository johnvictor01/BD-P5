<template>
  <div>
    <CabecalhoPessoa />
    <br>
    <br />
    <p>_</p>
    <!-- Passa obrasNaBiblio como prop para MyBiblio -->
    <MyBiblio v-if="obrasNaBiblio.length > 0" :obras="obrasNaBiblio" />
    <br>
    <br />
    <h1>Vamos às compras?</h1>
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
      loading: false
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
          alert("Nenhuma obra disponível.");
          this.obrasDisponiveis = [];  // Define o array de obras como vazio
        } else {
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
    await this.buscarUsuarioLogado(); // Aguarda a conclusão da requisição
    this.buscarObrasDisponiveis(); // Agora chama o método para buscar obras
  }
};
</script>

<style>
p{
  margin-top: 4rem;
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