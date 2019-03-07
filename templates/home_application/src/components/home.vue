<template>
    <div id="home">
        <Breadcrumb :to="to"></Breadcrumb>
        <span>{{msg}}</span>
        <Pagination
        :total="totalNumber"
        :page-size-change="pageSizeChange"
        :current-page-change="currentPageChange"></Pagination>
    </div>
</template>

<script>
import Breadcrumb from '@/components/Breadcrumb'
import Pagination from '@/components/Pagination'

    export default {
        name: 'HelloWorld',
        data() {
            return {
                msg: '欢迎使用嘉维蓝鲸开发框架',
                to: [
                    {displayName: '监控对象', path: '/'},
                    {displayName: '监控对象组', path: '/'}
                ],
                totalNumber: 0
            }
        },
        components: {
            Breadcrumb,
            Pagination
        },
        methods: {
            pageSizeChange(val) {
            },
            currentPageChange(val) {
            },
        }
    }
</script>

<style lang="scss" scoped>
    #home {
        background: #fff;
        height: 100%;
        width: 100%;
        text-align: center;
        span {
            display: inline-block;
            font-size: 30px;
            color: rgb(69, 162, 216);
            margin-top: 15%;
        }
    }
</style>
