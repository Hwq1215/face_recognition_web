<template>
<div>
    <el-upload
      class=""
      action="http://127.0.0.1:5006/findface"
      :http-request="httpRequest"
      :on-preview="handlePreview"
      :file-list="fileList2"
      list-type="picture">
      <el-button size="small" type="primary">点击上传</el-button>
      <el-dialog :visible.sync="dialogIsVisible" :append-to-body="true" :close-on-click-modal="false">
        <img style="width: 100%;" :src="produce_imgs">
    </el-dialog>
    </el-upload>
</div>
</template>
<script >
import axios from 'axios'

export default {
    name: 'findface',
    data() {
        return {
        fileList2: [],
        produce_imgs: '',
        dialogIsVisible: false,
    }},
    components:{
        
    },
    methods: {
        handleRemove(file, fileList) {
        console.log(file);
        console.log(this.fileList2);
        },
        handlePreview(file) {
        // console.log(file.response.data);
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