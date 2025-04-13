<template>
  <div>
    <!-- Barra de Filtros -->
    <div class="filtros-container">
      <div 
        v-for="(filtro, index) in filtrosConfig" 
        :key="index" 
        class="filtro"
        :class="{'filtro-range': filtro.type === 'range'}"
      >
        <label :for="filtro.id">{{ filtro.label }}:</label>
        
        <!-- Input de seleção -->
        <select 
          v-if="filtro.type === 'select'" 
          :id="filtro.id" 
          v-model="filtrosValues[filtro.model]"
        >
          <option value="">Todos</option>
          <option 
            v-for="(opcao, i) in filtro.options" 
            :key="i" 
            :value="opcao.value"
          >
            {{ opcao.text }}
          </option>
        </select>
        
        <!-- Input de range -->
        <div v-else-if="filtro.type === 'range'" class="range-container">
          <input
            type="range"
            :id="filtro.id"
            v-model="filtrosValues[filtro.model]"
            :min="filtro.min"
            :max="filtro.max"
            :step="filtro.step"
          />
          <span class="range-value">{{ formatarValor(filtrosValues[filtro.model], filtro.format) }}</span>
        </div>
        
        <!-- Input de texto/número -->
        <input
          v-else
          :type="filtro.type"
          :id="filtro.id"
          v-model="filtrosValues[filtro.model]"
          :placeholder="filtro.placeholder"
          :min="filtro.min"
          :max="filtro.max"
        />
      </div>
    </div>

    <!-- Lista de Obras Filtradas -->
    <div class="obras-container">
      <div v-for="obra in obrasFiltradas" :key="obra.ObraID" class="obra-card">
        <img :src="obra.Imagem ? `data:${obra.TipoArquivo};base64,${obra.Imagem}` : 'https://via.placeholder.com/150?text=Sem+Imagem'" :alt="obra.Titulo" />
        <h3>{{ obra.Titulo }}</h3>
        <p class="descricao">{{ obra.Descricao }}</p>
        <div class="detalhes-obra">
          <p><strong>Estilo:</strong> {{ obra.EstiloArte }}</p>
          <p><strong>Valor:</strong> R$ {{ formatarValor(obra.Valor, 'moeda') }}</p>
          <p><strong>Dimensões:</strong> {{ obra.Altura }}cm × {{ obra.Largura }}cm</p>
        </div>
        <button @click="adicionarAoCarrinho(obra)" class="btn-adicionar">
          <i class="fas fa-cart-plus"></i> Adicionar
        </button>
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
    // Configuração dos filtros
    const filtrosConfig = [
      {
        id: 'tipoArte',
        label: 'Tipo de Arte',
        model: 'tipoArte',
        type: 'select',
         options: [
          { value: 'Expressionismo', text: 'Expressionismo' },
          { value: 'Abstrato', text: 'Abstrato' },
          { value: 'Realismo', text: 'Realismo' },
          { value: 'Surrealismo', text: 'Surrealismo' },
          { value: 'Cubismo', text: 'Cubismo' },
          { value: 'Impressionismo', text: 'Impressionismo' },
          { value: 'Pós-Impressionismo', text: 'Pós-Impressionismo' },
          { value: 'Fauvismo', text: 'Fauvismo' },
          { value: 'Futurismo', text: 'Futurismo' },
          { value: 'Dadaísmo', text: 'Dadaísmo' },
          { value: 'Construtivismo', text: 'Construtivismo' },
          { value: 'Bauhaus', text: 'Bauhaus' },
          { value: 'De Stijl', text: 'De Stijl' },
          { value: 'Pop Art', text: 'Pop Art' },
          { value: 'Op Art', text: 'Op Art' },
          { value: 'Minimalismo', text: 'Minimalismo' },
          { value: 'Arte Conceitual', text: 'Arte Conceitual' },
          { value: 'Hiperrealismo', text: 'Hiperrealismo' },
          { value: 'Street Art', text: 'Street Art' },
          { value: 'Arte Digital', text: 'Arte Digital' },
          { value: 'Visionista', text: 'Visionista' },
          { value: 'Paisagista', text: 'Paisagista' },
          { value: 'Retratista', text: 'Retratista' },
          { value: 'Barroco', text: 'Barroco' },
          { value: 'Rococó', text: 'Rococó' },
          { value: 'Neoclassicismo', text: 'Neoclassicismo' },
          { value: 'Romantismo', text: 'Romantismo' },
          { value: 'Academicismo', text: 'Academicismo' },
          { value: 'Pré-Rafaelitas', text: 'Pré-Rafaelitas' },
          { value: 'Simbolismo', text: 'Simbolismo' },
          { value: 'Art Nouveau', text: 'Art Nouveau' },
          { value: 'Art Déco', text: 'Art Déco' }
        ]
      },
      {
        id: 'valor',
        label: 'Valor Máximo',
        model: 'valor',
        type: 'range',
        min: 0,
        max: 1000000,
        step: 100,
        format: 'moeda'
      },
      {
        id: 'nome',
        label: 'Pesquisar',
        model: 'nome',
        type: 'text',
        placeholder: 'Digite o nome'
      },
      {
        id: 'alturaMin',
        label: 'Altura Mínima',
        model: 'alturaMin',
        type: 'number',
        placeholder: 'Mínima (cm)',
        min: 0
      },
      {
        id: 'alturaMax',
        label: 'Altura Máxima',
        model: 'alturaMax',
        type: 'number',
        placeholder: 'Máxima (cm)',
        min: 0
      },
      {
        id: 'larguraMin',
        label: 'Largura Mínima',
        model: 'larguraMin',
        type: 'number',
        placeholder: 'Mínima (cm)',
        min: 0
      },
      {
        id: 'larguraMax',
        label: 'Largura Máxima',
        model: 'larguraMax',
        type: 'number',
        placeholder: 'Máxima (cm)',
        min: 0
      }
    ];

    // Valores dos filtros
    const filtrosValues = ref({
      tipoArte: '',
      valor: 5000,
      nome: '',
      alturaMin: null,
      alturaMax: null,
      larguraMin: null,
      larguraMax: null,
    });

    // Função para formatar valores
    const formatarValor = (valor, tipo) => {
      if (tipo === 'moeda') {
        return parseFloat(valor).toFixed(2).replace('.', ',');
      }
      return valor;
    };

    // Filtra as obras com base nos filtros aplicados
    const obrasFiltradas = computed(() => {
      return props.obras.filter((obra) => {
        return (
          (!filtrosValues.value.tipoArte || obra.EstiloArte === filtrosValues.value.tipoArte) &&
          parseFloat(obra.Valor) <= filtrosValues.value.valor &&
          (!filtrosValues.value.nome || obra.Titulo.toLowerCase().includes(filtrosValues.value.nome.toLowerCase())) &&
          (!filtrosValues.value.alturaMin || obra.Altura >= filtrosValues.value.alturaMin) &&
          (!filtrosValues.value.alturaMax || obra.Altura <= filtrosValues.value.alturaMax) &&
          (!filtrosValues.value.larguraMin || obra.Largura >= filtrosValues.value.larguraMin) &&
          (!filtrosValues.value.larguraMax || obra.Largura <= filtrosValues.value.larguraMax)
        );
      });
    });

    // Adiciona uma obra ao carrinho
    const adicionarAoCarrinho = (obra) => {
      emit('adicionar-ao-carrinho', obra);
    };

    return {
      filtrosConfig,
      filtrosValues,
      obrasFiltradas,
      adicionarAoCarrinho,
      formatarValor
    };
  },
};
</script>

