import * as commonApi from '@/api/api'
import * as commonMethods from '@/common/js/common.js'

const state = {
  isAdmin: window.isAdmin === '1', // 管理员
  isGetUserPerm: false, // 获取到当前用户的路由权限
  routerMenuList: [], // 当前用户的路由菜单权限
  permissions: [], // 当前用户的操作权限
}

const getters = {
  isAdmin: state => state.isAdmin,
  isGetUserPerm: state => state.isGetUserPerm,
  routerMenuList: state => state.routerMenuList,
  permissions: state => state.permissions
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
}

const actions = {
  getMenu ({ commit }, param) {
    return commonApi.getMenu()
  },
  getMenuTree ({ commit }, param) {
    return commonApi.getMenuTree()
  },
  getCurrentPermission ({ commit }, param) {
    return commonApi.getCurrentPermission().then(res => {
      if (res.result) {
        commit('setIsGetUserPerm', true)
        let haveAllMenu = res.data.menus
        let haveMenuTree = []
        for (let i = 0; i < haveAllMenu.length; i++) {
          if (haveAllMenu[i].parent == null) {
            let haveMenu = commonMethods.pushChildNode(haveAllMenu[i], haveAllMenu)
            haveMenuTree.push(haveMenu)
          }
        }
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
