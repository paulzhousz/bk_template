import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/home'
import First from '@/pages/first/First'
import New from '@/pages/new/New'
Vue.use(Router);

let router = new Router({
    routes: [
        {
            path: '/',
            redirect: '/index'
        },
        {
            path: '/first_first',
            component: First
        },
        {
            path: '/home',
            name: 'Home',
            component: Home,
            menuName: '首页',
            menuShow: true,
            hasChild: false,
        },
        {
            path: '/new',
            name: 'New',
            component: New,
            menuName: '新建页面',
            menuShow: true,
            hasChild: false,
        },
        {
            path: '/first',
            menuName: '导航一',
            menuShow: true,
            hasChild: true,
            children: [
                {
                    path: '/first_first',
                    menuName: '选项一'
                },
                {
                    path: '/first_second',
                    menuName: '选项二'
                },
                {
                    path: '/first_third',
                    menuName: '选项三'
                },
            ]
        },
        {
            path: '/second',
            menuName: '导航二',
            menuShow: true,
            hasChild: true,
            children: [
                {
                    path: '/second_first',
                    menuName: '选项一'
                },
                {
                    path: '/second_second',
                    menuName: '选项二'
                },
                {
                    path: '/second_third',
                    menuName: '选项三'
                },
            ]
        },
    ]
});

router.beforeEach((to, from, next) => {
    if (to.matched.length === 0) {
        from.name ? next({name: from.name}) : next('/');
    } else {
        next();
    }
});
export default router
