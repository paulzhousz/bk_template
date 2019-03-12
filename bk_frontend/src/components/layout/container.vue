<template>
    <div id="main-container">
        <router-view/>
    </div>
</template>

<script>
    export default {
        name: 'container',
        mounted() {
        },
        methods: {}
    }
</script>

<style lang="scss" scoped>
    $headerHeight: 60px;
    #main-container {
        width: calc(100% - 220px);
        height: calc(100% - 60px);
        padding: 20px;
        background: #f0f2f5;
        float: left;
        overflow: hidden;
    }
</style>
