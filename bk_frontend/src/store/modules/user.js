import * as commonApi from '@/api/api'

const state = {
}

const getters = {
}

const mutations = {
}

const actions = {
  getTableUser({commit, state}) {
    return commonApi.getTableUser()
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
