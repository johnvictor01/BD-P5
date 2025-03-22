<template>
  <div>

    <CabecalhoHome/>
    <MoreInformation/>
    <Contacts/>
    <Footer/>


  </div>


</template>

<script>
import CabecalhoHome from '../components/CabecalhoHome.vue'
import MoreInformation from '../components/MoreInformation.vue'
import Contacts from '../components/Contacts.vue'
import Footer from '../components/Footer.vue'
export default {
  name: 'HomeView',
  components: {
    CabecalhoHome,
    MoreInformation,
    Contacts,
    Footer
  }
}
</script>

<style>

</style>
