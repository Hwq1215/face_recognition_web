import{R as z,S as A,T as $,O,Q as U,D as q,k as R,c as N,J as H,K as J,L as B,U as G}from"./elm.7e6b5792.js";import{bH as L,bI as F,ag as p,o as g,g as I,h as c,a2 as o,X as i,a0 as m,a1 as V,S as X,W as b,F as M}from"./vendor.9fab5538.js";import{h as y}from"./config.2519a230.js";import{V as K}from"./VideoReader.eb4bdf8e.js";import{_ as v}from"./index.d4df333c.js";import"./lodash.8fc0361e.js";import"https://www.gstatic.com/firebasejs/9.8.4/firebase-app.js";import"https://www.gstatic.com/firebasejs/9.8.4/firebase-analytics.js";const Q=y;var D=async(e="",t={},n="GET",h="no-fetch")=>{if(n=n.toUpperCase(),e=Q+e,n=="GET"){let a="";Object.keys(t).forEach(l=>{a+=l+"="+t[l]+"&"}),a!==""&&(a=a.substr(0,a.lastIndexOf("&")),e=e+"?"+a)}if(window.fetch&&h=="fetch"){let a={credentials:"include",method:n,headers:{Accept:"application/json","Content-Type":"application/json"},mode:"cors",cache:"no-cache"};n=="POST"&&Object.defineProperty(a,"body",{value:JSON.stringify(t)});try{return await(await fetch(e,a)).json()}catch(l){throw new Error(l)}}else return new Promise((a,l)=>{let r;window.XMLHttpRequest?r=new XMLHttpRequest:r=new ActiveXObject;let d="";n=="POST"&&(d=JSON.stringify(t)),r.open(n,e,!0),r.setRequestHeader("Content-type","application/x-www-form-urlencoded"),r.send(d),r.onreadystatechange=()=>{if(r.readyState==4)if(r.status==200){let f=r.response;typeof f!="object"&&(f=JSON.parse(f)),a(f)}else l(r)}})};const W=e=>D("/manage/get",e,"GET"),Y=()=>D("/manage/total","","GET"),Z=e=>D("/manage/delete",e,"GET");const ee={name:"ProjectTable",props:{facesData:{type:Array,required:!1},pageSize:{type:Number,required:!1}},data(){return{total:20,currentPage:1,DialogIsVisiable:!1,VideoDialogIsVisiable:!1,editChoose:!0,imageUrl:"",pageSize:20,reFresh:!0,chooseItem:{faceId:0,name:"",imgSrc:"",files:void 0},facesData:[{name:"\u5F20\u4E09",fake:"\u662F"},{name:"\u674E\u56DB",fake:"\u5426"}],fakeData:[{name:"\u5F20\u4E09",time:"2021-05-01",fake:"\u662F",imgSrc:"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1620000000&di=1b1f1b1f1b1f1b1f1b1f1b1f1b1f1b1f&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F01e4e756e5b9fba801219c77f3b5b6.jpg%401280w_1l_2o_100sh.jpg"},{name:"\u674E\u56DB",time:"2021-05-01",fake:"\u5426",imgSrc:"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1620000000&di=1b1f1b1f1b1f1b1f1b1f1b1f1b1f1b1f&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F01e4e756e5b9fba801219c77f3b5b6.jpg%401280w_1l_2o_100sh.jpg"}]}},created(){this.init()},components:{DotsVerticalIcon:L,Plus:z,IconPicture:A,Refresh:$,VideoReader:K},watch:{currentPage(e){this.handlePageSelect(e)}},methods:{init(){this.getFacesTotal(),this.getFacesInPage(this.currentPage)},handlePageSelect(e){this.getFacesInPage(e)},handleEdit(e,t){this.factoryChooseItem(t),this.editChoose=!0,this.DialogIsVisiable=!0},updateFaceData(){this.UpDateFaceData()},handleDelete(e,t){this.deleteFaceData(t)},handleAdd(){this.initChooseItem(),this.editChoose=!1,this.DialogIsVisiable=!0},handleAddAll(){this.$refs["input-all"].click()},handleVideo(){this.VideoDialogIsVisiable=!0},addFaceData(){this.UploadFaceData()},handleInsert(){this.addFaceData()},async getFacesTotal(){this.total=await Y()},async getFacesInPage(e){this.facesData=[],this.facesData=await W({page:e,pageSize:this.pageSize})},async deleteFaceData(e){var t=await Z({faceId:e.faceId});console.log(t),t.msg=="success"?this.$message({message:"\u5220\u9664\u6210\u529F",type:"success"}):this.$message({message:"\u5220\u9664\u5931\u8D25",type:"error"}),this.facesData.forEach((n,h)=>{n.faceId==e.faceId&&this.facesData.splice(h,1)})},initChooseItem(){this.chooseItem={faceId:0,name:"",fake:"",files:void 0}},factoryChooseItem(e){this.chooseItem={faceId:e.faceId,name:e.name,fake:e.fake,imgSrc:e.imgSrc,files:void 0}},getVideoImg(){var e=this.$refs.reader.imgFile;this.showImg(e),this.VideoDialogIsVisiable=!1,console.log(e)},showImgEvent(e){let t=e.target.files[0];this.showImg(t)},showImg(e){let t=this;if(!e||!window.FileReader)return;let n=new FileReader;console.log(e),n.readAsDataURL(e),n.onloadend=function(){t.chooseItem.imgSrc=this.result,t.chooseItem.files=e}},UploadFaceData(){try{let e=new FormData;e.append("name",this.chooseItem.name),e.append("imgfile",this.chooseItem.files),console.log(e),F({method:"post",url:y+"/manage/add",headers:{"Content-Type":"multipart/form-data","Access-Control-Allow-Origin":"*"},data:e}).then(t=>{console.log(t),t.data=="success"?this.$message({message:"\u6DFB\u52A0\u6210\u529F",type:"success"}):this.$message({message:"\u6DFB\u52A0\u5931\u8D25",type:"error"}),this.init()})}catch(e){this.$message({message:"\u9519\u8BEF",type:"error"}),console.log(e)}finally{this.DialogIsVisiable=!1,this.initChooseItem()}},UpDateFaceData(){try{let e=new FormData;e.append("faceId",this.chooseItem.faceId),e.append("name",this.chooseItem.name),e.append("imgfile",this.chooseItem.files),console.log(e),F({method:"post",url:y+"/manage/update",headers:{"Content-Type":"multipart/form-data","Access-Control-Allow-Origin":"*"},data:e}).then(t=>{console.log(t),t.data=="success"?(this.$message({message:"\u4FEE\u6539\u6210\u529F",type:"success"}),this.facesData.map(n=>{n.faceId==this.chooseItem.faceId&&(n.name=this.chooseItem.name,n.imgSrc=this.chooseItem.imgSrc+"?t="+new Date().getTime())})):this.$message({message:"\u4FEE\u6539\u5931\u8D25\uFF0C\u4EBA\u8138\u6570\u4E0D\u552F\u4E00\u6216\u8005\u4EBA\u8138\u91CD\u590D",type:"error"}),this.init()})}catch(e){this.$message({message:"\u9519\u8BEF",type:"error"}),console.log(e)}finally{this.DialogIsVisiable=!1,this.initChooseItem()}},HandleImgSelect(){this.$refs.inputImg.click()}}},te={class:"w-full"},ae=["onClick"],se={class:"pl-2 mb-0 text font-semibold cursor-auto",style:{"margin-left":"0"}},oe=m("\u7F16\u8F91"),ie=m("\u5220\u9664"),le={type:"file",ref:"input-all",style:{display:"none"}},ne=m(" \u6279\u91CF\u4E0A\u4F20 "),re=c("span",{style:{float:"right","margin-right":"2%","margin-top":"45px",color:"#b0b0b0"}},"\u652F\u6301zip,rar\u683C\u5F0F\u7684\u538B\u7F29\u5305",-1),ce={class:"p-4"},de=["src"],me={style:{"margin-top":"0px","margin-left":"20px"}},fe=c("br",null,null,-1),ge=m("\u5F55\u5236"),he=m("\u786E\u8BA4"),pe=m("\u786E\u8BA4"),ue=m("\u53D6\u6D88");function _e(e,t,n,h,a,l){const r=O,d=R,f=U,k=p("Plus"),u=N,S=q,x=H,_=J,P=p("Picture"),T=p("VideoCameraFilled"),E=B,w=G,j=p("video-reader");return g(),I(M,null,[c("div",te,[o(f,{data:a.facesData,style:{width:"100%"},class:X(`is-${e.theme}`)},{default:i(()=>[o(r,{label:"\u7F16\u53F7",width:"200"},{default:i(s=>[m(V(s.$index+1),1)]),_:1}),o(r,{label:"\u7528\u6237\u540D","min-width":"280"},{default:i(s=>[c("div",{onClick:C=>l.handleEdit(s.$index,s.row),class:"flex items-center"},[c("span",se,V(s.row.name),1)],8,ae)]),_:1}),o(r,{label:"\u64CD\u4F5C",width:"200",fixed:"right"},{default:i(s=>[o(d,{size:"small",onClick:C=>l.handleEdit(s.$index,s.row)},{default:i(()=>[oe]),_:2},1032,["onClick"]),o(d,{size:"small",type:"danger",onClick:C=>l.handleDelete(s.$index,s.row)},{default:i(()=>[ie]),_:2},1032,["onClick"])]),_:1})]),_:1},8,["data","class"]),o(d,{type:"success",onClick:t[0]||(t[0]=s=>l.handleAdd()),style:{float:"right","margin-right":"5%","margin-top":"40px"},circle:""},{default:i(()=>[o(u,null,{default:i(()=>[o(k)]),_:1})]),_:1}),o(d,{type:"success",onClick:t[1]||(t[1]=s=>l.handleAddAll()),style:{float:"right","margin-right":"2%","margin-top":"40px"},rounded:""},{default:i(()=>[c("input",le,null,512),ne]),_:1}),re,c("div",ce,[o(S,{"page-size":a.pageSize,"pager-count":5,"current-page":a.currentPage,"onUpdate:current-page":t[2]||(t[2]=s=>a.currentPage=s),background:"",layout:"prev, pager, next",total:a.total,class:"mt-4"},null,8,["page-size","current-page","total"])])]),o(w,{modelValue:a.DialogIsVisiable,"onUpdate:modelValue":t[10]||(t[10]=s=>a.DialogIsVisiable=s),title:a.editChoose?"\u4FEE\u6539":"\u4E0A\u4F20"},{default:i(()=>[o(E,null,{default:i(()=>[o(_,{label:"\u59D3\u540D"},{default:i(()=>[o(x,{modelValue:a.chooseItem.name,"onUpdate:modelValue":t[3]||(t[3]=s=>a.chooseItem.name=s)},null,8,["modelValue"])]),_:1}),o(_,{label:"\u56FE\u7247"},{default:i(()=>[c("div",{onClick:t[4]||(t[4]=s=>l.HandleImgSelect()),class:"input-img"},[a.chooseItem.imgSrc?(g(),I("img",{key:0,src:a.chooseItem.imgSrc},null,8,de)):(g(),b(u,{key:1,size:"20"},{default:i(()=>[o(P)]),_:1}))]),c("div",me,[c("input",{onChange:t[5]||(t[5]=s=>l.showImgEvent(s)),ref:"inputImg",class:"input-hiden",hidden:"",type:"file"},null,544),fe,o(d,{type:"success",onClick:t[6]||(t[6]=s=>l.handleVideo())},{default:i(()=>[ge,o(u,{size:"17"},{default:i(()=>[o(T)]),_:1})]),_:1})])]),_:1}),o(_,null,{default:i(()=>[a.editChoose?(g(),b(d,{key:0,type:"primary",onClick:t[7]||(t[7]=s=>l.updateFaceData())},{default:i(()=>[he]),_:1})):(g(),b(d,{key:1,type:"primary",onClick:t[8]||(t[8]=s=>l.addFaceData())},{default:i(()=>[pe]),_:1})),o(d,{type:"danger",onClick:t[9]||(t[9]=s=>a.DialogIsVisiable=!1)},{default:i(()=>[ue]),_:1})]),_:1})]),_:1})]),_:1},8,["modelValue","title"]),o(w,{modelValue:a.VideoDialogIsVisiable,"onUpdate:modelValue":t[12]||(t[12]=s=>a.VideoDialogIsVisiable=s)},{default:i(()=>[o(j,{onChooseImg:t[11]||(t[11]=s=>l.getVideoImg()),ref:"reader"},null,512)]),_:1},8,["modelValue"])],64)}var be=v(ee,[["render",_e]]);const Ie={name:"Tables",data(){return{facesData:[],pageSize:13,currentPage:1,total:0}},methods:{init(){this.ProjectTable.init()}},components:{ProjectTable:be}},ye={class:"w-full block mx-auto h-auto py-2"},De={class:"flex flex-wrap flex-col bg-white shadow mb-7 mx-auto rounded-md"},we=c("div",{class:"py-5 px-6 border-b border-primary-white"},[c("h3",{class:"cursor-auto"},"\u4EBA\u8138\u4FE1\u606F")],-1),Ce={class:"block overflow-x-auto w-full"};function Fe(e,t,n,h,a,l){const r=p("ProjectTable");return g(),I("div",ye,[c("div",De,[we,c("div",Ce,[o(r,{facesData:a.facesData,pageSize:e.page-e.size},null,8,["facesData","pageSize"])])])])}var je=v(Ie,[["render",Fe]]);export{je as default};
//# sourceMappingURL=index.3464d9b2.js.map