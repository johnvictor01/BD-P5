<template>
    <div>
      <div class="imagens-container">
        <div v-for="(obra, index) in fakeObras" :key="index" class="imagem-card">
          <img :src="obra.imagem" :alt="obra.nome">
          <p>{{ obra.nome }}</p>
          <small>{{ obra.informacoes }}</small>
          <div class="card-actions">
            <button @click="abrirModalAutorizacao(obra)" class="btn-autorizar">Autorizar</button>
            <button @click="aplicarPreco(obra)" class="btn-preco">Aplicar Preço</button>
          </div>
        </div>
      </div>
  
      <!-- Modal de Autorização -->
      <div v-if="modalVisivel" class="modal">
        <div class="modal-content">
          <h3>Autorizar Obra</h3>
          <p><strong>Título:</strong> {{ obraSelecionada.nome }}</p>
          <p><strong>Descrição:</strong> {{ obraSelecionada.informacoes }}</p>
          <label for="preco">Preço (R$):</label>
          <input type="number" id="preco" v-model="preco" placeholder="Digite o preço" />
          <div class="modal-actions">
            <button @click="autorizarObra" class="btn-salvar">Autorizar</button>
            <button @click="fecharModal" class="btn-cancelar">Cancelar</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    name: 'Obras',
    setup() {
      const fakeObras = ref([
        {
          id: 1,
          imagem: 'https://via.placeholder.com/150',
          nome: 'Mona Lisa',
          informacoes: 'Uma das pinturas mais famosas de Leonardo da Vinci.',
          autor: 'Leonardo da Vinci',
          dataPublicacao: '1503-01-01',
          estilo: 'Renascimento',
          paisGaleria: 'FRA',
          altura: 77,
          largura: 53,
        },
        {
          id: 2,
          imagem: 'https://via.placeholder.com/150',
          nome: 'A Noite Estrelada',
          informacoes: 'Obra-prima de Vincent van Gogh.',
          autor: 'Vincent van Gogh',
          dataPublicacao: '1889-01-01',
          estilo: 'Pós-Impressionismo',
          paisGaleria: 'NLD',
          altura: 73.7,
          largura: 92.1,
        },
        {
          id: 3,
          imagem: 'https://via.placeholder.com/150',
          nome: 'O Grito',
          informacoes: 'Pintura expressionista de Edvard Munch.',
          autor: 'Edvard Munch',
          dataPublicacao: '1893-01-01',
          estilo: 'Expressionismo',
          paisGaleria: 'NOR',
          altura: 91,
          largura: 73.5,
        },
      ]);
  
      const modalVisivel = ref(false);
      const obraSelecionada = ref(null);
      const preco = ref(null);
  
      const abrirModalAutorizacao = (obra) => {
        obraSelecionada.value = obra;
        modalVisivel.value = true;
      };
  
      const fecharModal = () => {
        modalVisivel.value = false;
        obraSelecionada.value = null;
        preco.value = null;
      };
  
      const autorizarObra = () => {
        if (preco.value) {
          console.log("Obra autorizada:", obraSelecionada.value);
          console.log("Preço aplicado:", preco.value);
          fecharModal();
        } else {
          alert("Por favor, insira um preço.");
        }
      };
  
      const aplicarPreco = (obra) => {
        abrirModalAutorizacao(obra);
      };
  
      return {
        fakeObras,
        modalVisivel,
        obraSelecionada,
        preco,
        abrirModalAutorizacao,
        fecharModal,
        autorizarObra,
        aplicarPreco,
      };
    },
  };
  </script>
  
  <style>
  .imagens-container {
    margin-top: 4rem;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
  }
  
  .imagem-card {
    width: 200px;
    text-align: center;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    background-color: white;
  }
  
  .imagem-card img {
    width: 100%;
    height: auto;
    border-radius: 5px;
  }
  
  .imagem-card p {
    font-weight: bold;
    margin: 10px 0 5px;
  }
  
  .imagem-card small {
    font-size: 12px;
    color: gray;
  }
  
  .card-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }
  
  button {
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }
  
  .btn-autorizar {
    background-color: #4CAF50;
    color: white;
  }
  
  .btn-autorizar:hover {
    background-color: #45a049;
  }
  
  .btn-preco {
    background-color: #2196F3;
    color: white;
  }
  
  .btn-preco:hover {
    background-color: #1e88e5;
  }
  
  /* Estilos do Modal */
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
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 400px;
  }
  
  .modal-content h3 {
    margin-top: 0;
  }
  
  .modal-content label {
    display: block;
    margin: 10px 0 5px;
  }
  
  .modal-content input {
    width: 100%;
    padding: 8px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }
  
  .btn-salvar {
    background-color: #4CAF50;
    color: white;
  }
  
  .btn-salvar:hover {
    background-color: #45a049;
  }
  
  .btn-cancelar {
    background-color: #f44336;
    color: white;
  }
  
  .btn-cancelar:hover {
    background-color: #e53935;
  }
  </style>