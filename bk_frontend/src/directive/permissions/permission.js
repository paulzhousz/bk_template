import Vue from 'vue'

let perm = Vue => {
  Vue.directive('permission', {
    inserted: function(el, binding, vnode) {
      // 元素刚插入时隐藏
      el.style.display = 'none'
    },
    update: function(el, binding, vnode) {
      let {value, arg} = binding
      for (let i of value) {
        if (i.codename == arg) {
          el.style.display = ''
          return
        }
      }
      el.style.display = 'none'
    },
  })
}

export default perm
