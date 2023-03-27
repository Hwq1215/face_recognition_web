<template>
    <div class="body">
            <Header></Header>
                <router-view />
            <Footer></Footer>
    </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
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

<style>
.body{
    width: 100%;
    height: 100%;
}
</style>