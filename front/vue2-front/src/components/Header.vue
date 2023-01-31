<template>
<el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
  <el-menu-item index="1">首页</el-menu-item>
  <el-submenu index="2">
    <template slot="title">我的工作台</template>
    <el-menu-item index="2-1">选项1</el-menu-item>
    <el-menu-item index="2-2">选项2</el-menu-item>
    <el-menu-item index="2-3">选项3</el-menu-item>
    <el-submenu index="2-4">
      <template slot="title">选项4</template>
      <el-menu-item index="2-4-1">选项1</el-menu-item>
      <el-menu-item index="2-4-2">选项2</el-menu-item>
      <el-menu-item index="2-4-3">选项3</el-menu-item>
    </el-submenu>+
  </el-submenu>
  <el-menu-item index="3" >消息中心</el-menu-item>
  <el-menu-item index="4"><a href="https://www.ele.me" target="_blank">关于我们</a></el-menu-item>
</el-menu>

</template>

<script>
export default{
    name: 'Header',
    data(){
        return{
            activeIndex: '1',
            activeIndex2: '1'
        }
    },
    methods: {
        handleSelect(key, keyPath) {
          console.log(key, keyPath);
        },
      },
}
</script>