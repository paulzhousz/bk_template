<template>
    <div id="main-container">
        <breadcrumb :to="$route.meta.bread"></breadcrumb>
        <div class="container">
            <router-view/>
        </div>
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
            'breadcrumb': Breadcrumb
        },
        methods: {}
    }
</script>

<style lang="scss" scoped>
    $headerHeight: 60px;
    #main-container {
        padding: 20px 20px 0 20px;
        width: calc(100% - 220px);
        height: calc(100% - 60px);
        background: #f0f2f5;
        float: left;
        overflow: hidden;
        .container {
            height: calc(100% - 55px);
            width: 100%;
        }
    }
</style>
