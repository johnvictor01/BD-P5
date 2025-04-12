<template>
  <div>
    <div v-if="carregando" class="carregando">Carregando obras...</div>
        <!-- Popup de aprovação -->
        <div v-if="mostrarPopup" class="popup-overlay">
      <Aprovede />
            </div>
    <div v-else>
      <div class="imagens-container">
        <div v-for="(obra, index) in obras" :key="index" class="imagem-card">
          <img
            :src="`data:${obra.TipoArquivo};base64,${obra.Imagem}`"
            :alt="obra.nome"
          />
          <p>{{ obra.nome }}</p>
          <small>{{ obra.informacoes }}</small>
          <div class="card-actions">
            <button @click="liberarObra(obra)" class="btn-autorizar">
              Autorizar Venda
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import Aprovede from "./Aprovede.vue";

export default {
  name: "ObrasPendentes",
  components: {
    Aprovede,
  },
  setup() {
    const obras = ref([]);
    const carregando = ref(true);
    const mostrarPopup = ref(false);


    const carregarObrasPendentes = async () => {
      try {
        const response = await axios.get(
          "http://localhost:5000/obras-pendentes-vendas"
        );
        obras.value = response.data;
      } catch (error) {
        console.error("Erro ao carregar obras:", error);
        alert("Erro ao carregar obras pendentes");
      } finally {
        carregando.value = false;
      }
    };

    const liberarObra = async (obra) => {
      try {
        const response = await axios.post(
          "http://localhost:5000/autorizar-venda",
          {
            id_obra: obra.id,
          },
          { withCredentials: true }
        );

        if (response.data.sucesso) {
          mostrarPopup.value = true;
          setTimeout(() => {
            mostrarPopup.value = false;
            carregarObrasPendentes();
          }, 5000); // tempo para mostrar a animação do círculo
        }
      } catch (error) {
        console.error("Erro ao autorizar venda:", error);
        alert(error.response?.data?.erro || "Erro ao autorizar venda");
      }
    };
    onMounted(() => {
      carregarObrasPendentes();
    });

    return {
      obras,
      carregando,
      liberarObra,
      
    };
  },
};
</script>

<style>
/* Seus estilos permanecem os mesmos */
.carregando {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

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
  max-height: 150px;
  object-fit: contain;
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
  justify-content: center;
  margin-top: 10px;
}

.btn-autorizar {
  padding: 8px 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-autorizar:hover {
  background-color: #45a049;
}
</style>
