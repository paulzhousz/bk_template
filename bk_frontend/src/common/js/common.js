/*
* 公共函数
*/

/**
 * 树状数据递归 获取完整的树状结构数据
 * @params parentNode - 所有第一层的数据对象
 * @params allNode - 所有层级的数据对象
 * @params parent - 父级数据对象的key
 * @params key - 每个数据对象的唯一标识符
 * @return parentNode - 处理好的树状数据结构
*/
export function pushChildNode(parentNode, allNode, parent = 'parent', key = 'id') {
  parentNode.children = []
  for (let node of allNode) {
    if (node[parent] == parentNode[key]) {
      parentNode.children.push(node)
    }
  }
  for (let node of parentNode.children) {
    pushChildNode(node, allNode, parent, key)
  }
  return parentNode
}

// export function pushChildNode (parentNode, allNode, parent = 'parent', key = 'id') {
//   parentNode.children = []
//   allNode.forEach((node) => {
//     if (node[parent] == parentNode[key]) {
//       parentNode.children.push(node)
//     }
//   })
//   parentNode.children.forEach((node) => {
//     pushChildNode(node, allNode, parent, key)
//   })
//   return parentNode
// }
