<template>
  <div>
    <!-- Barra de Pesquisa -->
    <div class="search-bar">
      <input
        type="text"
        v-model="termoPesquisa"
        placeholder="Pesquisar obras..."
        @keyup.enter="carregarObras"
      />
      <button @click="carregarObras" class="btn-pesquisar">Pesquisar</button>
    </div>

    <!-- Lista de Obras -->
    <div v-if="carregando" class="carregando">Carregando obras...</div>
    <div v-else class="obras-container">
      <div v-for="obra in obrasFiltradas" :key="obra.id" class="obra-card">
        <img :src="`data:${obra.TipoArquivo};base64,${obra.Imagem}`" :alt="obra.nome" />
        <p>{{ obra.nome }}</p>
        <small>{{ obra.informacoes }}</small>
        <button @click="confirmarExclusao(obra.id)" class="btn-excluir">Excluir</button>
      </div>
    </div>

    <!-- Modal de Confirmação -->
    <div v-if="modalVisivel" class="modal">
      <div class="modal-content">
        <h3>Confirmar Exclusão</h3>
        <p>Tem certeza que deseja excluir esta obra permanentemente?</p>
        <div class="modal-actions">
          <button @click="excluirObra" class="btn-confirmar">Confirmar</button>
          <button @click="fecharModal" class="btn-cancelar">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'ExcluirObras',
  setup() {
    const obras = ref([]);
    const carregando = ref(false);
    const termoPesquisa = ref('');
    const modalVisivel = ref(false);
    const obraSelecionada = ref(null);

    // Carrega as obras do backend
    const carregarObras = async () => {
      carregando.value = true;
      try {
        const response = await axios.get('http://localhost:5000/obras'); // Você precisará criar este endpoint
        obras.value = response.data;
      } catch (error) {
        console.error('Erro ao carregar obras:', error);
        alert('Erro ao carregar obras');
      } finally {
        carregando.value = false;
      }
    };

    // Filtra as obras com base no termo de pesquisa
    const obrasFiltradas = computed(() => {
      return obras.value.filter((obra) =>
        obra.nome.toLowerCase().includes(termoPesquisa.value.toLowerCase())
      );
    });

    // Abre o modal de confirmação
    const confirmarExclusao = (id) => {
      obraSelecionada.value = id;
      modalVisivel.value = true;
    };

    // Fecha o modal
    const fecharModal = () => {
      modalVisivel.value = false;
      obraSelecionada.value = null;
    };

    // Método para excluir uma obra
    const excluirObra = async () => {
      if (!obraSelecionada.value) return;
      
      try {
        const response = await axios.post('http://localhost:5000/remover-obra', {
          id_obra: obraSelecionada.value
        });

        if (response.data.sucesso) {
          alert('Obra excluída com sucesso!');
          // Atualiza a lista de obras
          await carregarObras();
        }
      } catch (error) {
        console.error('Erro ao excluir obra:', error);
        alert('Erro ao excluir obra: ' + (error.response?.data?.erro || error.message));
      } finally {
        fecharModal();
      }
    };

    // Carrega as obras quando o componente é montado
    onMounted(() => {
      carregarObras();
    });

    return {
      termoPesquisa,
      obras,
      obrasFiltradas,
      carregando,
      modalVisivel,
      carregarObras,
      confirmarExclusao,
      fecharModal,
      excluirObra,
    };
  },
};
</script>

<style>
/* Seus estilos anteriores permanecem os mesmos */

/* Estilos adicionais para o modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn-confirmar {
  background-color: #f44336;
  color: white;
}

.btn-confirmar:hover {
  background-color: #e53935;
}

.btn-cancelar {
  background-color: #757575;
  color: white;
}

.btn-cancelar:hover {
  background-color: #616161;
}

.carregando {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

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