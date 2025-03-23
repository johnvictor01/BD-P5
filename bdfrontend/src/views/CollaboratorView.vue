<template>
    <div>
        <CabecalhoPessoa/>
        <br>
        <h1>Obras Esperando Autorização</h1>
        <AutorizarObras/>
        <h1>Deseja Excluir obras?</h1>
        <buttonExcluirObras/>

    </div>
</template>

<script>
import CabecalhoPessoa from '../components/CabecalhoPessoa.vue'
import AutorizarObras from '../components/AutorizarObras.vue'
import buttonExcluirObras from '../components/ButtonExcludeObras.vue'

    export default {
        name: 'CollaboratorView',
        components: {
            CabecalhoPessoa,
            AutorizarObras,
            buttonExcluirObras
        }
    }
</script>

<style>

</style>