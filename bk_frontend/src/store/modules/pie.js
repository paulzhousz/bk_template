import * as commonApi from '@/api/api'

const state = {
}

const getters = {
}

const mutations = {
}

const actions = {
  getTaskState({commit, state}) {
    return commonApi.getTaskState()
  },
  getServerSelect({commit, state}) {
    return commonApi.getServerSelect()
  },
  getServerPerformance({commit, state}, param) {
    return commonApi.getServerPerformance(param)
  },
  getBizServer({commit, state}) {
    return commonApi.getBizServer()
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
