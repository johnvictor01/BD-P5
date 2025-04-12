<template>
  <div class="pagamento-container">
    <div class="resumo-compra">
      <h2>Resumo da Compra</h2>
      <div v-if="carregando" class="carregando">Carregando itens do carrinho...</div>
      <div v-else>
        <div class="itens-lista">
          <div v-for="item in itensCarrinho" :key="item.ObraID" class="item-resumo">
            <span class="item-titulo">{{ item.Titulo }}</span>
            <span class="item-valor">R$ {{ formatarValor(item.Valor) }}</span>
          </div>
        </div>
        <div class="total-section">
          <div class="subtotal">
            <span>Subtotal:</span>
            <span>R$ {{ formatarValor(subtotal) }}</span>
          </div>
          <div class="total">
            <span>Total:</span>
            <span>R$ {{ formatarValor(subtotal) }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="metodos-pagamento">
      <TypePayment 
        :total="subtotal" 
        :itens="itensCarrinho" 
        :disabled="carregando || itensCarrinho.length === 0" 
      />
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import TypePayment from '../components/TypePayment.vue';

axios.defaults.withCredentials = true;

export default {
  name: 'Pagamento',
  components: {
    TypePayment
  },
  setup() {
    const router = useRouter();
    const itensCarrinho = ref([]);
    const carregando = ref(true);
    const erro = ref(null);

    // Função para carregar os itens do carrinho do backend
    const carregarCarrinho = async () => {
      try {
        carregando.value = true;
        const response = await axios.get('http://localhost:5000/recuperar-carrinho');
        
        if (response.data.sucesso) {
          // Filtra itens com valor definido e mapeia para o formato esperado
          itensCarrinho.value = response.data.itens
            .filter(item => item.valor !== null)
            .map(item => ({
              ObraID: item.ID,
              Titulo: item.Titulo,
              Valor: item.valor
            }));
          
          if (itensCarrinho.value.length === 0) {
            erro.value = 'Seu carrinho está vazio ou os itens não estão mais disponíveis';
          }
        }
      } catch (error) {
        console.error('Erro ao carregar carrinho:', error);
        if (error.response && error.response.status === 401) {
          erro.value = 'Sessão expirada. Por favor, faça login novamente.';
          router.push('/login');
        } else {
          erro.value = 'Falha ao carregar o carrinho. Tente novamente.';
        }
      } finally {
        carregando.value = false;
      }
    };

    // Tenta primeiro pegar do estado da rota (para experiência mais rápida)
    // Depois busca do servidor para garantir dados atualizados
    onMounted(() => {
      if (router.currentRoute.value.state?.itensCarrinho) {
        itensCarrinho.value = router.currentRoute.value.state.itensCarrinho;
      }
      carregarCarrinho();
    });

    // Calcula o subtotal
    const subtotal = computed(() => {
      return itensCarrinho.value.reduce((sum, item) => sum + (item.Valor || 0), 0);
    });

    // Formata valores monetários
    const formatarValor = (valor) => {
      return valor?.toFixed(2).replace('.', ',') || '0,00';
    };

    return {
      itensCarrinho,
      subtotal,
      carregando,
      erro,
      formatarValor
    };
  }
};
</script>

<style scoped>
.pagamento-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.resumo-compra {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.resumo-compra h2 {
  margin-bottom: 1.5rem;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.itens-lista {
  margin-bottom: 1.5rem;
}

.item-resumo {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px dashed #ddd;
}

.item-resumo:last-child {
  border-bottom: none;
}

.total-section {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 2px solid #eee;
}

.subtotal, .total {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.total {
  font-weight: bold;
  font-size: 1.1rem;
  margin-top: 1rem;
}

.metodos-pagamento {
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.carregando {
  padding: 1rem;
  text-align: center;
  color: #666;
}

.erro {
  color: #d32f2f;
  padding: 1rem;
  text-align: center;
  background: #ffebee;
  border-radius: 4px;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .pagamento-container {
    grid-template-columns: 1fr;
  }
}
</style>