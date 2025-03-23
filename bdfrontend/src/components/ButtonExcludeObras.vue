<template>
    <div>
      <!-- Barra de Pesquisa -->
      <div class="search-bar">
        <input
          type="text"
          v-model="termoPesquisa"
          placeholder="Pesquisar obras..."
          @keyup.enter="pesquisarObras"
        />
        <button @click="pesquisarObras" class="btn-pesquisar">Pesquisar</button>
      </div>
  
      <!-- Lista de Obras -->
      <div class="obras-container">
        <div v-for="obra in obrasFiltradas" :key="obra.id" class="obra-card">
          <img :src="obra.imagem" :alt="obra.nome" />
          <p>{{ obra.nome }}</p>
          <small>{{ obra.informacoes }}</small>
          <button @click="excluirObra(obra.id)" class="btn-excluir">Excluir</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue';
  
  export default {
    name: 'ExcluirObras',
    setup() {
      // Dados fictícios de obras
      const obras = ref([
        {
          id: 1,
          imagem: 'https://via.placeholder.com/150',
          nome: 'Mona Lisa',
          informacoes: 'Uma das pinturas mais famosas de Leonardo da Vinci.',
        },
        {
          id: 2,
          imagem: 'https://via.placeholder.com/150',
          nome: 'A Noite Estrelada',
          informacoes: 'Obra-prima de Vincent van Gogh.',
        },
        {
          id: 3,
          imagem: 'https://via.placeholder.com/150',
          nome: 'O Grito',
          informacoes: 'Pintura expressionista de Edvard Munch.',
        },
        {
          id: 4,
          imagem: 'https://via.placeholder.com/150',
          nome: 'A Criação de Adão',
          informacoes: 'Afresco famoso de Michelangelo na Capela Sistina.',
        },
      ]);
  
      // Termo de pesquisa
      const termoPesquisa = ref('');
  
      // Filtra as obras com base no termo de pesquisa
      const obrasFiltradas = computed(() => {
        return obras.value.filter((obra) =>
          obra.nome.toLowerCase().includes(termoPesquisa.value.toLowerCase())
        );
      });
  
      // Método para pesquisar obras (pode ser expandido para chamar uma API)
      const pesquisarObras = () => {
        console.log('Pesquisando obras com o termo:', termoPesquisa.value);
      };
  
      // Método fictício para excluir uma obra
      const excluirObra = (id) => {
        console.log('Excluindo obra com ID:', id);
        obras.value = obras.value.filter((obra) => obra.id !== id);
      };
  
      return {
        termoPesquisa,
        obrasFiltradas,
        pesquisarObras,
        excluirObra,
      };
    },
  };
  </script>
  
  <style>
  .search-bar {
    display: flex;
    justify-content: center;
    margin: 20px 0;
  }
  
  .search-bar input {
    padding: 10px;
    width: 300px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-right: 10px;
  }
  
  .search-bar button {
    padding: 10px 20px;
    background-color: #2196f3;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .search-bar button:hover {
    background-color: #1e88e5;
  }
  
  .obras-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
  }
  
  .obra-card {
    width: 200px;
    text-align: center;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    background-color: white;
  }
  
  .obra-card img {
    width: 100%;
    height: auto;
    border-radius: 5px;
  }
  
  .obra-card p {
    font-weight: bold;
    margin: 10px 0 5px;
  }
  
  .obra-card small {
    font-size: 12px;
    color: gray;
  }
  
  .obra-card button {
    padding: 8px 12px;
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  .obra-card button:hover {
    background-color: #e53935;
  }
  </style>