<template>
    <div id="header">
        <div class="logo-info">
            <ul>
                <li class="logo">
                    <img src="../../assets/img/logo.png" alt="">
                </li>
                <li class="line"></li>
                <li class="app_name">
                    <a href="/" class="">开发框架</a>
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
    export default {
        name: 'cw-header',
        data() {
            return {
                username: '',
                logout_url: ''
            }
        },
    }
</script>

<style lang="scss" scoped>
    $headerHeight: 60px;
    #header {
        width: 100%;
        height: $headerHeight;
        /*box-shadow: 0 0 8px 0 rgba(232, 237, 250, .6), 0 2px 4px 0 rgba(232, 237, 250, .5);*/
        // box-shadow: 0 5px 5px rgba(170, 170, 170, .32);
        line-height: $headerHeight;
        background: rgb(85, 92, 99);
        .logo-info {
            width: 360px;
            height: $headerHeight;
            float: left;
            .logo {
                display: inline;
                margin-left: 20px;
                float: left;
            }
            .logo img {
                vertical-align: middle;
            }
            .line {
                float: left;
                height: 15px;
                border-left: 1px solid #ddd;
                margin: 33px 15px 5px 15px;
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
