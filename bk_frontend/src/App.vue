<template>
    <div id='app'>
        <Header></Header>
        <LeftMenu></LeftMenu>
        <Container></Container>
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
        //   this.$http.get('/test/').then(res => {
        //     console.log(res)
        //   })
        }
    }
</script>
<style>
</style>
