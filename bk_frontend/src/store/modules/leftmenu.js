import * as commonApi from '@/api/api'
import * as commonMethods from '@/common/js/common.js'

const state = {
  isAdmin: window.isAdmin === '1', // 管理员
  isGetUserPerm: false, // 获取到当前用户的路由权限
  routerMenuList: [], // 当前用户的路由菜单权限
  permissions: [], // 当前用户的操作权限
  routerList: [], // 当前用户能跳转的路由
}

const getters = {
  isAdmin: state => state.isAdmin,
  isGetUserPerm: state => state.isGetUserPerm,
  routerMenuList: state => state.routerMenuList,
  permissions: state => state.permissions,
  routerList: state => state.routerList
}

const mutations = {
  setIsGetUserPerm(state, isGetUserPerm) {
    state.isGetUserPerm = isGetUserPerm
  },
  setRouterMenuList(state, routerMenuList) {
    state.routerMenuList = routerMenuList
  },
  setPermissions(state, permissions) {
    state.permissions = permissions
  },
  setRouterList(state, routerList) {
    state.routerList = routerList
  },
}

const actions = {
  getMenu ({ commit }, param) {
    return commonApi.getMenu()
  },
  getMenuTree ({ commit }, param) {
    return commonApi.getMenuTree()
  },
  getCurrentPermission ({ commit, state }, param) {
    return commonApi.getCurrentPermission().then(res => {
      if (res.result) {
        commit('setIsGetUserPerm', true)
        // 筛选出菜单类型的数据
        let haveAllMenu = JSON.parse(JSON.stringify(res.data.menus)).filter((item) => {
          if (item.is_menu) {
            return true
          }
        })
        let haveMenuTree = []
        for (let i = 0; i < haveAllMenu.length; i++) {
          if (haveAllMenu[i].parent == null) {
            let haveMenu = commonMethods.pushChildNode(haveAllMenu[i], haveAllMenu)
            haveMenuTree.push(haveMenu)
          }
        }
        commit('setRouterList', res.data.menus)
        commit('setRouterMenuList', haveMenuTree)
        commit('setPermissions', res.data.permissions)
      }
    })
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