<style scoped>
.filtros-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin: 20px 0;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}

.filtro {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filtro label {
  font-weight: 600;
  color: #343a40;
  font-size: 0.9rem;
}

.filtro input,
.filtro select {
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: border-color 0.3s;
}

.filtro input:focus,
.filtro select:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.filtro-range {
  grid-column: span 2;
}

.range-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.range-container input[type="range"] {
  flex: 1;
  height: 8px;
  cursor: pointer;
}

.range-value {
  min-width: 60px;
  text-align: right;
  font-weight: 500;
}

.obras-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 25px;
  margin-top: 30px;
}

.obra-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.obra-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.obra-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-bottom: 1px solid #eee;
}

.obra-card h3 {
  margin: 15px 15px 5px;
  font-size: 1.1rem;
  color: #212529;
}

.descricao {
  margin: 0 15px 10px;
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.4;
}

.detalhes-obra {
  padding: 0 15px;
  margin-bottom: 15px;
}

.detalhes-obra p {
  margin: 5px 0;
  font-size: 0.85rem;
  color: #495057;
}

.btn-adicionar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: calc(100% - 30px);
  margin: 0 15px 15px;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-adicionar:hover {
  background-color: #218838;
}

.btn-adicionar i {
  font-size: 0.9rem;
}

/* Responsividade */
@media (max-width: 768px) {
  .filtros-container {
    grid-template-columns: 1fr;
  }
  
  .filtro-range {
    grid-column: span 1;
  }
  
  .obras-container {
    grid-template-columns: 1fr;
  }
}
</style>