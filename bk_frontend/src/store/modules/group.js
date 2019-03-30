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
  },
  editGroups({commit, state}, param) {
    return commonApi.editGroups(param)
  },
  addGroups({commit, state}, param) {
    return commonApi.addGroups(param)
  },
  getAllUser({commit, state}, param) {
    return commonApi.getAllUser()
  },
  deleteGroups({commit, state}, param) {
    return commonApi.deleteGroups(param)
  },
  groupsStatus({commit, state}, param) {
    return commonApi.groupsStatus(param)
  },
  getAuthority({commit, state}, param) {
    return commonApi.getAuthority(param)
  },
  getPermsTree({commit, state}, param) {
    return commonApi.getPermsTree(param)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
