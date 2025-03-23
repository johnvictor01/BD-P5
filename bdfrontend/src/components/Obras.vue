<template>
    <div>
      <div v-if="!Array.isArray(obras) || obras.length === 0">
        <p>Nenhuma obra disponível.</p>
      </div>
      <div v-else>
        <div class="imagens-container">
          <div v-for="(obra, index) in obras" :key="index" class="imagem-card">
            <img :src="obra.imagem || 'caminho/para/imagem-padrao.jpg'" :alt="obra.nome">
            <p>{{ obra.nome }}</p>
            <small>{{ obra.informacoes }}</small>
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
        default: () => [] // Valor padrão como array vazio
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
  </style>