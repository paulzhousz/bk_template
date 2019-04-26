const state = {
  // breadcrumbs: []
  isCollapse: true // 左侧菜单是否收缩
}

const getters = {
  // breadcrumbs: state => state.breadcrumbs
  isCollapse: state => state.isCollapse
}

const mutations = {
  // updateBreadcrumbs (state, breadcrumbs) {
  //   state.breadcrumbs = breadcrumbs
  // },
  setIsCollapse (state, isCollapse) {
    state.isCollapse = isCollapse
  },
}

const actions = {}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
