<template>
  <div class="carrinho-container">
    <h2>Carrinho</h2>
    <div v-if="itens.length > 0">
      <div v-for="item in itens" :key="item.ObraID" class="item-carrinho">
        <p>{{ item.Titulo }} - R$ {{ item.Valor }}</p>
        <button @click="removerDoCarrinho(item.ObraID)" class="btn-remover">Remover</button>
      </div>
      <p><strong>Total:</strong> R$ {{ total }}</p>
      <button @click="irParaPagamento" class="btn-pagamento">Ir para Pagamento</button>
    </div>
    <div v-else>
      <p>O carrinho está vazio.</p>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// Configura o Axios para enviar cookies (necessário para a sessão)
axios.defaults.withCredentials = true;

export default {
  name: 'Carrinho',
  props: {
    itens: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const router = useRouter();

    // Calcula o total do carrinho
    const total = computed(() => {
      return props.itens.reduce((sum, item) => sum + (item.Valor || 0), 0);
    });

    // Remove um item do carrinho
    const removerDoCarrinho = (obraId) => {
      const index = props.itens.findIndex((item) => item.ObraID === obraId);
      if (index !== -1) {
        props.itens.splice(index, 1);
      }
    };

    const irParaPagamento = async () => {
      try {
        // Prepara os itens no formato esperado pelo backend (apenas ObraID)
        const itensParaEnviar = props.itens.map(item => ({ ObraID: item.ObraID }));
        
        // Envia os itens do carrinho para o backend
        const response = await axios.post('http://localhost:5000/salvar-carrinho', {
          itens: itensParaEnviar
        });

        // Se a requisição for bem-sucedida, navega para a página de pagamento
        if (response.data.sucesso) {
          router.push({ 
            name: 'Pagamento',
            // Passa os itens do carrinho via estado da rota
            state: { itensCarrinho: props.itens }
          });
        } else {
          alert('Erro ao salvar carrinho: ' + response.data.erro);
        }
      } catch (error) {
        console.error('Erro ao enviar carrinho:', error);
        if (error.response && error.response.status === 401) {
          alert('Sessão expirada. Faça login novamente.');
          router.push('/login');
        } else {
          alert('Falha ao processar o carrinho. Tente novamente.');
        }
      }
    };

    return {
      total,
      removerDoCarrinho,
      irParaPagamento,
    };
  },
};
</script>

<style>
/* Estilos permanecem os mesmos */
.carrinho-container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.item-carrinho {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.btn-remover {
  padding: 5px 10px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-remover:hover {
  background-color: #e53935;
}

.btn-pagamento {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

p {
  text-decoration: underline;
}

.btn-pagamento:hover {
  background-color: #45a049;
}
</style>