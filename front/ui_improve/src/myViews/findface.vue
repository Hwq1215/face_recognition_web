<template>

        <div class="top-box">
    <h4>
        开启欺诈识别<el-switch v-model="isOpenFAS"></el-switch>
    </h4>
    <h4>
        开启关键点标识<el-switch v-model="isOpenLandmarks"></el-switch>
    </h4>
        <!-- <el-button type="success" size="large" class="top-button" @click="slice">asd</el-button> -->
    <el-button type="success"  class="top-button" @click="handleRecord()">录制 <el-icon><VideoCamera /></el-icon></el-button>
</div>
<div>

    <el-upload
      class="upload-demo"
      :action="actionUrl"
      drag="true"
      ref="upload-ref"
      auto-upload="true"
      :http-request="httpRequest"
      :on-preview="handlePreview"
      v-model:file-list="fileList2"
      list-type="picture">
      <el class="drag-item">
        <h3>拖拽图片到这</h3>
        <h5>- 或 -</h5>
        <h3>点此上传</h3></el>
    <el-dialog v-model="dialogIsVisible"  :append-to-body="true" :close-on-click-modal="false" :lock-scroll="true" class="img-dialog">
        <div class="img-block">
            <img w-full  :src="previewContent.imgUrl">
                <span>识别结果由从左到右排序，分别为</span>
                <div v-for="item in previewContent.names">
                    <span>{{item}},</span>
                </div>
        </div>
        
    </el-dialog>
    </el-upload>

    <!-- <div class="side-box">
        <el-button>
        <el-icon><Plus /></el-icon>
        </el-button>
    </div> -->
</div>

<el-dialog v-model="VideoDialogIsVisiable">
    <video-reader @choose-img="uploadImg()" ref="video-reader">
        <!-- <template #second-btn>
            <el-button type="warning" @click="">查看</el-button>
        </template> -->
    </video-reader>
</el-dialog>
    </template>
<script lang="js">
import axios from 'axios'
import { Plus } from '@element-plus/icons-vue'
import { httpurl } from '../config'
import VideoReader from '../mycomponents/VideoReader.vue'

export default {
    data(){
        return {
        fileList2: [],
        actionUrl: httpurl+"/findface",
        produce_result: {},
        dialogIsVisible: false,
        isOpenFAS: true,
        isOpenLandmarks: true,
        VideoDialogIsVisiable: false,
     }
    },
    computed: {
        previewContent(){
            return {
               "imgUrl":this.produce_result.imgUrl,
               "names": this.produce_result.names.map((item)=>{
                    return item == 'unknown' ? '未知' : item;
               })
            }
        },
    },
    components:{
        VideoReader,
        Plus,
    },
    methods: {
        handleRemove(file, fileList) {
        console.log(file);
        console.log(this.fileList2);
        },
        handlePreview(file) {
        console.log(file);
        this.produce_result = file.response.data;
        this.dialogIsVisible = true;
        },

        async httpRequest(options){
        console.log(options)
        let fd = new FormData();
        fd.append('imgfile', options.file);
        var ax = axios({
            method:'post',
            url:options.action+"?isopenfas="+this.isOpenFAS+"&isopenlandmarks="+this.isOpenLandmarks,
            headers:{'Content-Type':'multipart/form-data',
                    "Access-Control-Allow-Origin": "*"},
            data:fd,
        }) 
        return ax;
        },
        handleRecord(){
            this.VideoDialogIsVisiable = true;
        },
        async uploadImg(){
            var imgUrl = this.$refs['video-reader'].imgUrl;
            var img = this.$refs['video-reader'].imgFile;
            if(imgUrl == '' || imgUrl == null || imgUrl == undefined){
                this.$message.error('请先拍照');
                return;
            }
            if(img == '' || img == null || img == undefined){
                this.$message.error('请先拍照');
                return;
            }
            console.log(img);
            let fd = new FormData();
            fd.append('imgfile',img);
            var ax = axios({
            method:'post',
            url:this.actionUrl+"?isopenfas="+this.isOpenFAS+"&isopenlandmarks="+this.isOpenLandmarks,
            headers:{'Content-Type':'multipart/form-data',
                    "Access-Control-Allow-Origin": "*"},
            data:fd,
            })
            this.fileList2.push({
                name: "cut.png",
                percentage: 0,
                status: 'success',
                size: img.size,
                uid: 0,
                url: imgUrl,
                response: {
                    data: await ax.then(res => res.data),
                },
                raw: new File([img],'cut_img', {type:'image/png', lastModified: Date.now()})
            });
            this.VideoDialogIsVisiable = false;
        },
    }
    }
</script>

<style>
    .drag-item{
        font-size: medium;
        background-color: #f5f7fa;
    }
    .top-box{
        width: 100%;
        height: 100%;   
        display: flex;
        background-color: #ffffff;
        font-size: large;
        align-items: center;
    }
    .top-box h4{
        margin-left: 3%;
    }
    .top-box .top-button{
        margin-left: 5%;
    }
    .father-box{
        width: 100%;
        height: 100%;
        display: flex;
    }
    .record-button{
        width: 100px;
    }
    .upload-demo{
        width: 100%;
        height: 100%;
        margin-bottom: 300px;
    }
    .img-dialog{
        height: auto;
        width: 100%;
        text-align: center;
        align-items: center;
        justify-content: center;
    }
    .img-dialog .img-block{
        text-align: center;
        align-items: center;
        justify-content: center;
    }
    .img-block img{
        max-width: 350px;
        max-height: 350px;
        margin: 0 auto;
    }

    ::v-deep .el-dialog{
       display: flex;
       flex-direction: column;
       margin:0 !important;
       position:absolute;
       top:50%;
       left:50%;
       transform:translate(-50%,-50%);
       max-height:calc(100% - 30px);
       max-width:calc(100% - 30px);
   }
  ::v-deep  .el-dialog .el-dialog__body{
       flex:1;
       overflow: auto;
   }
</style>