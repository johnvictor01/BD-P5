<template>
    <div>
      <CabecalhoPessoa />
      <h1>. <br>.</h1>
      <h1>Edite sua Obra</h1>
        <form id="obra-form" @submit="submitForm">
          <div class="input-container">
            <label for="titulo">Título da Obra</label>
            <input type="text" id="titulo" v-model="titulo" required />
          </div>
          <div class="input-container">
            <label for="descricao">Descrição</label>
            <textarea id="descricao" v-model="descricao" required></textarea>
          </div>
          <div class="input-container">
            <input type="submit" class="submit-btn" :value="isEditing ? 'Salvar Edição' : 'Publicar Obra'" />
          </div>
        </form>
      </div>
  </template>
  
  <script>

  import Message from "../components/Message.vue";
  import CabecalhoPessoa from '../components/CabecalhoPessoa.vue'
  
  export default {
    name: "FormsPubli",
    components: {
      Message,
      CabecalhoPessoa
    },
    data() {
      return {
        usuario: "",
        senha: "",
        isLoggedIn: false,
        titulo: "",
        descricao: "",
        msg: "",
        msgvisible: false,
        isEditing: false, // Indica se está no modo de edição
        obraId: null, // Armazena o ID da obra em edição
      };
    },
    mounted() {
  // Verifica se há uma obra na rota ao carregar o componente
  if (this.$route.params.obra) {
    this.isEditing = true;
    this.obra = this.$route.params.obra; // Armazena o objeto da obra
    this.carregarObraParaEdicao();
  }
},
watch: {
  // Observa mudanças na obra da rota
  '$route.params.obra': function(newObra) {
    if (newObra) {
      this.isEditing = true;
      this.obra = newObra;
      this.carregarObraParaEdicao();
    }
  }
},

   
        
methods: {
  async submitForm(e) {
    e.preventDefault();

    const userId = localStorage.getItem("userId");

    // Dados da obra
    const obra = {
      nome: this.titulo, // Use o campo 'nome' da obra
      informacoes: this.descricao, // Use o campo 'informacoes' da obra
      autor: userId,
    };

    try {
      if (this.isEditing) {
        // Modo de edição: atualiza a obra existente
        obra.id = this.obra.id; // Usa o ID da obra original
        const response = await axios.put('http://localhost:5000/edit-obra', obra);
        console.log("Obra atualizada:", response.data);
        this.msg = "Obra atualizada com sucesso!";
      } else {
        // Modo de criação: cria uma nova obra
        const response = await axios.post("http://localhost:5000/obras", obra);
        console.log("Nova obra criada:", response.data);
        this.msg = "Obra publicada com sucesso!";
      }

      this.msgvisible = true;
      setTimeout(() => (this.msgvisible = false), 3000);

      // Limpa o formulário após o envio
      this.titulo = "";
      this.descricao = "";

      // Redireciona para a página /Autor
      this.$router.push({ name: 'Autor' });
    } catch (error) {
      console.error("Erro ao salvar obra:", error);
      this.msg = "Erro ao salvar a obra!";
      this.msgvisible = true;
      setTimeout(() => (this.msgvisible = false), 3000);
    }
  },
},
  }
  </script>
  
  <style>
  #obra-form {
    max-width: 400px;
    margin: 0 auto;
  }
  
  .input-container {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
  }
  
  label {
    font-weight: bold;
    margin-bottom: 5px;
    color: #222;
  }
  
  input,
  textarea {
    padding: 5px;
    width: 100%;
  }
  
  .submit-btn {
    background-color: #222;
    color: #d49400;
    border: 2px solid #22222247;
    border-radius: 10px;
    font-weight: bold;
    font-size: 16px;
    padding: 10px;
    cursor: pointer;
    transition: 0.5s;
  }
  
  .submit-btn:hover {
    background-color: transparent;
    color: #222;
  }
  </style>