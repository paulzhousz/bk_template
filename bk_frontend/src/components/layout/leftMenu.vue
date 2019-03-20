<template>
    <div id="left-menu">
        <el-row>
            <el-col :span="12">
                <el-menu
                router
                :default-active="currentMenu"
                background-color="rgb(4, 21, 39)"
                text-color="#fff"
                active-text-color="#ffd04b"
                :unique-opened="only">
                    <template v-for="(item, index) in menusList">
                        <el-submenu :index="index + ''" :key="index" v-if="item.children.length > 0 && item.is_menu">
                            <template slot="title">
                                <i class="el-icon-document"></i>
                                <span>{{item.display_name}}</span>
                            </template>
                            <el-menu-item v-for="(itemChild, indexChild) in item.children" :index="itemChild.path" :key="indexChild">
                                <span>{{itemChild.display_name}}</span>
                            </el-menu-item>
                        </el-submenu>
                        <el-menu-item :index="item.path" :key="item.path" v-else-if="item.children == 0 && item.is_menu">
                            <i class="el-icon-view"></i>
                            <span>{{item.display_name}}</span>
                        </el-menu-item>
                    </template>
                </el-menu>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                only: true,
                currentMenu: '/home',
                menusList: [
                    {children: []}
                ]
            }
        },
       created() {
            this.getUrl()
            this.getLeftmenu()
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
                self.currentMenu = currentUrl.split('#')[1];
            },
            getPath() {
                /*
                * 点击浏览器前进后退按钮高亮显示同步
                */
                let self = this
                self.currentMenu = self.$route.path;
            },
            getLeftmenu() {
                this.$store.dispatch('leftmenu/getMenu').then(res => {
                    if (res.result) {
                        // for (let i of res.data) {
                        //     if (i.children.length == 0) {
                                this.menusList = res.data
                                console.log(res.data)
                            }
                    //     }
                    // }
                })
            }
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
        width: 220px;
        height: calc(100% - 60px);
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
    #left-menu ul>li>div>span {
        margin-left: 20px;
    }
    #left-menu ul>li>span {
        margin-left: 20px;
    }
    .el-submenu .el-menu-item {
        padding-left: 90px !important;
    }
</style>
<style lang="scss">
    #left-menu .el-submenu.is-opened > .el-submenu__title {
        color: rgb(248, 209, 100) !important;
        i {
            color: rgb(248, 209, 100);
        }
    }
    #left-menu .el-submenu.is-opened .el-submenu__icon-arrow.el-icon-arrow-down {
        color: rgb(248, 209, 100) !important;
    }
</style>
