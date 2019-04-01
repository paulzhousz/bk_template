import * as commonApi from '@/api/api'

const state = {
}

const getters = {
}

const mutations = {
}

const actions = {
  getTableUser({commit, state}, param) {
    return commonApi.getTableUser(param)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
