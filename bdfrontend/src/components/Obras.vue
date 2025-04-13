<template>
  <div>
    <div v-if="!Array.isArray(obras) || obras.length === 0">
      <p>Nenhuma obra disponível.</p>
    </div>
    <div v-else>
      <div class="imagens-container">
        <div 
          v-for="(obra, index) in obras" 
          :key="index" 
          class="imagem-card"
          @click="abrirModal(obra)"
        >
          <img :src="obra.imagem || 'caminho/para/imagem-padrao.jpg'" :alt="obra.nome">
          <p>{{ obra.nome }}</p>
          <small>{{ obra.informacoes }}</small>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="modalAberto" class="modal-overlay" @click.self="fecharModal">
      <div class="modal-content">
        <button class="modal-close" @click="fecharModal">&times;</button>
        <div class="modal-body">
          <div class="modal-imagem-container">
            <img :src="obraSelecionada.imagem || 'caminho/para/imagem-padrao.jpg'" :alt="obraSelecionada.nome">
          </div>
          <div class="modal-info">
            <h2>{{ obraSelecionada.nome }}</h2>
            <p class="descricao">{{ obraSelecionada.informacoes }}</p>
            <div v-if="obraSelecionada.autor" class="info-extra">
              <p><strong>Autor:</strong> {{ obraSelecionada.autor }}</p>
            </div>
            <div class="compra-message">
              <p>Cadastre-se para adquirir esta obra!</p>
              <button class="btn-cadastro" @click="irParaCadastro">Quero me cadastrar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Obras',
  props: {
    obras: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  data() {
    return {
      modalAberto: false,
      obraSelecionada: null
    }
  },
  methods: {
    abrirModal(obra) {
      this.obraSelecionada = obra;
      this.modalAberto = true;
      document.body.style.overflow = 'hidden'; // Impede scroll da página principal
    },
    fecharModal() {
      this.modalAberto = false;
      document.body.style.overflow = 'auto'; // Restaura scroll da página principal
    },
    irParaCadastro() {
      this.$emit('cadastrar');
      this.fecharModal();
    }
  }
};
</script>

<style scoped>
.imagens-container {
  margin-top: 70px;
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
  cursor: pointer;
  transition: transform 0.3s ease;
}

.imagem-card:hover {
  transform: scale(1.05);
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

/* Estilos do Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 10px;
  width: 80%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  padding: 20px;
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
}

.modal-body {
  display: flex;
  gap: 30px;
}

.modal-imagem-container {
  flex: 1;
}

.modal-imagem-container img {
  width: 100%;
  max-height: 70vh;
  object-fit: contain;
  border-radius: 8px;
}

.modal-info {
  flex: 1;
  text-align: left;
}

.modal-info h2 {
  margin-top: 0;
  color: #2c3e50;
}

.descricao {
  margin: 20px 0;
  line-height: 1.6;
}

.info-extra {
  margin: 20px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.compra-message {
  margin-top: 30px;
  padding: 20px;
  background-color: #e8f4fd;
  border-radius: 8px;
  text-align: center;
}

.btn-cadastro {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 15px;
}

.btn-cadastro:hover {
  background-color: #2980b9;
}

/* Responsividade */
@media (max-width: 768px) {
  .modal-body {
    flex-direction: column;
  }
  
  .modal-content {
    width: 95%;
  }
}
</style>