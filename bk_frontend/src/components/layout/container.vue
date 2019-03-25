<template>
    <div id="main-container">
        <router-view/>
        <Footer></Footer>
    </div>
</template>

<script>
    import Footer from '@/components/layout/Footer'

    export default {
        name: 'container',
        mounted() {
        },
        components: {
            Footer
        },
        methods: {}
    }
</script>

<style lang="scss" scoped>
    $headerHeight: 60px;
    #main-container {
        width: calc(100% - 220px);
        height: calc(100% - 60px);
        background: #f0f2f5;
        float: left;
        overflow: hidden;
    }
</style>
