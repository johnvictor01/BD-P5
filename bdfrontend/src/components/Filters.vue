<template>
  <div>
    <!-- Barra de Filtros -->
    <div class="filtros-container">
      <div class="filtro">
        <label for="tipoArte">Tipo de Arte:</label>
        <select id="tipoArte" v-model="filtros.tipoArte">
          <option value="">Todos</option>
          <option value="Visionista">Visionista</option>
          <option value="Paisagista">Paisagista</option>
        </select>
      </div>

      <div class="filtro">
        <label for="valor">Valor (R$):</label>
        <input
          type="range"
          id="valor"
          v-model="filtros.valor"
          :min="0"
          :max="10000"
          step="100"
        />
        <span>{{ filtros.valor }}</span>
      </div>

      <div class="filtro">
        <label for="nome">Pesquisar por Nome:</label>
        <input type="text" id="nome" v-model="filtros.nome" placeholder="Digite o nome" />
      </div>

      <div class="filtro">
        <label for="alturaMin">Altura Mínima (cm):</label>
        <input type="number" id="alturaMin" v-model="filtros.alturaMin" placeholder="Mínima" />
      </div>

      <div class="filtro">
        <label for="alturaMax">Altura Máxima (cm):</label>
        <input type="number" id="alturaMax" v-model="filtros.alturaMax" placeholder="Máxima" />
      </div>

      <div class="filtro">
        <label for="larguraMin">Largura Mínima (cm):</label>
        <input type="number" id="larguraMin" v-model="filtros.larguraMin" placeholder="Mínima" />
      </div>

      <div class="filtro">
        <label for="larguraMax">Largura Máxima (cm):</label>
        <input type="number" id="larguraMax" v-model="filtros.larguraMax" placeholder="Máxima" />
      </div>
    </div>

    <!-- Lista de Obras Filtradas -->
    <div class="obras-container">
      <div v-for="obra in obrasFiltradas" :key="obra.ObraID" class="obra-card">
        <img :src="obra.Imagem ? `data:${obra.TipoArquivo};base64,${obra.Imagem}` : 'https://via.placeholder.com/150?text=Sem+Imagem'" :alt="obra.Titulo" />        <h3>{{ obra.Titulo }}</h3>
        <p>{{ obra.Descricao }}</p>
        <small>Estilo: {{ obra.EstiloArte }}</small>
        <p><strong>Valor:</strong> R$ {{ parseFloat(obra.Valor).toFixed(2) }}</p>
        <p><strong>Altura:</strong> {{ obra.Altura }} cm</p>
        <p><strong>Largura:</strong> {{ obra.Largura }} cm</p>
        <button @click="adicionarAoCarrinho(obra)" class="btn-adicionar">Adicionar ao Carrinho</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
  name: 'Filters',
  props: {
    obras: {
      type: Array,
      required: true
    }
  },
  emits: ['adicionar-ao-carrinho'],
  setup(props, { emit }) {
    // Filtros
    const filtros = ref({
      tipoArte: '',
      valor: 10000, // Valor máximo inicial
      nome: '',
      alturaMin: null,
      alturaMax: null,
      larguraMin: null,
      larguraMax: null,
    });

    // Filtra as obras com base nos filtros aplicados
    const obrasFiltradas = computed(() => {
      return props.obras.filter((obra) => {
        const tipoArteMatch =
          !filtros.value.tipoArte || obra.EstiloArte === filtros.value.tipoArte;
        const valorMatch = parseFloat(obra.Valor) <= filtros.value.valor;
        const nomeMatch =
          !filtros.value.nome ||
          obra.Titulo.toLowerCase().includes(filtros.value.nome.toLowerCase());
        const alturaMatch =
          (!filtros.value.alturaMin || obra.Altura >= filtros.value.alturaMin) &&
          (!filtros.value.alturaMax || obra.Altura <= filtros.value.alturaMax);
        const larguraMatch =
          (!filtros.value.larguraMin || obra.Largura >= filtros.value.larguraMin) &&
          (!filtros.value.larguraMax || obra.Largura <= filtros.value.larguraMax);

        return (
          tipoArteMatch && valorMatch && nomeMatch && alturaMatch && larguraMatch
        );
      });
    });

    // Adiciona uma obra ao carrinho
    const adicionarAoCarrinho = (obra) => {
      console.log('Obra selecionada:', obra); // Depuração
      emit('adicionar-ao-carrinho', obra); // Emite o evento com a obra selecionada
    };

    return {
      filtros,
      obrasFiltradas,
      adicionarAoCarrinho,
    };
  },
};
</script>

<style>
.filtros-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 10px 0;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.filtro {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filtro label {
  font-weight: bold;
}

.filtro input,
.filtro select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
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

.btn-adicionar {
  padding: 8px 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.btn-adicionar:hover {
  background-color: #45a049;
}
</style>