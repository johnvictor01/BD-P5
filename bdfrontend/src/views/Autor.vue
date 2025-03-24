<template>
    <div>
        <CabecalhoPessoa/>
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <h1>Olá, {{ autor.Nome }}</h1>
                    <p>Email: {{ autor.Email }}</p>
                </div>
            </div>
        </div>
        <h2>Suas Obras</h2>
        <Obras :obras="ObrasAutor"/> <!-- Passa as obras como props -->
        <br>
        <ButtonSolicitarPubli/>
        <br>
        <DashBoard :valoresObras="valoresObras"/> <!-- Passa os valores das obras como props -->
        <br>
        <ButtonSolicitarEditPubli/>
        <br>
        <Footer/>
    </div>
</template>

<script>
import CabecalhoPessoa from '../components/CabecalhoPessoa.vue'
import DashBoard from '../components/DashBoard.vue'
import Obras from '../components/Obras.vue'
import ButtonSolicitarPubli from '../components/ButtonSolicitarPubli.vue'
import ButtonSolicitarEditPubli from '../components/ButtonSolicitarEditPubli.vue'
import Footer from '../components/Footer.vue'
import axios from 'axios'

// Configura o Axios para enviar cookies
axios.defaults.withCredentials = true;

export default {
    name: 'Autor',
    data() {
        return {
            autor: {
                Nome: '',
                Email: '',
            },
            ObrasAutor: [], // Armazena as obras do autor
            valoresObras: [], // Armazena os valores das obras para o Dashboard
            loading: false // Controla o estado de carregamento
        }
    },
    components: {
        CabecalhoPessoa,
        DashBoard,
        Obras,
        ButtonSolicitarPubli,
        ButtonSolicitarEditPubli,
        Footer
    },
    methods: {
        async buscarUsuarioLogado() {
            try {
                const response = await axios.get('http://localhost:5000/autor-logado');
                this.autor = response.data;
            } catch (error) {
            alert("Erro ao buscar dados do autor. Tente novamente.");
                this.$router.push('/LoginAutor');  // Redireciona para a página de login em caso de erro
            }
        },

        async buscarObrasAutor() {
            if (!this.autor) {
                alert("Autor não autenticado.");
                this.$router.push('/LoginAutor');  // Redireciona para a página de login
                return;
            }
            
            this.loading = true;
            try {
                // Busca as obras do autor
                const response = await axios.get('http://localhost:5000/obras-autor');

                if (response.data.length === 0) {
                    alert("Nenhuma obra encontrada.");
                    this.ObrasAutor = [];  
                    // Define o array de obras como vazio
                } else {
                    this.ObrasAutor = response.data;
                    console.log('Valores das obras:', response.data); 
                }

                // Extrai os valores das obras para o Dashboard
                
                this.valoresObras = this.ObrasAutor.map(obra => obra.valor);
                 // Depuração
            } catch (error) {
                console.error('Erro ao buscar obras do autor:', error);
                if (error.response && error.response.status === 401) {
                    alert("Autor não autenticado ou sessão expirada.");
                    this.$router.push('/LoginAutor');  // Redireciona para a página de login
                } else {
                    alert("Erro ao carregar as obras.");
                }
            } finally {
                this.loading = false;
            }
        }
    },
    async mounted() {
        await this.buscarUsuarioLogado(); // Aguarda a conclusão da requisição
        this.buscarObrasAutor(); // Agora chama o método para buscar obras
    }
}
</script>

<style>
/* Estilos personalizados */
.container {
    margin-top: 2rem;
}

h1 {
    margin-top: 4rem;
}

h2 {
    margin-top: 2rem;
}
</style>