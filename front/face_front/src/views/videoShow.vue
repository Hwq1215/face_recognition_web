<template>
    <div>
        <el-button type="primary" @click="dialogImageUrl = true">视频流链接地址</el-button>
        <div class="img-container">
        
        <el-dialog v-model="dialogImageUrl">
            <el-form>
                <el-form-item label="视频流链接地址">
                    <el-input v-model="videoUrl"></el-input>
                </el-form-item>
            <el-form-item label="是否开启反欺诈">
                <el-switch v-model="isOpenFAS" />
            </el-form-item>
            <el-form-item >
                <el-button type="primary" @click="openVideo" >确认</el-button>
                <el-button type="danger" @click="dialogImageUrl = false" >取消</el-button>
            </el-form-item>
            </el-form>
        </el-dialog>
        <img  v-if="videoShow" class="index-img" :src="requestUrl" alt="">
        </div>
    </div>

</template>

<script>
import { httpurl } from '@/config'

export default{
    name: 'videoShow',
    data(){
        return{
            dialogImageUrl: true,
            videoShow : false,
            videoUrl:'',
            actionUrl: httpurl+'/webvideo',
            requestUrl: '',
            isOpenFAS: true
    }
    },
    created(){
        this.dialogImageUrl = true
    },
    methods:{
        openVideo(){
            this.videoShow = false
            this.requestUrl = encodeURI(this.actionUrl + '?url=' + encodeURIComponent(this.videoUrl)) + '&' + 'isopenfas=' +  + this.isOpenFAS
            console.log(this.requestUrl)
            this.videoShow = true
            this.dialogImageUrl = false
            
        },
        
    }
}
</script>

<style>
    .img-container{
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .index-img{
        max-width: 1400px;
        max-width: 530px;
    }
</style>