<template>
    <div class="login-container">
      <div class="login-card">
        <div class="login-form">
          <p>Galeria Arte Nova</p>
          <h2 id="H2LOGIN">Login</h2>
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
          const response = await axios.post('http://localhost:5000/verificar_autor', {
            NomeUsuario: this.username,
            Senha: this.password
          });
  
          console.log('Login bem-sucedido:', response.data);
  
          // Redireciona para a página principal (exemplo)
          alert(`Bem-vindo, ${response.data.Nome}!`);
          this.$router.push('/Autor');  // Redireciona para a página de compras
  
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
 .login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(270deg, #6e2295, #5412af, #1970b8e1);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
  padding: 20px;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  width: 100%;
  min-width: 300px;
  max-width: 400px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}
#username, #password{
  padding: 10px;
  align-items: center;
}
p{
  font-size: 18px;
}

.login-form h2 {
  color: #333;
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 2rem;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
#H2LOGIN{
margin-top: 10px;
}

.form-group {
  margin-bottom: 1.5rem;
  
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid rgba(221, 36, 118, 0.3);
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
}

.form-group input:focus {
  outline: none;
  border-color: #dd2476;
  box-shadow: 0 0 0 3px rgba(221, 36, 118, 0.2);
}

.login-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(to right, #ff512f, #dd2476);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(221, 36, 118, 0.3);
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(221, 36, 118, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.error-message {
  color: #ff3333;
  margin-top: 1rem;
  text-align: center;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.7);
  padding: 8px;
  border-radius: 5px;
  border-left: 3px solid #ff3333;
}

  </style>
  