<template>
  <div>
    <!-- Cabeçalho -->
    <div class="top-bar">
      <router-link to="/" class="home-link">
        <font-awesome-icon icon="fa-solid fa-house" />
      </router-link>

      <div class="user-area" @click="abrirPerfil">
        <div class="user-avatar">
          {{ usuarioIniciais }}
        </div>
        <span class="user-name">{{ usuario?.nome_completo || "Usuário" }}</span>
      </div>
    </div>

    <!-- Modal de Perfil -->
    <transition name="fade">
      <div
        v-if="mostrarPerfil"
        class="profile-modal-overlay"
        @click.self="fecharPerfil"
      >
        <div class="profile-modal">
          <button class="close-btn" @click="fecharPerfil">×</button>

          <div class="profile-header">
            <div class="profile-avatar">{{ usuarioIniciais }}</div>
            <h2>{{ usuario.nome_completo }}</h2>
          </div>

          <div class="profile-details">
            <div class="detail-item">
              <h3>Informações Pessoais</h3>
              <p><strong>CPF:</strong> {{ usuario.cpf }}</p>
              <p><strong>Nascimento:</strong> {{ formatarData(usuario.data_nascimento) }}</p>
              <p  v-show="tipoUsuario === 1"><strong>Matrícula:</strong> {{ usuario.matricula }}</p>
            </div>

            <div class="detail-item">
              <h3>Contato</h3>
              <p><strong>Email:</strong> {{ usuario.email }}</p>
              <p><strong>Telefone:</strong> {{ usuario.telefone }}</p>
              <p><strong>Endereço:</strong> {{ formatarEndereco(usuario.endereco) }}</p>
            </div>
          </div>

          <div
    v-show="tipoUsuario === 1"
    class="download-btn-container"
  >
    <button class="download-btn" @click="baixarDados">
      <font-awesome-icon icon="fa-solid fa-download" />
      Baixar Histórico de Compras
    </button>
  </div>
  <div
    v-show="tipoUsuario === 3"
    class="download-btn-container"
  >
    <button class="download-btn" @click="baixarDadosVendas">
      <font-awesome-icon icon="fa-solid fa-download" />
      Baixar Histórico de Vendas
    </button>
  </div>

        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faHouse, faDownload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import axios from "axios";

library.add(faHouse, faDownload);

export default {
  name: "CabecalhoPessoa",
  components: {
    FontAwesomeIcon,
  },
  props: {
    tipoUsuario: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const usuario = ref({});
    const mostrarPerfil = ref(false);
    const carregando = ref(true);

    const usuarioIniciais = computed(() => {
      const nome = usuario.value.nome_completo || "";
      return nome
        .split(" ")
        .map((n) => n[0] || "")
        .join("")
        .toUpperCase() || "US";
    });

    const carregarUsuario = async () => {
      let url;
      switch (props.tipoUsuario) {
        case 1:
          url = "http://localhost:5000/dados-usuario-logado";
          break;
        case 2:
          url = "http://localhost:5000/dados-autor-logado";
          break;
        case 3:
          url = "http://localhost:5000/dados-funcionario-logado";
          break;
        default:
          url = "http://localhost:5000/dados-usuario-logado";
      }

      try {
        const response = await axios.get(url, { withCredentials: true });
        usuario.value = response.data;
      } catch (error) {
        console.error("Erro ao carregar dados:", error);
      } finally {
        carregando.value = false;
      }
    };

    const abrirPerfil = () => {
      mostrarPerfil.value = true;
      document.body.style.overflow = "hidden";
    };

    const fecharPerfil = () => {
      mostrarPerfil.value = false;
      document.body.style.overflow = "";
    };

    const formatarData = (dataISO) => {
      if (!dataISO) return "N/A";
      const data = new Date(dataISO);
      return data.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "long",
        year: "numeric",
      });
    };

    const formatarEndereco = (endereco) => {
      if (!endereco) return "Não informado";
      const {
        rua = "",
        numero = "",
        bairro = "",
        cidade = "",
        estado = "",
        cep = "",
        pais = "",
      } = endereco;
      return `${rua}, ${numero} – ${bairro}, ${cidade} - ${estado}, ${cep}, ${pais}`;
    };

    const baixarDados = () => {
      const blob = new Blob([JSON.stringify(usuario.value, null, 2)], {
        type: "application/json",
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `historico_compras_${props.tipoUsuario}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

    const baixarDadosVendas = () => {
      const blob = new Blob([JSON.stringify(usuario.value, null, 2)], {
        type: "application/json",
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `historico_compras_${props.tipoUsuario}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };


    onMounted(carregarUsuario);

    return {
      usuario,
      mostrarPerfil,
      carregando,
      usuarioIniciais,
      abrirPerfil,
      fecharPerfil,
      formatarData,
      formatarEndereco,
      baixarDados,
    };
  },
};
</script>

<style scoped>
/* Estilos do cabeçalho */
.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #1a1a1a;
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.home-link {
  color: white;
  font-size: 24px;
  transition: all 0.3s ease;
}
.home-link:hover {
  color: #ffb833;
  transform: scale(1.1);
}

.user-area {
  display: flex;
  align-items: center;
  gap: 15px;
  cursor: pointer;
  padding: 8px 15px;
  border-radius: 30px;
  transition: background 0.3s ease;
}
.user-area:hover {
  background-color: rgba(255, 184, 51, 0.1);
}

.user-avatar {
  width: 40px;
  height: 40px;
  background-color: #ffb833;
  color: #1a1a1a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 16px;
}
.user-name {
  font-weight: 500;
}

/* Modal */
.profile-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  backdrop-filter: blur(5px);
}

.profile-modal {
  background-color: #1e1e1e;
  border-radius: 15px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 30px;
  position: relative;
  border: 1px solid #ffb833;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  color: #ffb833;
  font-size: 28px;
  cursor: pointer;
  transition: transform 0.3s ease;
}
.close-btn:hover {
  transform: scale(1.2);
}

.profile-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #333;
}
.profile-avatar {
  width: 80px;
  height: 80px;
  background-color: #ffb833;
  color: #1a1a1a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 32px;
  margin: 0 auto 15px;
}
.profile-header h2 {
  margin: 10px 0;
  color: #ffb833;
}
.member-since {
  color: #ccc;
  font-size: 0.9rem;
}

.profile-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}
.detail-item {
  background-color: #252525;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #ffb833;
}
.detail-item h3 {
  color: #ffb833;
  margin-top: 0;
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
}
.detail-item p {
  margin: 8px 0;
  color: #ddd;
}

/* Botão de download */
.download-btn-container {
  text-align: right;
  margin-top: 20px;
}
.download-btn {
  background-color: #ffb833;
  color: #1a1a1a;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s ease, transform 0.3s ease;
}
.download-btn:hover {
  background-color: #e0a72a;
  transform: scale(1.05);
}

/* Fade animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsivo */
@media (max-width: 768px) {
  .profile-details {
    grid-template-columns: 1fr;
  }
  .profile-modal {
    width: 95%;
    padding: 20px;
  }
}
</style>
