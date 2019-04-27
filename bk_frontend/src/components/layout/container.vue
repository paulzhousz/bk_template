<template>
    <div id="main-container" :style="isCollapse ? 'width: calc(100% - 230px)' : 'width: calc(100% - 230px)'">
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
    import { mapGetters } from 'vuex'

    export default {
        name: 'container',
        mounted() {
        },
        components: {
            'app-footer': Footer,
            'breadcrumb': Breadcrumb
        },
        computed: {
            ...mapGetters('main', ['isCollapse'])
        },
        methods: {}
    }
</script>

<style lang="scss" scoped>
    $headerHeight: 50px;
    #main-container {
        padding: 20px 20px 0 20px;
        height: calc(100% - 50px);
        background: #f0f2f5;
        float: left;
        overflow: hidden;
        .container {
            height: calc(100% - 55px);
            width: 100%;
        }
    }
</style>
