import * as commonApi from '@/api/api'

const state = {
}

const getters = {
}

const mutations = {
}

const actions = {
  getMenu ({ commit, state }, param) {
    return commonApi.getMenu()
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
