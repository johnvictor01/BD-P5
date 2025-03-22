<template>
    <div>
        <h1>Destaques das nossas obras de arte</h1>
        <Obras/>
    </div>
</template>

<script >

import Obras from '../components/Obras.vue'

export default {
    name: 'MoreInformation',
    data(){
      
    },
    components: {
        Obras
    }
}

</script>

<style >

h1 {
    margin-top: 8rem;
    text-align: center;
    margin-bottom: 20px;
}


</style>
