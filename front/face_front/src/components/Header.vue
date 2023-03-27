<template>
<el-menu 
    :default-active="activeIndex"
    mode="horizontal"
    :router="true"
    class="main-menu"
    >
    <el-menu-item index="/">首页</el-menu-item>
    <el-sub-menu>
      <template #title >图像处理</template>
      <el-menu-item index="/findface">人脸识别</el-menu-item>
      <el-menu-item index="/compare" >人脸对比</el-menu-item>
      <el-menu-item index="/landmarks" >人脸精细分割</el-menu-item>
    </el-sub-menu>
    <el-menu-item index="/videoshow">视频流接入</el-menu-item>
    <el-menu-item index="/manage">人脸信息管理</el-menu-item>
    <el-menu-item index="/bootstrap">关于我们</el-menu-item>
  </el-menu>
</template>

<script>
    import { ref } from 'vue'
    export default{
        name: 'Header',
        data(){
            return{
                activeIndex: '/',
            }
        },
        created(){
          console.log(this.$route.path)
          this.activeIndex = this.$route.path
        },
        methods: {

        },
    }
</script>

<style>
  .main-menu{
    font-weight: 600;
  };
</style>