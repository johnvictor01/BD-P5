<template>
    <div>
        <CabecalhoPessoa :tipoUsuario="3" />
        <br>
        <h1>Obras Esperando Autorização</h1>
        <AutorizarObras/>
        <h1>Deseja Excluir obras?</h1>
        <buttonExcluirObras/>
        <h1>Algumas Compras Exigem sua Aprovação:</h1>
        <AutorizarVenda/>

    </div>
</template>

<script>
import CabecalhoPessoa from '../components/CabecalhoPessoa.vue'
import AutorizarObras from '../components/AutorizarObras.vue'
import buttonExcluirObras from '../components/ButtonExcludeObras.vue'
import AutorizarVenda from '@/components/AutorizarVenda.vue'

    export default {
        name: 'CollaboratorView',
        components: {
            CabecalhoPessoa,
            AutorizarObras,
            buttonExcluirObras,
            AutorizarVenda
        }
    }
</script>

<style>

</style>