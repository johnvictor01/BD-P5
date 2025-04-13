<template>
    <div class="cadastro-container">
      <h2>Cadastro de Autor</h2>
      <form @submit.prevent="submitForm" class="cadastro-form">
        <!-- Seção de Dados Pessoais -->
        <fieldset>
          <legend>Dados Pessoais</legend>
          
          <div class="form-group">
            <label for="nome">Nome*</label>
            <input type="text" id="nome" v-model="formData.Nome" required maxlength="100">
          </div>
  
          <div class="form-group">
            <label for="sobrenome">Sobrenome*</label>
            <input type="text" id="sobrenome" v-model="formData.Sobrenome" required maxlength="100">
          </div>
  
          <div class="form-group">
            <label for="cpf">CPF*</label>
            <input type="text" id="cpf" v-model="formData.CPF" 
                   @input="formatCPF" required pattern="\d{3}\.\d{3}\.\d{3}-\d{2}">
            <small>Formato: 000.000.000-00</small>
          </div>
  
          <div class="form-group">
            <label for="dataNascimento">Data de Nascimento*</label>
            <input type="date" id="dataNascimento" v-model="formData.DataNascimento" required>
          </div>
  
          <div class="form-group">
            <label for="email">Email*</label>
            <input type="email" id="email" v-model="formData.Email" required maxlength="100">
          </div>
  
          <div class="form-group">
            <label for="telefone">Telefone</label>
            <input type="tel" id="telefone" v-model="formData.Telefone" 
                   @input="formatTelefone" maxlength="15">
            <small>Formato: (00) 00000-0000</small>
          </div>
        </fieldset>
  
        <!-- Seção de Endereço -->
        <fieldset>
          <legend>Endereço</legend>
          
          <div class="form-group">
            <label for="rua">Rua*</label>
            <input type="text" id="rua" v-model="formData.Rua" required maxlength="200">
          </div>
  
          <div class="form-row">
            <div class="form-group">
              <label for="numero">Número*</label>
              <input type="text" id="numero" v-model="formData.Numero" required maxlength="10">
            </div>
  
            <div class="form-group">
              <label for="bairro">Bairro*</label>
              <input type="text" id="bairro" v-model="formData.Bairro" required maxlength="100">
            </div>
          </div>
  
          <div class="form-row">
            <div class="form-group">
              <label for="cidade">Cidade*</label>
              <input type="text" id="cidade" v-model="formData.Cidade" required maxlength="100">
            </div>
  
            <div class="form-group">
              <label for="estado">Estado*</label>
              <select id="estado" v-model="formData.Estado" required>
                <option value="">Selecione</option>
                <option v-for="(estado, sigla) in estadosBrasil" :value="sigla">{{ estado }}</option>
              </select>
            </div>
          </div>
  
          <div class="form-row">
            <div class="form-group">
              <label for="cep">CEP*</label>
              <input type="text" id="cep" v-model="formData.CEP" 
                     @input="formatCEP" required maxlength="9">
              <small>Formato: 00000-000</small>
            </div>
  
            <div class="form-group">
              <label for="pais">País*</label>
              <select id="pais" v-model="formData.Pais" required>
                <option value="BRA">Brasil</option>
                <option value="ARG">Argentina</option>
                <option value="USA">Estados Unidos</option>
              </select>
            </div>
          </div>
        </fieldset>
  
        <!-- Seção de Dados de Autor -->
        <fieldset>
          <legend>Dados de Autor</legend>
          
          <div class="form-group">
            <label for="matricula">Matrícula*</label>
            <input type="text" id="matricula" v-model="formData.MatriculaAutor" required maxlength="15">
          </div>
  
          <div class="form-group">
            <label for="nomeUsuario">Nome de Usuário*</label>
            <input type="text" id="nomeUsuario" v-model="formData.NomeUsuario" required maxlength="30">
          </div>
  
          <div class="form-group">
            <label for="senha">Senha*</label>
            <input type="password" id="senha" v-model="formData.Senha" required minlength="8">
            <small>Mínimo 8 caracteres</small>
          </div>
  
          <div class="form-group">
            <label for="confirmarSenha">Confirmar Senha*</label>
            <input type="password" id="confirmarSenha" v-model="confirmarSenha" required>
            <span v-if="senhasNaoConferem" class="error-message">As senhas não coincidem</span>
          </div>
        </fieldset>
  
        <div class="form-actions">
          <button type="submit" :disabled="submitting || senhasNaoConferem">
            {{ submitting ? 'Cadastrando...' : 'Cadastrar' }}
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'FormsCadAutor',
    data() {
      return {
        formData: {
          // Dados Pessoais
          Nome: "",
          Sobrenome: "",
          CPF: "",
          DataNascimento: "",
          Email: "",
          Telefone: "",
          
          // Endereço
          Rua: "",
          Numero: "",
          Bairro: "",
          Cidade: "",
          Estado: "",
          CEP: "",
          Pais: "BRA",
          
          // Dados de Autor
          MatriculaAutor: "",
          NomeUsuario: "",
          Senha: "",
        },
        confirmarSenha: "",
        submitting: false,
        estadosBrasil: {
          "AC": "Acre",
          "AL": "Alagoas",
          "AP": "Amapá",
          "AM": "Amazonas",
          "BA": "Bahia",
          "CE": "Ceará",
          "DF": "Distrito Federal",
          "ES": "Espírito Santo",
          "GO": "Goiás",
          "MA": "Maranhão",
          "MT": "Mato Grosso",
          "MS": "Mato Grosso do Sul",
          "MG": "Minas Gerais",
          "PA": "Pará",
          "PB": "Paraíba",
          "PR": "Paraná",
          "PE": "Pernambuco",
          "PI": "Piauí",
          "RJ": "Rio de Janeiro",
          "RN": "Rio Grande do Norte",
          "RS": "Rio Grande do Sul",
          "RO": "Rondônia",
          "RR": "Roraima",
          "SC": "Santa Catarina",
          "SP": "São Paulo",
          "SE": "Sergipe",
          "TO": "Tocantins"
        }
      }
    },
    computed: {
      senhasNaoConferem() {
        return this.formData.Senha && this.confirmarSenha && 
               this.formData.Senha !== this.confirmarSenha;
      }
    },
    methods: {
      formatCPF(event) {
        let value = event.target.value.replace(/\D/g, '');
        if (value.length > 3) value = value.replace(/^(\d{3})/, '$1.');
        if (value.length > 7) value = value.replace(/^(\d{3})\.(\d{3})/, '$1.$2.');
        if (value.length > 11) value = value.replace(/^(\d{3})\.(\d{3})\.(\d{3})/, '$1.$2.$3-');
        this.formData.CPF = value.substring(0, 14);
      },
      formatTelefone(event) {
        let value = event.target.value.replace(/\D/g, '');
        if (value.length > 0) value = `(${value.substring(0, 2)}${value.length > 2 ? ') ' : ''}${value.substring(2)}`;
        if (value.length > 10) value = `${value.substring(0, 10)}-${value.substring(10)}`;
        this.formData.Telefone = value.substring(0, 15);
      },
      formatCEP(event) {
        let value = event.target.value.replace(/\D/g, '');
        if (value.length > 5) value = `${value.substring(0, 5)}-${value.substring(5)}`;
        this.formData.CEP = value.substring(0, 9);
      },
      async submitForm() {
        if (this.senhasNaoConferem || this.submitting) return;
        
        this.submitting = true;
        
        try {
          // Preparar os dados para envio
          const payload = {
            pessoa: {
              Nome: this.formData.Nome,
              Sobrenome: this.formData.Sobrenome,
              CPF: this.formData.CPF.replace(/\D/g, ''),
              DataNascimento: this.formData.DataNascimento,
              Email: this.formData.Email,
              Telefone: this.formData.Telefone.replace(/\D/g, '')
            },
            endereco: {
              Rua: this.formData.Rua,
              Numero: this.formData.Numero,
              Bairro: this.formData.Bairro,
              Cidade: this.formData.Cidade,
              Estado: this.formData.Estado,
              CEP: this.formData.CEP.replace(/\D/g, ''),
              Pais: this.formData.Pais
            },
            autor: {
              MatriculaAutor: this.formData.MatriculaAutor,
              NomeUsuario: this.formData.NomeUsuario,
              Senha: this.formData.Senha
            }
          };
  
          // Aqui você faria a chamada para sua API
          console.log("Dados para cadastro de autor:", payload);
          
          // Simulando uma requisição assíncrona
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          alert("Autor cadastrado com sucesso!");
          this.resetForm();
          
        } catch (error) {
          console.error("Erro ao cadastrar autor:", error);
          alert("Ocorreu um erro ao cadastrar o autor. Por favor, tente novamente.");
        } finally {
          this.submitting = false;
        }
      },
      resetForm() {
        this.formData = {
          Nome: "",
          Sobrenome: "",
          CPF: "",
          DataNascimento: "",
          Email: "",
          Telefone: "",
          Rua: "",
          Numero: "",
          Bairro: "",
          Cidade: "",
          Estado: "",
          CEP: "",
          Pais: "BRA",
          MatriculaAutor: "",
          NomeUsuario: "",
          Senha: ""
        };
        this.confirmarSenha = "";
      }
    }
  }
  </script>
  
  <style scoped>
  /* Estilos idênticos aos dos outros formulários */
  .cadastro-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  h2 {
    color: #2c3e50;
    text-align: center;
    margin-bottom: 30px;
  }
  
  .cadastro-form {
    background: #f9f9f9;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  fieldset {
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 20px;
    margin-bottom: 20px;
  }
  
  legend {
    padding: 0 10px;
    color: #3498db;
    font-weight: bold;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-row {
    display: flex;
    gap: 15px;
  }
  
  .form-row .form-group {
    flex: 1;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #34495e;
  }
  
  input, select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  
  input:focus, select:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
  }
  
  small {
    display: block;
    margin-top: 5px;
    color: #7f8c8d;
    font-size: 12px;
  }
  
  .error-message {
    color: #e74c3c;
    font-size: 12px;
    margin-top: 5px;
  }
  
  .form-actions {
    text-align: center;
    margin-top: 20px;
  }
  
  button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #2980b9;
  }
  
  button:disabled {
    background-color: #95a5a6;
    cursor: not-allowed;
  }
  
  @media (max-width: 600px) {
    .form-row {
      flex-direction: column;
      gap: 0;
    }
  }
  </style>