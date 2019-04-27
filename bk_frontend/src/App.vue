<template>
    <div id='app'>
        <Header></Header>
        <div class="flex_content">
            <LeftMenu></LeftMenu>
            <Container></Container>
        </div>
    </div>
</template>

<script>
    import Header from '@/components/layout/header'
    import LeftMenu from '@/components/layout/LeftMenu'
    import Container from '@/components/layout/Container'
    import '@/assets/css/base.scss'
    import '@/assets/css/table.scss'
    import '@/assets/css/dialog.scss'

    export default {
        name: 'App',
        components: {
            Header,
            LeftMenu,
            Container
        },
        created () {
        }
    }
</script>
<style lang="scss">
#app {
    .flex_content {
        height: 100%;
        display: flex;
        #main-container {
            flex-grow: 1;
        }
    }
}
</style>
