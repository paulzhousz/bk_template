<template>
    <div id="header">
        <div class="logo-info">
            <ul class="fat">
                <li class="logo">
                    <img src="../../assets/img/logo_new.png" alt="">
                    <span class="logo_lg">蓝鲸开发框架</span>
                </li>
                <li class="shrink_leftmenu" @change="changeShow">
                    <el-radio-group :value="isCollapse">
                        <el-radio-button :label="true" v-show="!isCollapse">
                            <i class="el-icon-s-fold"></i>
                        </el-radio-button>
                        <el-radio-button :label="false" v-show="isCollapse">
                            <i class="el-icon-s-unfold"></i>
                        </el-radio-button>
                    </el-radio-group>
                </li>
            </ul>
        </div>
        <div class="login">
            <ul>
                <li><img class="photo" src="../../assets/img/photo.jpg"></li>
                <li><span class="username">{{username}}</span></li>
                <li><a :href="logout_url" class="login-out el-icon-time"></a></li>
            </ul>
        </div>
    </div>
</template>

<script>
    import { mapGetters, mapMutations } from 'vuex'

    export default {
        name: 'cw-header',
        data() {
            return {
                username: '',
                logout_url: ''
            }
        },
        computed: {
            ...mapGetters('main', ['isCollapse'])
        },
        methods: {
            changeShow() {
                let isCollapse = !this.isCollapse
                this.$store.commit('main/setIsCollapse', isCollapse)
            }
        },
    }
</script>

<style lang="scss" scoped>
    $headerHeight: 50px;
    #header {
        width: 100%;
        height: $headerHeight;
        /*box-shadow: 0 0 8px 0 rgba(232, 237, 250, .6), 0 2px 4px 0 rgba(232, 237, 250, .5);*/
        // box-shadow: 0 5px 5px rgba(170, 170, 170, .32);
        line-height: $headerHeight;
        background: rgb(255, 255, 255);
        .logo-info {
            width: 230px;
            height: $headerHeight;
            float: left;
            .fat {
                width: 100%;
                height: 100%;
                .logo {
                    display: inline;
                    margin-left: 20px;
                    float: left;
                    img {
                        vertical-align: middle;
                        width: 35px;
                        height: 25px;
                    }
                    .logo_lg {
                        font-size: 18px;
                        color: #333;
                        text-align: left;
                        font-weight: bold;
                        vertical-align: middle;
                        margin-left: 5px;
                    }
                }
                .shrink_leftmenu {
                    height: 100%;
                    .el-radio-group {
                        width: 30px;
                        .el-icon-d-arrow-left {
                            cursor: pointer;
                            font-size: 18px;
                            margin-left: 40px;
                            vertical-align: middle;
                        }
                    }
                }
            }
            .app_name {
                float: left;
                line-height: 83px;
                background-image: -webkit-gradient(linear, 0 0, 0 bottom, from(rgba(168, 219, 245, 0.9)), to(rgba(3, 134, 207, 1)));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 23px;
                display: inline-block;
                height: 100%;
            }
        }
        .menu-list {
            margin-left: 20px;
            float: left;
            height: 100%;
            min-width: 600px;
        }
        .login {
            float: right;
            height: 100%;
            width: 200px;
            padding-left: 20px;
            li {
                height: $headerHeight;
                float: left;
                line-height: $headerHeight;
                margin: 0 8px;
            }
            .photo {
                width: 40px;
                height: 40px;
                border-radius: 50px;
                vertical-align: middle;
                display: inline-block;
                border: 1px solid #ddd;
            }
            .username {
                font-size: 18px;
                margin-top: 5px;
            }
            .login-out {
                font-size: 25px;
                color: #37b9ed;
                margin-top: 18px;
                cursor: pointer;
            }
            .login-out:hover {
                color: #ddd;
            }
        }
    }
</style>
<style lang="scss">
    .el-radio-button__inner {
        border: none !important;
        font-size: 20px;
        // margin-left: 20px;
    }
</style>
