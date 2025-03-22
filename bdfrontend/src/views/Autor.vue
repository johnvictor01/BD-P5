<template>
    <div>
        <CabecalhoPessoa/>
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <h1>Olá, {{ autor.nome }}</h1>
                </div>
            </div>
        </div>
        <h2>Suas Obras</h2>
        <Obras/>
        <DashBoard/>
        <br>
        <ButtonSolicitarPubli/>
        <br>
        <ButtonSolicitarEditPubli/>

    </div>
</template>

<script>
import CabecalhoPessoa from '../components/CabecalhoPessoa.vue'
import DashBoard from '../components/DashBoard.vue'
import Obras from '../components/Obras.vue'
import ButtonSolicitarPubli from '../components/ButtonSolicitarPubli.vue'
import ButtonSolicitarEditPubli from '../components/ButtonSolicitarEditPubli.vue'

export default {
    name: 'Autor',
    data() {
        return {
            autor: {
                nome: 'Fulano de Tal',
                email:  '',
   
}
        }
    },
    components: {
        CabecalhoPessoa,
        DashBoard,
        Obras,
        ButtonSolicitarPubli,
        ButtonSolicitarEditPubli
    }
}

</script>

<style lang="scss" scoped>

</style>