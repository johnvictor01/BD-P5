<template>
  <div>
    <div v-if="carregando" class="carregando">Carregando obras...</div>
    
    <div v-else>
      <div class="imagens-container">
        <div v-for="(obra, index) in obras" :key="index" class="imagem-card">
          <img :src="`data:${obra.TipoArquivo};base64,${obra.Imagem}`" :alt="obra.nome">
          <p>{{ obra.nome }}</p>
          <small>{{ obra.informacoes }}</small>
          <div class="card-actions">
            <button @click="abrirModalAutorizacao(obra)" class="btn-autorizar">Autorizar</button>
          </div>
        </div>
      </div>

      <!-- Modal de Autorização -->
      <div v-if="modalVisivel" class="modal">
        <div class="modal-content">
          <h3>Autorizar Obra</h3>
          <p><strong>Título:</strong> {{ obraSelecionada.nome }}</p>
          <p><strong>Descrição:</strong> {{ obraSelecionada.informacoes }}</p>
          <p><strong>Autor:</strong> {{ obraSelecionada.autor }}</p>
          <label for="preco">Preço (R$):</label>
          <input type="number" id="preco" v-model="preco" placeholder="Digite o preço" step="0.01" min="0" />
          <div class="modal-actions">
            <button @click="liberarObra" class="btn-salvar">Liberar Obra</button>
            <button @click="fecharModal" class="btn-cancelar">Cancelar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'ObrasPendentes',
  setup() {
    const obras = ref([]);
    const carregando = ref(true);
    const modalVisivel = ref(false);
    const obraSelecionada = ref(null);
    const preco = ref(null);

    // Carrega as obras pendentes ao montar o componente
    const carregarObrasPendentes = async () => {
      try {
        const response = await axios.get('http://localhost:5000/obras-pendentes');
        obras.value = response.data;
      } catch (error) {
        console.error("Erro ao carregar obras:", error);
        alert("Erro ao carregar obras pendentes");
      } finally {
        carregando.value = false;
      }
    };

    // Abre o modal para autorização
    const abrirModalAutorizacao = (obra) => {
      obraSelecionada.value = obra;
      preco.value = obra.valor || null;
      modalVisivel.value = true;
    };

    const fecharModal = () => {
      modalVisivel.value = false;
      obraSelecionada.value = null;
      preco.value = null;
    };

    // Libera a obra no backend
    const liberarObra = async () => {
      if (!preco.value || preco.value <= 0) {
        alert("Por favor, insira um preço válido.");
        return;
      }

      try {
        const response = await axios.post('http://localhost:5000/liberar-obra', {
          id: obraSelecionada.value.id,
          valor: preco.value
        });

        if (response.data.sucesso) {
          alert("Obra liberada com sucesso!");
          // Atualiza a lista de obras
          await carregarObrasPendentes();
          fecharModal();
        }
      } catch (error) {
        console.error("Erro ao liberar obra:", error);
        alert("Erro ao liberar obra");
      }
    };

    // Carrega as obras quando o componente é montado
    onMounted(() => {
      carregarObrasPendentes();
    });

    return {
      obras,
      carregando,
      modalVisivel,
      obraSelecionada,
      preco,
      abrirModalAutorizacao,
      fecharModal,
      liberarObra
    };
  }
};
</script>

<style>
/* Seus estilos anteriores permanecem os mesmos */
.carregando {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

/* Adicione isso para melhorar a exibição de imagens base64 */
.imagem-card img {
  max-height: 150px;
  object-fit: contain;
}
</style>