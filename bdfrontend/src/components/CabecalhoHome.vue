<template>
    <div>
      <div class="cabecalho-links">
        <router-link to="/" class="home-link">
          <font-awesome-icon icon="fa-solid fa-house" />
        </router-link>
  
        <nav>
          <router-link to="/Client">Cliente</router-link> |
          <router-link to="/Collaborator">Colaborador</router-link> |
          <router-link to="/Autor">Autor</router-link>
        </nav>
      </div>
    </div>
  </template>
  
  <script>
  import { library } from "@fortawesome/fontawesome-svg-core";
  import { faHouse } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
  
  library.add(faHouse);
  
  export default {
    name: "CabecalhoHome",
    components: {
      FontAwesomeIcon,
    },
  };
  </script>
  
  <style>
  .cabecalho-links {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    padding: 10px 20px;
    color: white;
    justify-content: space-between;
    align-items: center;
    background-color: #000000;
    border-bottom: 1px solid #ccc;
  }
  
  .home-link {
    color: white;
    font-size: 24px;
    text-decoration: none;
  }
  
  .home-link:hover {
    color: rgb(255, 184, 51);
  }
  
  .cabecalho-links nav a {
    color: white;
    text-decoration: none;
    margin: 0 10px;
  }
  
  .cabecalho-links nav a:hover {
    color: rgb(255, 184, 51);
  }
  </style>
  