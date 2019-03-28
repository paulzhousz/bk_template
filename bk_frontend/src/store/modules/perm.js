import * as commonApi from '@/api/api'

const state = {
}

const getters = {
}

const mutations = {
}

const actions = {
  getPermsTree({commit, state}, param) {
    return commonApi.getPermsTree()
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
