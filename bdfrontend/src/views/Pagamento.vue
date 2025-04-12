<template>
  <div class="pagamento-container">
    <div class="resumo-compra">
      <h2>Resumo da Compra</h2>
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
          <span>R$ {{ formatarValor(subtotal) }}</span> <!-- Aqui pode adicionar taxas se necessário -->
        </div>
      </div>
    </div>
    
    <div class="metodos-pagamento">
      <TypePayment :total="subtotal" />
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import TypePayment from '../components/TypePayment.vue';

export default {
  name: 'Pagamento',
  components: {
    TypePayment
  },
  setup() {
    const router = useRouter();
    const itensCarrinho = ref([]);

    // Recupera os itens do carrinho do estado da rota
    onMounted(() => {
      if (router.currentRoute.value.state?.itensCarrinho) {
        itensCarrinho.value = router.currentRoute.value.state.itensCarrinho;
      } else {
        // Caso não tenha itens, pode redirecionar ou buscar de outra fonte
        console.warn('Nenhum item encontrado no carrinho');
      }
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

@media (max-width: 768px) {
  .pagamento-container {
    grid-template-columns: 1fr;
  }
}
</style>