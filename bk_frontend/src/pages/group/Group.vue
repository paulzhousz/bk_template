<template>
  <div class="group">
    <breadcrumb :to="to"></breadcrumb>
    <div class="contain">
      <div class="search">
        <el-row>
          <el-col :span="6">
            <span class="aglin">角色名：</span>
            <el-input class="aglin-input" size="mini" v-model="inputGroup" placeholder="请输入内容"></el-input>
          </el-col>
          <el-col :span="6">
            <span class="aglin">是否内置：</span>
            <el-select size="mini" v-model="valueIsBuiltIn" clearable placeholder="请选择">
              <el-option
                v-for="(item, index) in optionsIsBuiltIn"
                :key="index"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <span class="aglin">是否启用：</span>
            <el-select size="mini" v-model="valueIsEnable" clearable placeholder="请选择">
              <el-option
                v-for="(item, index) in optionsIsEnable"
                :key="index"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-button size="mini" type="primary" @click.native="search">查询</el-button>
            <el-button size="mini" @click.native="reset">重置</el-button>
          </el-col>
        </el-row>
      </div>
      <div class="new">
        <el-button size="mini" type="primary" @click="handleNew">新建角色</el-button>
      </div>
      <div class="table">
        <el-table
          stripe
          ref=""
          :data="data"
          v-loading="loading"
          style="width: 100%"
          height="100%">
          <!-- <el-table-column
          type="selection"
          width="30">
          </el-table-column> -->
          <el-table-column
          prop="name"
          label="组名"
          show-overflow-tooltip>
          </el-table-column>
          <el-table-column
          prop="display_name"
          label="显示名"
          show-overflow-tooltip>
          </el-table-column>
          <el-table-column
          label="是否内置">
            <template slot-scope="scope">
              <span>{{scope.is_built_in == false ? '否' : '是'}}</span>
            </template>
          </el-table-column>
          <el-table-column
          label="是否禁用">
            <template slot-scope="scope">
              <el-checkbox v-model="scope.is_enable"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column
          prop="description"
          label="描述"
          show-overflow-tooltip>
          </el-table-column>
          <el-table-column
            prop="handle"
            label="操作"
            fixed="right"
            width="150">
            <template slot-scope="scope">
              <el-button type="text" @click="handleEdit(scope)">编辑</el-button>
              <el-button type="text" @click="handleAuthority(scope)">权限</el-button>
              <el-button type="text" @click="handleDelete(scope)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <pagination
        :total="totalNumber"
        @page-size-change="pageSizeChange">
      </pagination>
      <new-edit ref="newEdit" :title="title" @handle-success="handleSuccess" dialog-action="dialogAction">
        <div slot="dialog-content"></div>
      </new-edit>
    </div>
  </div>
</template>

<script>
import Breadcrumb from '@/components/Breadcrumb'
import Pagination from '@/components/Pagination'
import NewEdit from '@/components/NewEdit'
export default {
  components: {
    Breadcrumb,
    Pagination,
    NewEdit
  },
  data() {
    return {
      inputGroup: '',
      title: '',
      dialogAction: '',
      valueIsBuiltIn: undefined,
      valueIsEnable: undefined,
      optionsIsBuiltIn: [
        {value: true, label: '是'},
        {value: false, label: '否'},
      ],
      optionsIsEnable: [
        {value: true, label: '是'},
        {value: false, label: '否'},
      ],
      totalNumber: 0,
      currentPage: 1,
      pageSize: 10,
      loading: false,
      data: [],
      to: [
        {displayName: '系统管理', path: {path: ''}},
        {displayName: '角色管理', path: {path: '/group'}},
      ]
    }
  },
  created() {
    this.search()
  },
  methods: {
    search() {
      let params = {
        page: this.currentPage,
        page_size: this.pageSize,
        is_built_in: this.valueIsBuiltIn,
        is_enable: this.valueIsEnable,
        display_name: this.inputGroup,
        omit: 'menus, permissions'
      }
      this.loading = true
      this.$store.dispatch('group/getGroups', params).then(res => {
        if (res.result) {
          this.loading = false
          this.data = res.data.items
          this.totalNumber = res.data.count
        }
      })
    },
    pageSizeChange(val) {
      this.currentPage = val.currentPage
      this.pageSize = val.pageSize
      this.search({page: this.currentPage, page_size: this.pageSize})
    },
    reset() {
      this.inputGroup = ''
      this.valueIsBuiltIn = undefined
      this.valueIsEnable = undefined
      this.search()
    },
    handleEdit(scope) {
      this.dialogAction = 'edit'
      this.$refs['newEdit'].open()
      this.title = '编辑'
    },
    handleNew() {
      this.dialogAction = 'new'
      this.$refs['newEdit'].open()
      this.title = '新建'
    },
    handleSuccess(dialogAction) {
      this.$refs['newEdit'].cancel()
    },
    handleAuthority(scope) {
    },
    handleDelete(scope) {
    },
  },
}
</script>

<style lang="scss">
  .group {
    padding: 20px 20px 0 20px;
    height: calc(100% - 20px);
    width: 100%;
    .contain {
      height: calc(100% - 33px);
      padding: 20px;
      background: #fff;
      .search {
        height: 50px;
        line-height: 50px;
        .aglin-input {
          width: 60%;
        }
      }
      .new {
        height: 40px;
      }
      .table {
        height: calc(100% - 110px);
        .el-table {
          border-top: 1px solid rgb(235, 238, 245);
        }
      }
    }
  }
</style>
