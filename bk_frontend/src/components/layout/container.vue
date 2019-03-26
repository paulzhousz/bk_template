<template>
    <div id="main-container">
        <breadcrumb :to="$route.meta.bread"></breadcrumb>
        <router-view/>
        <app-footer></app-footer>
    </div>
</template>

<script>
    import Breadcrumb from '@/components/Breadcrumb'
    import Footer from '@/components/layout/Footer'

    export default {
        name: 'container',
        mounted() {
        },
        components: {
            'app-footer': Footer,
            Breadcrumb
        },
        methods: {}
    }
</script>

<style lang="scss" scoped>
    $headerHeight: 60px;
    #main-container {
        padding: 20px 0 0 20px;
        width: calc(100% - 220px);
        height: calc(100% - 60px);
        background: #f0f2f5;
        float: left;
        overflow: hidden;
    }
</style>
