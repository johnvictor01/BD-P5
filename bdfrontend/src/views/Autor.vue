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

export default {
    name: 'Autor',
    data() {
        return {
            autor: {
                Nome: '',
                Email: '',
            },
            ObrasAutor: [], // Armazena as obras do autor
            valoresObras: [] // Armazena os valores das obras para o Dashboard
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
    async mounted() {
        try {
            // Busca os dados do autor
            const responseAutor = await axios.get('http://localhost:5000/autor-logado');
            this.autor = responseAutor.data;

            // Busca as obras do autor
            await this.buscarObrasAutor();
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            alert("Erro ao carregar dados. Tente novamente.");
        }
    },
    methods: {
        async buscarObrasAutor() {
            try {
                console.log("Printando os autores")
                const response = await axios.get('http://localhost:5000/obras-autor');
                this.ObrasAutor = response.data; // Atualiza as obras do autor
                console.log("nao passei")
                console.log(this.ObrasAutor)
                console.log("Acima printei os autores")
                

                // Extrai os valores das obras para o Dashboard
                this.valoresObras = this.ObrasAutor.map(obra => obra.Valor);
            } catch (error) {
                console.error('Erro ao buscar obras do autor:', error);
                alert("Erro ao carregar obras do autor. Tente novamente.");
            }
        }
    }
}
</script>

<style >

</style>