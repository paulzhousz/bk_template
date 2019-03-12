// 引入axios
const axios = require("axios");
// 引入mockjs
const Mock = require("mockjs");
// 获取 mock.Random 对象
const Random = Mock.Random;
// 睡眠时间
const sleep = function (n) {
  let start = new Date().getTime()
  while (true) {
    if (new Date().getTime() - start > n) {
      break
    }
  }
}

// Mock.mock(`${window.siteUrl}qingcloud/get_servers_by_mapping`, "post", get_servers_by_mapping); // 获取指定后端映射可选主机的下拉框数据

// axios.post('qingcloud/get_value_list', {'value_set_id': 'vxnets'}).then(res => {
//   console.log(res)
// })