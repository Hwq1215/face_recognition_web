<template>
<div>
    <el-upload
      class="upload-demo"
      :action="actionUrl"
      drag="true"
      :http-request="httpRequest"
      :on-preview="handlePreview"
      v-model:file-list="fileList2"
      list-type="picture">
      <el class="drag-item">
        <h3>拖拽图片到这</h3>
        <h5>- 或 -</h5>
        <h3>点此上传</h3></el>
    <el-dialog v-model="dialogIsVisible"  :append-to-body="true" :close-on-click-modal="false">
      <img w-full style="width:100%" :src="produce_imgs">
    </el-dialog>
    </el-upload>
</div>
    </template>
<script >
import axios from 'axios'
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { httpurl } from '@/config'

export default {
    data() {
        return {
        fileList2: [],
        actionUrl: httpurl+"/findface",
        produce_imgs: '',
        dialogIsVisible: false,
    }},
    components:{
        Plus
    },
    methods: {
        handleRemove(file, fileList) {
        console.log(file);
        console.log(this.fileList2);
        },
        handlePreview(file) {
        console.log(file);
        this.produce_imgs = file.response.data;
        this.dialogIsVisible = true;
        },
        httpRequest(options){
        // console.log(options)
        let fd = new FormData();
        fd.append('imgfile', options.file);
        this.fileList2.join({name:options.file.name,url:options.file.url});
        var ax = axios({
            method:'post',
            url:options.action,
            headers:{'Content-Type':'multipart/form-data',
                    "Access-Control-Allow-Origin": "*"},
            data:fd,
        }) 
        return ax;
        },
    }
    }
</script>

<style>
    .drag-item{
        font-size: medium;
        background-color: #f5f7fa;
    }
</style>