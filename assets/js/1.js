webpackJsonp([1],{A8gV:function(t,e){},PisC:function(t,e){},cMGX:function(t,e,a){"use strict";var i={data:function(){return{currentPage:1,pageSize:10,pager:5}},props:{total:Number},methods:{handleSizeChange:function(t){this.pageSize=t,this.$emit("page-size-change",{pageSize:this.pageSize,currentPage:this.currentPage})},handleCurrentChange:function(t){this.currentPage=t,this.$emit("page-size-change",{pageSize:this.pageSize,currentPage:this.currentPage})}}},n={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"pagination"}},[e("el-pagination",{attrs:{"current-page":this.currentPage,"page-sizes":[10,20,50,100],"pager-count":this.pager,layout:"total, sizes, prev, pager, next, jumper",total:this.total},on:{"size-change":this.handleSizeChange,"current-change":this.handleCurrentChange}})],1)},staticRenderFns:[]};var s=a("C7Lr")(i,n,!1,function(t){a("PisC")},null,null);e.a=s.exports},l0np:function(t,e,a){"use strict";var i={props:{title:{type:String,default:""},width:{type:String,default:""},dialogAction:{type:String,default:""}},data:function(){return{isShow:!1}},methods:{open:function(){this.isShow=!0},confirm:function(){this.$emit("handle-success",this.dialogAction)},cancel:function(){this.isShow=!1}}},n={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"dialog"},[a("el-dialog",{attrs:{title:t.title,visible:t.isShow,width:t.width},on:{"update:visible":function(e){t.isShow=e}}},[t._t("dialog-content"),t._v(" "),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{attrs:{type:"primary",size:"mini"},on:{click:t.confirm}},[t._v("确 定")]),t._v(" "),a("el-button",{attrs:{size:"mini"},on:{click:t.cancel}},[t._v("取 消")])],1)],2)],1)},staticRenderFns:[]};var s=a("C7Lr")(i,n,!1,function(t){a("A8gV")},null,null);e.a=s.exports},lJZH:function(t,e){},xD9o:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=a("HzJ8"),n=a.n(i),s=a("3cXf"),r=a.n(s),o=a("cMGX"),l=a("l0np");function c(t,e,a){/^[a-zA-Z0-9_]+$/.test(e)?a():a(new Error("只能由英文、数字、下划线组成"))}function u(t,e,a){/^[\u4e00-\u9fa50-9a-zA-Z_]+$/.test(e)?a():a(new Error("只能由中文、英文、数字、或者下划线组成"))}a("CaOM");var h={components:{pagination:o.a,"new-edit":l.a},data:function(){return{inputGroup:"",title:"",dialogAction:"",activeName:"first",width:"40%",valueIsBuiltIn:void 0,valueIsEnable:void 0,labelPosition:"right",totalNumber:0,currentPage:1,pageSize:10,loadingGroup:!1,loadingLeft:!1,loadingRight:!1,cacheLeftData:[],cacheRightData:[],data:[],leftData:[],rightData:[],formGroups:{name:"",display_name:"",users:[],desc:""},rulesGroups:{name:[{required:!0,message:"请输入组名"},{max:20,message:"长度在20个字符之内"},{validator:c}],display_name:[{required:!0,message:"请输入显示名"},{max:14,message:"长度在14个字符之内"},{validator:u}]},optionsIsBuiltIn:[{value:!0,label:"是"},{value:!1,label:"否"}],optionsIsEnable:[{value:!0,label:"是"},{value:!1,label:"否"}]}},created:function(){this.search()},methods:{search:function(){var t=this,e={page:this.currentPage,page_size:this.pageSize,is_built_in:this.valueIsBuiltIn,is_enable:this.valueIsEnable,display_name:this.inputGroup,omit:"menus,permissions"};this.loadingGroup=!0,this.$store.dispatch("group/getGroups",e).then(function(e){e.result&&(t.loadingGroup=!1,t.data=e.data.items,t.totalNumber=e.data.count)})},pageSizeChange:function(t){this.currentPage=t.currentPage,this.pageSize=t.pageSize,this.search({page:this.currentPage,page_size:this.pageSize})},reset:function(){this.inputGroup="",this.valueIsBuiltIn=void 0,this.valueIsEnable=void 0,this.search()},handleEdit:function(t){this.activeName="first",this.dialogAction="edit",this.title="编辑",this.$refs.newEdit.open(),this.formGroups=JSON.parse(r()(t.row)),this.formGroups.users=this.formGroups.users.map(function(t){return t.id}),this.rightData=t.row.users,this.leftData=[],this.getLeftUser()},leaveTab:function(t){var e=!0;return this.$refs.refformGroups.validate(function(t){e=!!t}),e},handleNew:function(){var t=this;this.activeName="first",this.dialogAction="new",this.title="新建",this.$refs.newEdit.open(),this.$nextTick(function(){t.$refs.refformGroups.clearValidate()}),this.leftData=[],this.rightData=[],this.getLeftUser(),this.formGroups={}},checkboxChange:function(t){var e=this,a=t.is_enable?"是否启用":"是否禁用";this.$confirm(a,"提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){if(1==t.is_enable){var a={groups:[t.id],enable:!0};e.$store.dispatch("group/groupsStatus",a).then(function(a){a.result?e.$message({type:"success",message:"禁用成功"}):(t.is_enable=!t.is_enable,e.$message({type:"error",message:"禁用失败"}))})}else if(0==t.is_enable){var i={groups:[t.id],enable:!1};e.$store.dispatch("group/groupsStatus",i).then(function(a){a.result?e.$message({type:"success",message:"启用成功"}):(t.is_enable=!t.is_enable,e.$message({type:"error",message:"启用失败"}))})}}).catch(function(){t.is_enable=!t.is_enable,e.$message({type:"info",message:"调取接口失败"})})},handleAuthority:function(t){this.$router.push(t)},handleSuccess:function(t){var e=this;if("new"==this.dialogAction){var a={name:this.formGroups.name,description:this.formGroups.desc,users:this.formGroups.users};this.$store.dispatch("group/addGroups",a).then(function(t){t.result?(e.search(),e.$message({type:"success",message:"新建成功"})):e.$message({type:"error",message:"新建失败"})}).catch(function(){e.$message({type:"info",message:"接口调用失败"})})}else if("edit"==this.dialogAction){this.rightDataId=this.rightData.map(function(t){return t.id}),this.formGroups.users=this.rightDataId;var i=this.formGroups;this.$store.dispatch("group/editGroups",i).then(function(t){t.result?(e.search(),e.$message({type:"success",message:"编辑成功"})):e.$message({type:"error",message:"编辑失败"})}).catch(function(){e.$message({type:"info",message:"接口调用失败"})})}this.$refs.newEdit.cancel()},handleDelete:function(t){var e=this;this.$confirm("此操作将永久删除, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){var a={id:t.row.id};e.$store.dispatch("group/deleteGroups",a).then(function(t){t.result?(e.search(),e.$message({type:"success",message:"删除成功"})):e.$message({type:"error",message:"删除失败"})})}).catch(function(){e.$message({type:"info",message:"已取消"})})},getLeftUser:function(){var t=this;this.$store.dispatch("group/getAllUser").then(function(e){e.result&&("new"==t.dialogAction?t.leftData=e.data:"edit"==t.dialogAction&&(t.leftData=e.data.filter(function(e){var a=!0,i=!1,s=void 0;try{for(var r,o=n()(t.rightData);!(a=(r=o.next()).done);a=!0){var l=r.value;if(e.id==l.id)return!1}}catch(t){i=!0,s=t}finally{try{!a&&o.return&&o.return()}finally{if(i)throw s}}return!0})))})},turnRightItems:function(){this.rightData.push.apply(this.rightData,this.cacheLeftData);var t=0,e=!0,a=!1,i=void 0;try{for(var s,r=n()(this.cacheLeftData);!(e=(s=r.next()).done);e=!0){var o=s.value;this.leftData.splice(o.rowIndex-t,1),t++}}catch(t){a=!0,i=t}finally{try{!e&&r.return&&r.return()}finally{if(a)throw i}}this.cacheLeftData=[]},turnLeftItems:function(){this.leftData.push.apply(this.leftData,this.cacheRightData);var t=0,e=!0,a=!1,i=void 0;try{for(var s,r=n()(this.cacheRightData);!(e=(s=r.next()).done);e=!0){var o=s.value;this.rightData.splice(o.indexRight-t,1),t++}}catch(t){a=!0,i=t}finally{try{!e&&r.return&&r.return()}finally{if(a)throw i}}this.cacheRightData=[]},handleLeftChange:function(t){this.cacheLeftData=t},handleRightChange:function(t){this.cacheRightData=t},leftRow:function(t){var e=t.row,a=t.rowIndex;e.rowIndex=a},rightRow:function(t){var e=t.row,a=t.rowIndex;e.rowIndex=a}},computed:{leftButtonColor:function(){return 0!=this.leftData.length},rightButtonColor:function(){return 0!=this.rightData.length}}},p={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"group"},[a("div",{staticClass:"search"},[a("el-row",[a("el-col",{attrs:{span:6}},[a("span",{staticClass:"aglin"},[t._v("角色名：")]),t._v(" "),a("el-input",{staticClass:"aglin-input",attrs:{size:"mini",clearable:"",placeholder:"请输入内容"},model:{value:t.inputGroup,callback:function(e){t.inputGroup=e},expression:"inputGroup"}})],1),t._v(" "),a("el-col",{attrs:{span:6}},[a("span",{staticClass:"aglin"},[t._v("是否内置：")]),t._v(" "),a("el-select",{attrs:{size:"mini",clearable:"",placeholder:"请选择"},model:{value:t.valueIsBuiltIn,callback:function(e){t.valueIsBuiltIn=e},expression:"valueIsBuiltIn"}},t._l(t.optionsIsBuiltIn,function(t,e){return a("el-option",{key:e,attrs:{label:t.label,value:t.value}})}),1)],1),t._v(" "),a("el-col",{attrs:{span:6}},[a("span",{staticClass:"aglin"},[t._v("是否启用：")]),t._v(" "),a("el-select",{attrs:{size:"mini",clearable:"",placeholder:"请选择"},model:{value:t.valueIsEnable,callback:function(e){t.valueIsEnable=e},expression:"valueIsEnable"}},t._l(t.optionsIsEnable,function(t,e){return a("el-option",{key:e,attrs:{label:t.label,value:t.value}})}),1)],1),t._v(" "),a("el-col",{attrs:{span:6}},[a("el-button",{attrs:{size:"mini",type:"primary"},nativeOn:{click:function(e){return t.search(e)}}},[t._v("查询")]),t._v(" "),a("el-button",{attrs:{size:"mini"},nativeOn:{click:function(e){return t.reset(e)}}},[t._v("重置")])],1)],1)],1),t._v(" "),a("div",{staticClass:"new"},[a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:t.handleNew}},[t._v("新建角色")])],1),t._v(" "),a("div",{staticClass:"table"},[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.loadingGroup,expression:"loadingGroup"}],ref:"",staticStyle:{width:"100%"},attrs:{stripe:"",data:t.data,height:"100%"}},[a("el-table-column",{attrs:{prop:"name",label:"组名","show-overflow-tooltip":""}}),t._v(" "),a("el-table-column",{attrs:{prop:"display_name",label:"显示名","show-overflow-tooltip":""}}),t._v(" "),a("el-table-column",{attrs:{label:"是否内置"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",[t._v(t._s(0==e.is_built_in?"否":"是"))])]}}])}),t._v(" "),a("el-table-column",{attrs:{label:"是否启用"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-checkbox",{on:{change:function(a){return t.checkboxChange(e.row)}},model:{value:e.row.is_enable,callback:function(a){t.$set(e.row,"is_enable",a)},expression:"scope.row.is_enable"}})]}}])}),t._v(" "),a("el-table-column",{attrs:{prop:"description",label:"描述","show-overflow-tooltip":""}}),t._v(" "),a("el-table-column",{attrs:{prop:"handle",label:"操作",fixed:"right",width:"150"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-button",{attrs:{type:"text"},on:{click:function(a){return t.handleEdit(e)}}},[t._v("编辑")]),t._v(" "),a("el-button",{attrs:{type:"text"},on:{click:function(a){return t.handleAuthority({name:"permission",params:{group_id:e.row.id}})}}},[t._v("权限")]),t._v(" "),a("el-button",{attrs:{type:"text"},on:{click:function(a){return t.handleDelete(e)}}},[t._v("删除")])]}}])})],1)],1),t._v(" "),a("pagination",{attrs:{total:t.totalNumber},on:{"page-size-change":t.pageSizeChange}}),t._v(" "),a("new-edit",{ref:"newEdit",attrs:{title:t.title,"dialog-action":"dialogAction",width:t.width},on:{"handle-success":t.handleSuccess}},[a("div",{attrs:{slot:"dialog-content"},slot:"dialog-content"},[a("el-tabs",{attrs:{"before-leave":t.leaveTab},model:{value:t.activeName,callback:function(e){t.activeName=e},expression:"activeName"}},[a("el-tab-pane",{attrs:{label:"角色信息",name:"first"}},[a("el-form",{ref:"refformGroups",attrs:{"label-position":t.labelPosition,"label-width":"120px",model:t.formGroups,rules:t.rulesGroups}},[a("el-form-item",{attrs:{label:"组名",prop:"name"}},[a("el-input",{staticClass:"form-content",attrs:{size:"mini"},model:{value:t.formGroups.name,callback:function(e){t.$set(t.formGroups,"name",e)},expression:"formGroups.name"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"显示名",prop:"display_name"}},[a("el-input",{staticClass:"form-content",attrs:{size:"mini"},model:{value:t.formGroups.display_name,callback:function(e){t.$set(t.formGroups,"display_name",e)},expression:"formGroups.display_name"}})],1),t._v(" "),a("el-form-item",{attrs:{label:"描述"}},[a("el-input",{staticClass:"form-content",attrs:{type:"textarea"},model:{value:t.formGroups.desc,callback:function(e){t.$set(t.formGroups,"desc",e)},expression:"formGroups.desc"}})],1)],1)],1),t._v(" "),a("el-tab-pane",{attrs:{label:"分配用户",name:"second"}},[a("div",[a("el-row",[a("el-col",{attrs:{span:10}},[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.loadingLeft,expression:"loadingLeft"}],staticStyle:{width:"100%","margin-bottom":"0px"},attrs:{data:t.leftData,border:"",height:"280","row-class-name":t.leftRow},on:{"selection-change":t.handleLeftChange}},[a("el-table-column",{attrs:{type:"selection",prop:"value"}}),t._v(" "),a("el-table-column",{attrs:{prop:"username",label:"用户名"}}),t._v(" "),a("el-table-column",{attrs:{prop:"chname",label:"中文名","show-overflow-tooltip":""}})],1)],1),t._v(" "),a("el-col",{attrs:{span:4}},[a("div",{staticStyle:{"margin-top":"100%","margin-left":"25%","margin-right":"25%"}},[t.leftButtonColor?a("el-button",{attrs:{size:"mini",type:"primary",icon:"icon el-icon-d-arrow-right"},on:{click:t.turnRightItems}}):t._e(),t._v(" "),t.leftButtonColor?t._e():a("el-button",{attrs:{type:"info",disabled:"",size:"mini",icon:"icon el-icon-d-arrow-right"}}),t._v(" "),t.rightButtonColor?a("el-button",{staticStyle:{margin:"5px 0 0 0"},attrs:{size:"mini",type:"primary",icon:"icon el-icon-d-arrow-left"},on:{click:t.turnLeftItems}}):t._e(),t._v(" "),t.rightButtonColor?t._e():a("el-button",{staticClass:"not-have",staticStyle:{margin:"5px 0 0 0"},attrs:{type:"info",disabled:"",size:"mini",icon:"icon el-icon-d-arrow-left"}})],1)]),t._v(" "),a("el-col",{attrs:{span:10}},[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.loadingRight,expression:"loadingRight"}],staticStyle:{width:"100%","margin-bottom":"0px"},attrs:{data:t.rightData,height:"280",border:"","row-class-name":t.rightRow},on:{"selection-change":t.handleRightChange}},[a("el-table-column",{attrs:{type:"selection",prop:"value"}}),t._v(" "),a("el-table-column",{attrs:{label:"用户名",prop:"username"}}),t._v(" "),a("el-table-column",{attrs:{prop:"chname",label:"中文名","show-overflow-tooltip":""}})],1)],1)],1)],1)])],1)],1)])],1)},staticRenderFns:[]};var f=a("C7Lr")(h,p,!1,function(t){a("lJZH")},null,null);e.default=f.exports}});
//# sourceMappingURL=1.js.map