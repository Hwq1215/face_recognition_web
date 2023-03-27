<template>
    <div class="video-box">
        <video ref="video-play" class="video-play"></video>
        <div v-if="imgExist" class="side-box">
            <el-button class="" type="primary" @click="getImg()">录制</el-button>
            <div class="img-box">
                <img  v-if="imgUrl" :src="imgUrl" ref="cut-img"  />
                <el-icon v-else class="img-icon"><Picture /></el-icon>
            </div>
            <div class="btn-place">
                <el-button class="" type="success" @click="$emit('choose-img',1)">选定</el-button>
                <slot name="second-btn"></slot>
            </div>
        </div>
    </div>
    
</template>

<script>
export default{
    name:'video-reader',
    props:{
        imgExist:{
            type:Boolean,
            default: true, 
        }
    },
    data(){
        return{
            constraints:{
                audio:false,
                video:true
            },
            imgUrl: "",
            imgFile: "",
        }
    },
    created(){
        this.getVedioStream();
    },
    methods:{
        getVedioStream(){
            navigator.mediaDevices.getUserMedia(this.constraints)
            .then(stream=>{
                var videoObj = this.$refs['video-play'];
                videoObj.srcObject = stream;
                videoObj.play();
                
            })
            .catch(err=>{
                console.log(err);
            })
        },
        getImg(){
            var videoObj = this.$refs['video-play'];
            var img = this.$refs['cut-img'];
            var canvas = document.createElement("canvas");
            canvas.width = videoObj.videoWidth;
            canvas.height = videoObj.videoHeight;
            console.log()
            const ctx = canvas.getContext("2d");
            ctx.drawImage(videoObj, 0, 0, videoObj.videoWidth, videoObj.videoHeight);
            const base64 = canvas.toDataURL('image/png');
            // console.log(base64);
            this.imgUrl = base64;
            this.imgFile = this.convertBase64UrlToImgFile(base64, 'cut.png', 'image/png');
            console.log(this.imgFile);
        },
        convertBase64UrlToImgFile(urlData, fileName, fileType) {
            //去掉base64的头信息，转换为byte
            urlData = urlData.replace(/^data:image\/\w+;base64,/, "");
            var bytes = window.atob(urlData); //转换为byte
            //处理异常,将ascii码小于0的转换为大于0
            var ab = new ArrayBuffer(bytes.length);
            var ia = new Int8Array(ab);
            var i;
            for (i = 0; i < bytes.length; i++) {
                ia[i] = bytes.charCodeAt(i);
            }
            //转换成文件，添加文件的type，name，lastModifiedDate属性
            var blob = new Blob([ab], { type: fileType });
            blob.lastModifiedDate = new Date();
            blob.name = fileName;
            return blob;
    },

    }
}
</script>

<style>
    
    .video-box{
        display: flex;
        height: 400px;
    }
    .video-box .video-play{
        width: 60%;
        height: 100%;
    }
    .video-box .side-box{
        width: 40%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .video-box .side-box .img-box{
        margin-top: 5%;
        width: 90%;
        height: 72%;
        display: flex;
        border: 1px dotted #ccc;
        justify-content: center;
        align-items: center;
    }
    .video-box .side-box .img-box img{
        max-width: 100%;
        max-height: 100%;
    }
    .btn-place{
        margin-top: 5%;
        width: 90%;
        height: 10%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>