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
  },
  addUser({commit, state}, param) {
    return commonApi.addUser(param)
  },
  editUser({commit, state}, param) {
    return commonApi.editUser(param)
  },
  deleteUser({commit, state}, param) {
    return commonApi.deleteUser(param)
  },
  usersStatus({commit, state}, param) {
    return commonApi.usersStatus(param)
  },
  getUserAuthority({commit, state}, param) {
    return commonApi.getUserAuthority(param)
  },
  getAllGroup({commit, state}) {
    return commonApi.getAllGroup()
  },
  setUserPerm({commit, state}, param) {
    return commonApi.setUserPerm(param)
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
