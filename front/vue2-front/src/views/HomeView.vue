<template>
    <div>
    <Header></Header>
    <router-view />
    <Footer></Footer>
    </div>
</template>

<script>
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'

export default {
    name: 'HomeView',    
    data() {
        return{
        }
    },
    components: {
        Header,
        Footer,
    }
}
</script>