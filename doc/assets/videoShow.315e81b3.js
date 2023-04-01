import{m as V,R as S,c as w,J as L,K as C,Z as k,L as I,U as F,k as y}from"./elm.7e6b5792.js";import{h as E}from"./config.f6d607cf.js";import{_ as $}from"./index.a1960522.js";import{ag as c,o as d,g as r,h as l,F as b,ak as A,a2 as t,X as i,$ as O,a0 as v,S as q,a1 as R}from"./vendor.9fab5538.js";import"./lodash.8fc0361e.js";import"https://www.gstatic.com/firebasejs/9.8.4/firebase-app.js";import"https://www.gstatic.com/firebasejs/9.8.4/firebase-analytics.js";var B={name:"videoShow",data(){return{dialogImageUrl:!1,videoShow:!1,videoUrl:"",actionUrl:E+"/webvideo",requestUrl:"",isOpenFAS:!0,openVar:!0,videoList:[]}},components:{Close:V,Plus:S},created(){this.dialogImageUrl=!1},methods:{addVideo(){if(this.videoUrl==""){this.$message({message:"\u89C6\u9891\u6D41\u5730\u5740\u4E0D\u80FD\u4E3A\u7A7A",type:"warning"});return}var e=this.videoList.length+1;this.videoList.push({id:e,name:"\u89C6\u9891\u6D41"+(this.videoList.length+1),videoUrl:this.videoUrl,isOpenFAS:this.isOpenFAS,active:""}),this.videoUrl="",this.isOpenFAS=!0,this.selectVideo(this.videoList[e-1])},useLocalVideo(){const e=new WebSocket("ws://localhost:7888");this.videoUrl="http://localhostvideo",navigator.mediaDevices.getUserMedia({video:!0}).then(o=>{const a=new MediaRecorder(o);a.ondataavailable=n=>{e.send(n.data)},a.start()}).catch(o=>{console.error(o)})},selectVideo(e){this.videoList.forEach(o=>{o.active=""}),e.active="isactive",this.openVideo(e)},openVideo(e){var o=e.videoUrl,a=e.isOpenFAS;this.videoShow=!1,this.requestUrl=encodeURI(this.actionUrl+"?url="+encodeURIComponent(o))+"&isopenfas="+a,console.log(this.requestUrl),this.videoShow=!0,this.dialogImageUrl=!1},deleteVideo(e){this.videoList.forEach(o=>{o.id==e.id&&this.videoList.splice(o.id-1,1)}),this.videoList.length===0||this.videoList==null||this.videoList==null?(this.videoShow=!1,this.requestUrl=""):this.selectVideo(this.videoList[0]),this.$forceUpdate()}}};const N={class:"video-frame"},D={class:"video-selector"},P=["onClick"],z={class:"selector-item"},M={class:"img-container"},J=v("\u786E\u8BA4"),K=v("\u53D6\u6D88"),T=v("\u91C7\u7528\u672C\u673A\u6444\u50CF\u5934"),W=["src"];function X(e,o){const a=c("Close"),n=w,p=c("Plus"),h=L,m=C,f=k,u=y,g=I,_=F;return d(),r("div",N,[l("div",D,[(d(!0),r(b,null,A(e.videoList,s=>(d(),r("div",{class:q(["selector-item",s.active])},[l("button",{onClick:U=>e.selectVideo(s)},[l("span",null,R(s.name),1),t(n,{onClick:U=>e.deleteVideo(s)},{default:i(()=>[t(a)]),_:2},1032,["onClick"])],8,P)],2))),256)),l("div",z,[l("button",{onClick:o[0]||(o[0]=s=>e.dialogImageUrl=!0)},[l("span",null,[t(n,{style:{"margin-top":"8px"},size:"samll"},{default:i(()=>[t(p)]),_:1})])])])]),l("div",M,[t(_,{modelValue:e.dialogImageUrl,"onUpdate:modelValue":o[6]||(o[6]=s=>e.dialogImageUrl=s)},{default:i(()=>[t(g,null,{default:i(()=>[t(m,{label:"\u89C6\u9891\u6D41\u94FE\u63A5\u5730\u5740"},{default:i(()=>[t(h,{modelValue:e.videoUrl,"onUpdate:modelValue":o[1]||(o[1]=s=>e.videoUrl=s)},null,8,["modelValue"])]),_:1}),t(m,{label:"\u662F\u5426\u5F00\u542F\u53CD\u6B3A\u8BC8"},{default:i(()=>[t(f,{modelValue:e.isOpenFAS,"onUpdate:modelValue":o[2]||(o[2]=s=>e.isOpenFAS=s)},null,8,["modelValue"])]),_:1}),t(m,null,{default:i(()=>[t(u,{type:"primary",onClick:o[3]||(o[3]=s=>{e.dialogImageUrl=!1,e.addVideo()})},{default:i(()=>[J]),_:1}),t(u,{type:"danger",onClick:o[4]||(o[4]=s=>e.dialogImageUrl=!1)},{default:i(()=>[K]),_:1}),t(u,{type:"success",onClick:o[5]||(o[5]=s=>{e.dialogImageUrl=!1,e.useLocalVideo()}),style:{"margin-left":"120px"}},{default:i(()=>[T]),_:1})]),_:1})]),_:1})]),_:1},8,["modelValue"]),e.videoShow?(d(),r("img",{key:0,class:"index-img",src:e.requestUrl,alt:""},null,8,W)):O("",!0)])])}var ee=$(B,[["render",X]]);export{ee as default};
//# sourceMappingURL=videoShow.315e81b3.js.map
