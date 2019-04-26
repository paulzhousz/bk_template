/*表单验证规则 */

/**
 * 校验由英文和下划线组成
 */
export function validateNameUnderline(rule, value, callback) {
  if (/^[a-zA-Z0-9_]+$/.test(value)) {
    callback()
  } else {
    callback(new Error('只能由英文、数字、下划线组成'))
  }
}

/**
 * 校验中文
 */
export function validateChName(rule, value, callback) {
  if (/^[\u4e00-\u9fa50-9a-zA-Z_]+$/.test(value)) {
    callback()
  } else {
    callback(new Error('只能由中文、英文、数字、或者下划线组成'))
  }
}

/**
 * 检查字数长度
 */
export function checkLength(value, min, max) {
  let valueLength = value.length
  if (valueLength >= min && valueLength <= max) {
    return true
  } else {
    return false
  }
}

/**
 * 手机号匹配
 */
export function matchPhoneNum(rule, value, cb) {
  if (value) {
    if (/^1[3|4|5|8][0-9]\d{4,8}$/.test(value) && value.length == 11) {
      cb()
    } else {
      cb(new Error('只能为手机号格式'))
    }
  } else {
    cb(new Error('手机号不能为空'))
  }
}
