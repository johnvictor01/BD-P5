<template>
    <div class="login-container">
      <div class="login-card">
        <div class="login-form">
          <h2>Login</h2>
          <form @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="username">Usuário</label>
              <input type="text" id="username" v-model="username" required />
            </div>
            <div class="form-group">
              <label for="password">Senha</label>
              <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit" class="login-button">Login</button>
            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';  // Importa Axios para requisições HTTP
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        errorMessage: ''  // Armazena mensagens de erro
      };
    },
    methods: {
      async handleLogin() {
        try {
          const response = await axios.post('http://localhost:5000/verificar_usuario', {
            NomeUsuario: this.username,
            Senha: this.password
          });
  
          console.log('Login bem-sucedido:', response.data);
  
          // Redireciona para a página principal (exemplo)
          alert(`Bem-vindo, ${response.data.Nome}!`);
          this.$router.push('/Collaborator');  // Redireciona para a página de compras
  
        } catch (error) {
          if (error.response && error.response.status === 401) {
            this.errorMessage = 'Usuário ou senha incorretos.';
          } else {
            this.errorMessage = 'Erro ao conectar ao servidor.';
          }
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .error-message {
    color: red;
    margin-top: 10px;
    text-align: center;
  }
  </style>
  