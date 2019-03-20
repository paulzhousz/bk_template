import Vue from 'vue'
import Router from 'vue-router'
const MonitorPanel = () => import('@/pages/monitor_panel/MonitorPanel')
const Authority = () => import('@/pages/authority/authority')
Vue.use(Router);

let router = new Router({
    routes: [
        {
            path: '/monitor_panel',
            name: '/monitor_panel',
            component: MonitorPanel
        },
        {
            path: '/authority',
            name: '/authority',
            component: Authority
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
