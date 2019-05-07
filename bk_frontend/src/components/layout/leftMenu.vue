<template>
    <div id="left-menu" :style="isCollapse ? 'width: auto' : 'width: 230px'">
        <el-row>
            <el-col :span="12">
                <el-menu
                router
                :default-active="currentMenu"
                background-color="rgb(42, 47, 55)"
                text-color="#fff"
                active-text-color="#ffd04b"
                :unique-opened="only"
                :collapse="isCollapse">
                    <template v-for="(item, index) in routerMenuList">
                        <el-submenu :index="index + ''" :key="index" v-if="item.children.length > 0 && item.is_menu">
                            <template slot="title">
                                <font-awesome-icon :icon="item.icon"></font-awesome-icon>
                                <span>{{item.display_name}}</span>
                            </template>
                            <el-menu-item v-for="(itemChild, indexChild) in item.children" :index="itemChild.path" :key="indexChild">
                              <span v-if="itemChild.is_menu">{{itemChild.display_name}}</span>
                            </el-menu-item>
                        </el-submenu>
                        <el-menu-item :index="item.path" :key="item.path" v-else-if="item.children == 0 && item.is_menu">
                            <font-awesome-icon :icon="item.icon"></font-awesome-icon>
                            <span>{{item.display_name}}</span>
                        </el-menu-item>
                    </template>
                </el-menu>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex'

    export default {
        data() {
            return {
                only: true,
                currentMenu: '/monitor_panel',
                menusList: [
                    {children: []}
                ]
            }
        },
        created() {
            this.$root.$on('change', (val) => {
                this.isCollapse = val
            })
            this.getUrl()
        },
        computed: {
            ...mapGetters('leftmenu', ['routerMenuList']),
            ...mapGetters('main', ['isCollapse'])
        },
        methods: {
            getUrl() {
                /*
                * 刷新当前页面左侧对应菜单高亮
                * @param    currentUrl       当前url
                * @param    currentMenu      当前菜单
                */
                let self = this
                let currentUrl = window.location.href;
                self.currentMenu = self.$route.meta.currentMenu
            },
            getPath() {
                /*
                * 点击浏览器前进后退按钮高亮显示同步
                */
                let self = this
                self.currentMenu = self.$route.meta.currentMenu
            },
        },
        watch: {
            /*
            * 监听路由，当路由变化时，改变默认显示高亮的值
            */
            '$route': 'getPath'
        }
    }
</script>

<style lang="scss" scoped>
    #left-menu {
        width: auto;
        height: calc(100% - 50px);
        float: left;
        .el-menu {
            border-right: none;
            width: 100%;
            height: 100%;
        }
        .el-row {
            width: 100%;
            height: 100%;
        }
        .el-row .el-col.el-col-12 {
            width: 100%;
            height: 100%;
            ul li span{
                margin-left: 20px;
            }
        }
    }
    // #left-menu ul>li>div>span {
    //     margin-left: 20px;
    // }
    // #left-menu ul>li>span {
    //     margin-left: 20px;
    // }
    .el-submenu .el-menu-item {
        padding-left: 50px !important;
    }
</style>
<style lang="scss">
    .el-submenu__title {
        padding-left: 30px !important;
        font-size: 13px !important;
        color: rgb(199, 207, 212) !important;
        font-weight: 500 !important;
        border-left: 3px solid rgb(42, 47, 55);
    }
    .el-submenu__title:hover {
        color: #fff !important;
        background: rgb(28, 31, 37) !important;
        border-left: 3px solid rgb(74, 155, 255);
    }
    .el-submenu.is-opened {
        .el-submenu__title {
            background: rgb(28, 31, 37) !important;
            border-left: 3px solid rgb(74, 155, 255);
        }
        .el-menu-item {
            background: rgb(28, 31, 37) !important;
            border-left: 3px solid rgb(74, 155, 255);
        }
    }
    .el-menu-item:hover {
        color: #fff !important;
        background: rgb(28, 31, 37) !important;
    }
    .el-menu-item.is-active {
        color: #fff !important;
        font-weight: 500px;
        background: rgb(28, 31, 37) !important;
        border-left: 3px solid rgb(74, 155, 255);
    }
    .el-menu-item {
        padding-left: 30px !important;
        font-size: 13px !important;
        color: rgb(155, 175, 185) !important;
        font-weight: 500 !important;
        border-left: 3px solid rgb(42, 47, 55);
    }
    .el-submenu.is-active {
        background: rgb(28, 31, 37) !important;
    }
</style>
