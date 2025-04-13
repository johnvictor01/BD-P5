<template>
  <div>
    <CabecalhoPessoa />
    <div class="payment-container">
      <h2>Finalize sua Compra</h2>
      
      <!-- Formulário de Identificação -->
      <div class="identity-form" v-if="!identityConfirmed">
        <h3>Para oferecer as melhores condições:</h3>
        <div class="form-group">
          <label>Qual seu time do coração?</label>
          <input type="text" v-model="userIdentity.time" placeholder="Ex: Flamengo, Vasco...">
        </div>
        <div class="form-group">
          <label>
            <input type="checkbox" v-model="userIdentity.assisteOnePiece"> 
            Sou fã de One Piece
          </label>
        </div>
        <div class="form-group">
          <label>
            <input type="checkbox" v-model="userIdentity.ehDeSousa"> 
            Sou de Sousa-PB
          </label>
        </div>
        <button @click="confirmIdentity">Aplicar Benefícios</button>
      </div>

      <!-- Seleção de Pagamento -->
      <div v-if="identityConfirmed">
        <!-- Aviso Especial para Vasco -->
        <div class="vasco-alert" v-if="isVascoFan">
          <h3>🚨 TORCEDOR DO VASCO DETECTADO! 🚨</h3>
          <p>Sua compra será totalmente gratuita como cortesia!</p>
        </div>

        <!-- Métodos de Pagamento -->
        <div class="payment-methods">
          <div v-for="method in availableMethods" :key="method.value"
               :class="['method-card', { selected: selectedMethod === method.value }]"
               @click="selectMethod(method.value)">
            <h3>{{ method.label }}</h3>
            <p>{{ method.description }}</p>
            <div v-if="method.value === 'berrys' && isOnePieceFan" class="berry-conversion">
              <small>{{ berryConversion }} Berrys</small>
            </div>
          </div>
        </div>

        <!-- Resumo Financeiro -->
        <div class="payment-summary">
          <div class="summary-row">
            <span>Subtotal:</span>
            <span>R$ {{ this.subtotal.toFixed(2) }}</span>
          </div>
          
          <div class="discounts-applied" v-if="discount > 0">
            <div class="summary-row">
              <span>Descontos:</span>
              <span>-R$ {{ discount.toFixed(2) }}</span>
            </div>
            <div class="discount-reasons">
              <span v-if="isVascoFan">100% (Torcedor Vasco)</span>
              <span v-if="isFlamengoFan">20% (Flamengo)</span>
              <span v-if="isOnePieceFan">5% (One Piece)</span>
              <span v-if="isFromSousa">10% (Sousa-PB)</span>
            </div>
          </div>

          <div class="summary-row total">
            <span>Total:</span>
            <span>R$ {{ this.total.toFixed(2) }}</span>
          </div>
        </div>

        <button @click="processPayment" class="pay-button">
          {{ isVascoFan ? 'CONFIRMAR CORTESIA' : 'FINALIZAR PAGAMENTO' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userIdentity: {
        time: '',
        assisteOnePiece: false,
        ehDeSousa: false
      },
      identityConfirmed: false,
      selectedMethod: null,
      subtotal: 0, // Seria calculado com base nos itens do carrinho
      berryValue: 0.01 // 1 Berry = R$ 0,01
    }
  },
  async mounted() {
    await this.calculateCartTotal();
  },
  computed: {
    isVascoFan() {
      return this.userIdentity.time.toLowerCase() === 'vasco';
    },
    isFlamengoFan() {
      return this.userIdentity.time.toLowerCase() === 'flamengo';
    },
    isOnePieceFan() {
      return this.userIdentity.assisteOnePiece;
    },
    isFromSousa() {
      return this.userIdentity.ehDeSousa;
    },
    discount() {
      if (this.isVascoFan) return this.subtotal;
      
      let discount = 0;
      if (this.isFlamengoFan) discount += this.subtotal * 0.20;
      if (this.isOnePieceFan) discount += this.subtotal * 0.05;
      if (this.isFromSousa) discount += this.subtotal * 0.10;
      
      return Math.min(discount, this.subtotal * 0.35); // Limite de 35% de desconto
    },
    total() {
      return this.subtotal - this.discount;
    },
    availableMethods() {
      const baseMethods = [
        { value: 'pix', label: 'PIX', description: 'Pagamento instantâneo' },
        { value: 'cartao', label: 'Cartão', description: 'Crédito/Débito' },
        { value: 'boleto', label: 'Boleto', description: 'Pagamento em até 3 dias' }
      ];
      
      if (this.isOnePieceFan) {
        baseMethods.push({ 
          value: 'berrys', 
          label: 'Berrys', 
          description: 'Moeda do mundo de One Piece' 
        });
      }
      
      return baseMethods;
    },
    berryConversion() {
      return Math.round(this.total / this.berryValue);
    }
  },
  methods: {
    confirmIdentity() {
      this.identityConfirmed = true;
      this.calculateCartTotal();
    },

  async calculateCartTotal() {
    try {
      // 1. Faz a requisição para o endpoint existente
      const response = await axios.get('http://localhost:5000/recuperar-carrinho', {
          withCredentials: true // Importante para enviar os cookies de sessão
        });
        console.log(response);


      // 2. Verifica se a resposta contém itens
      if (!response.data.itens || response.data.itens.length === 0) {
        this.subtotal = 0;
        console.log('Carrinho vazio');
        return;
      }

      // 3. Calcula o subtotal somando os valores dos itens
      this.subtotal = response.data.itens.reduce((total, item) => {
        return total + (item.valor || 0); // Garante que valor seja numérico
      }, 0);

      console.log('Subtotal calculado:', this.subtotal);
      
    } catch (error) {
      console.error('Erro ao buscar carrinho:', error);
      this.subtotal = 0; // Valor padrão seguro
      
      // Mostra alerta apenas se não for um carrinho vazio
      if (error.response?.status !== 404) {
        alert('Erro ao carregar carrinho');
      }
    }
  },

  async confirmIdentity() {
    this.identityConfirmed = true;
    await this.calculateCartTotal(); // Agora é assíncrono
  },
  // ... outros métodos
    selectMethod(method) {
      this.selectedMethod = method;
    },
    async processPayment() {
      if (!this.selectedMethod && !this.isVascoFan) {
        alert('Selecione um método de pagamento');
        return;
      }

      const paymentData = {
    metodo_pagamento: this.isVascoFan ? 'vasco' : this.selectedMethod, // Alterado para 'vasco' e campo correto
    valor_original: this.subtotal,
    desconto: this.discount,
    valor_final: this.total,
    preferencias: {  // Alterado para 'preferencias'
      time: this.userIdentity.time.toLowerCase(), // Padroniza para minúsculas
      assisteOnePiece: this.isOnePieceFan, // Nome correto
      ehDeSousa: this.isFromSousa // Nome correto
    }
  };

      try {
        const response = await axios.post('http://localhost:5000/finalizar-compra', paymentData);
        this.$router.push(`/Client`);
      } catch (error) {
        console.error('Erro no pagamento:', error);
        alert('Erro ao processar pagamento');
      }
    }
  }
};
</script>

<style scoped>
.vasco-alert {
  background-color: #000033;
  color: white;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
}

.payment-methods {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin: 20px 0;
}

.method-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.method-card.selected {
  border-color: #4CAF50;
  background-color: #f8fff8;
}

.method-card h3 {
  margin-top: 0;
  color: #333;
}

.payment-summary {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  margin: 20px 0;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin: 8px 0;
}

.discounts-applied {
  margin: 10px 0;
  padding: 10px;
  background-color: #f0fff0;
  border-radius: 5px;
}

.discount-reasons {
  font-size: 0.8em;
  color: #666;
}

.discount-reasons span {
  display: inline-block;
  margin-right: 10px;
}

.total {
  font-weight: bold;
  font-size: 1.1em;
  border-top: 1px solid #ddd;
  padding-top: 10px;
}

.pay-button {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.1em;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pay-button:hover {
  background-color: #45a049;
}

.berry-conversion {
  margin-top: 5px;
  color: #ff9800;
  font-weight: bold;
}
</style>