<template>
    <div class="container">
      <h2 class="title">Contatos da Galeria</h2>
      
      <div class="contact-card">
        <h3>Galeria Arte Nova</h3>

        <p><font-awesome-icon icon="envelope" /> contato@artenova.com</p>
        <p><font-awesome-icon icon="phone" /> (11) 98765-4321</p>
        <p><font-awesome-icon icon="map-marker-alt" /> Av. Paulista, 1000 - SP</p>
      </div>
  
    </div>
  </template>
  
  <script>
  import { library } from "@fortawesome/fontawesome-svg-core";
  import { faEnvelope, faPhone, faMapMarkerAlt } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
  
  // Adiciona os ícones à biblioteca
  library.add(faEnvelope, faPhone, faMapMarkerAlt);
  

  export default {
    name: "Contacts",
    components: {
      FontAwesomeIcon
    }
  };
  </script>
  
  <style>
  body {
    font-family: Arial, sans-serif;
    background: #f4f4f4;
    color: #333;
  }

  h2{
    margin-top: 7rem;
  }

  .container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
    text-align: center;
  }
  
  .title {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .contact-card {
    border: 1px solid #ddd;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 8px;
    background: #f9f9f9;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .contact-card h3 {
    margin: 0;
    color: #333;
    text-align: center;
  }
  
  .contact-card p {
    margin: 5px 0;
    color: #555;
    display: flex;
    align-items: center;
    justify-content: center;
    align-items: center;
  }
  
  .contact-card p svg {
    margin-right: 8px;
    color: rgb(200, 142, 36);  }
  </style>
  