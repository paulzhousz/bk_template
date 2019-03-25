import * as commonApi from '@/api/api'

const state = {
}

const getters = {
}

const mutations = {
}

const actions = {
  getGroups({commit, state}, param) {
    return commonApi.getGroups(param)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
