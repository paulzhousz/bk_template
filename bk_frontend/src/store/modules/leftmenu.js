import * as commonApi from '@/api/api'

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
  getMenu ({ commit, state }, param) {
    return commonApi.getMenu()
  },
  getCurrentPermission ({ commit }, param) {
    return commonApi.getCurrentPermission().then(res => {
      if (res.result) {
        commit('setIsGetUserPerm', true)
        commit('setRouterMenuList', res.data.menus)
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
