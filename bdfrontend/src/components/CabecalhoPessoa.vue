<template>
    <div class="top-bar">
      <router-link to="/" class="home-link">
        <font-awesome-icon icon="fa-solid fa-house" />
      </router-link>
      <div class="linha-neon"></div> <!-- Linha neon -->
      <div v-if="usuario" class="usuario-card-wrapper">
        
        <div class="usuario-card">
          <h3>{{ usuario.nome }}</h3>
          <p>Email: {{ usuario.email }}</p>
          <p>Telefone: {{ usuario.telefone }}</p>
        </div>
      </div>
      <div v-else class="loading">Carregando usuário...</div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import { library } from "@fortawesome/fontawesome-svg-core";
  import { faHouse } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
  
  library.add(faHouse);
  
  export default {
    name: "CabecalhoHome",
    components: {
      FontAwesomeIcon,
    },
    setup() {
      const usuario = ref(null);
  
      const fetchUsuario = () => {
        // JSON fixo para teste
        setTimeout(() => {
          usuario.value = {
            id: 1,
            nome: "João Silva",
            email: "joao@email.com",
            telefone: "(83) 99999-9999",
          };
        }, 1000);
      };
  
      onMounted(fetchUsuario);
  
      return { usuario };
    },
  };
  </script>
  
  <style>
  .top-bar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #000000;
    color: white;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    z-index: 10; /* Garante que a barra fique acima de outros elementos */
  }
  
  .home-link {
    margin-left: 15px;
    color: white;
    font-size: 24px;
    text-decoration: none;
  }
  

  .home-link:hover {
    transition-duration: 0.6s all;
    color: rgb(255, 184, 51);
    transition-duration: 0.6s;
    font-size: 30px;
    
  }

  

  
  .usuario-card-wrapper {
    margin-right: 5rem;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  
  .linha-neon {
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(to right, #fff, rgb(255, 184, 51), rgba(255, 184, 51, 0.6));
    box-shadow: 0 0 15px rgba(255, 184, 51, 1);
    transform: translateY(-50%);
  }
  
  .usuario-card {
    margin-top: 30px;
    background: #1c1c1c;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 2px 2px 5px rgba(255, 184, 51, 0.3);
    width: 100%;
    max-width: 400px; /* Limita a largura do card */
  }
  
  .usuario-card h3 {
    margin: 0;
    font-size: 18px;
    color: rgb(255, 184, 51);
  }
  
  .usuario-card p {
    font-size: 14px;
    margin: 5px 0;
  }
  
  .loading {
    margin-right: 5rem;
    font-size: 16px;
    text-align: center;
    margin-top: 20px;
  }
  </style>