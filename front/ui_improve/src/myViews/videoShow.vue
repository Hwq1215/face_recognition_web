<template>
    <div class="video-frame">
        <div class="video-selector">
            <div v-for="item in videoList" class="selector-item" :class="item.active">
                <button  @click="selectVideo(item)">
                    <span>{{ item.name }}</span>
                    <el-icon @click="deleteVideo(item)"><Close/></el-icon>
                </button>
            </div>
            <div class="selector-item">
                <button @click="dialogImageUrl = true"><span><el-icon style="margin-top: 8px;" size="samll"><Plus></Plus></el-icon></span></button>
            </div>
            <!-- <el-button type="info" @click="$event => {videoUrl= '' ;videoShow=false; return ;}">清理</el-button> -->
        </div>

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
                <el-button type="primary" @click="dialogImageUrl=false;addVideo();" >确认</el-button>
                <el-button type="danger" @click="dialogImageUrl = false" >取消</el-button>
                <el-button type="success" @click="dialogImageUrl = false; useLocalVideo();" style="margin-left: 120px;">采用本机摄像头</el-button>
            </el-form-item>
            </el-form>
        </el-dialog >
        <!-- <el-dialog v-model="openVar" title="警告" width="400px" center>
           
            <el-icon color="red"><warning/></el-icon>
            <span> 欺诈识别已记录，请勿进行欺诈识别</span>
        </el-dialog> -->
            <img v-if="videoShow" class="index-img" :src="requestUrl" alt="">

        <!-- <img v-else class="index-img" src="../assets/images/loading.webp" alt=""> -->
        </div>
    </div>

</template>

<script lang="js">
import { httpurl } from '../config'
import { Close,Plus } from '@element-plus/icons-vue'

export default{
    name: 'videoShow',
    data(){
        return{
            dialogImageUrl: false,
            videoShow : false,
            videoUrl:'',
            actionUrl: httpurl+'/webvideo',
            requestUrl: '',
            isOpenFAS: true,
            openVar: true,
            videoList:[
                // {
                //     id: 1,
                //     name: '视频流1',
                //     videoUrl: '',
                //     isOpenFAS: true,
                //     active: '',
                // }
            ]
                
    }
    },
    components:{
        Close,
        Plus
    },
    created(){
        this.dialogImageUrl = false;
    },
    methods:{
        addVideo(){
            if(this.videoUrl == ''){
                this.$message({
                    message: '视频流地址不能为空',
                    type: 'warning'
                })
                return
            }
            var id =  this.videoList.length + 1
            this.videoList.push({
                id: id,
                name: '视频流' + (this.videoList.length + 1),
                videoUrl: this.videoUrl,
                isOpenFAS: this.isOpenFAS,
                active: ''
            })
            this.videoUrl = ''
            this.isOpenFAS = true
            this.selectVideo(this.videoList[id-1]);
        
        },
        useLocalVideo(){
            const ws = new WebSocket('ws://localhost:7888');
            this.videoUrl = 'http://localhostvideo'
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    // 将视频流传输到后台
                    const mediaRecorder = new MediaRecorder(stream);
                    mediaRecorder.ondataavailable = event => {
                    ws.send(event.data);
                    };
                    mediaRecorder.start();
                })
                .catch(error => {
                    console.error(error);
                });
            // this.addVideo();
        },
        selectVideo(item){
            this.videoList.forEach(element => {
                element.active = ''
            });
            item.active = 'isactive';
            this.openVideo(item);
        },
        openVideo(item){
            var videoUrl = item.videoUrl
            var isOpenFAS = item.isOpenFAS
            this.videoShow = false
            this.requestUrl = encodeURI(this.actionUrl + '?url=' + encodeURIComponent(videoUrl)) + '&' + 'isopenfas=' + isOpenFAS
            console.log(this.requestUrl)
            this.videoShow = true
            this.dialogImageUrl = false
            
        },
        
        deleteVideo(item){
            this.videoList.forEach(element => {
               if(element.id == item.id){
                   this.videoList.splice(element.id-1,1)
               }
            });
            if(this.videoList.length === 0 || this.videoList == null || this.videoList == undefined){
                this.videoShow = false;
                this.requestUrl = '';
            }else{
                this.selectVideo(this.videoList[0])
            }
            this.$forceUpdate();
        }
    }
}

</script>

<style>
    .video-frame{
        width: 100%;
        height: 650px;
        flex-direction: column;
        margin-bottom: 50px;
    }
    .video-selector{
        display: flex;
        margin-top: 42px;
    }
    .video-selector .selector-item{
        display: flex;
        min-width: 35px;
        max-width: 130px;
        height: 30px;
        margin-left: 0px;
        margin-right: 2px;
        border-radius: 8px 8px 0px 0px;
        background-color: #c5def6;
        transition: all 0.5s;
    }
    .video-selector .selector-item:hover{
        background-color: white;
    }
    .video-selector .selector-item.isactive{
        background-color: white;
    }
    .video-selector .selector-item button{
        display: flex;
        width: 100%;
        height: 100%;
        border: none;
    }
    .video-selector .selector-item button span{
        margin: auto;
        margin-left: 20px;
        margin-right: 15px;
        font-size: 16px;
        font-weight: 500;
        color: #2c3e50;
    }
    .video-selector .selector-item button .el-icon{
        margin-top: 8px;
        margin-right: 5px;
    }
    .img-container{
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .index-img{

        margin-top: 40px;
        max-width: 1500px;
        max-height: 580px;
    }
</style>