import{_ as w,u as S}from"./index.a1960522.js";import{M as E,N as F,H as L,I as A,k as B,J as z,K as N,L as U}from"./elm.7e6b5792.js";import{L as g,bw as M,by as O,bz as R,bx as W,r as x,ag as c,o as m,g as _,a2 as t,X as s,h as e,F as P,ak as j,W as G,bk as H,bl as J,a0 as u,m as K,$ as X}from"./vendor.9fab5538.js";import{_ as q,a as Q}from"./google.acc9adbb.js";import{S as Y,W as Z}from"./WelcomeLabel.de9339b4.js";import"./lodash.8fc0361e.js";import"https://www.gstatic.com/firebasejs/9.8.4/firebase-app.js";import"https://www.gstatic.com/firebasejs/9.8.4/firebase-analytics.js";const ee=g({name:"RegisterForm",components:{MailIcon:M,AcademicCapIcon:O,IdentificationIcon:R,LockOpenIcon:W},setup(){const o=x(),a=x({username:"",email:"",usrType:"",password:""});return{userType:[{id:1,nameType:"Admin"},{id:2,nameType:"Creator"},{id:3,nameType:"Member"}],form:o,formData:a}}}),l=o=>(H("data-v-5fbeaa67"),o=o(),J(),o),te={class:"w-full"},oe=l(()=>e("div",{class:"text-muted text-center mt-1.5 mb-6"},[e("small",null,"Sign up with")],-1)),se={class:"flex flex-nowrap text-center justify-center pb-7.5"},ae=l(()=>e("img",{src:q,alt:"",class:"h-4 w-4"},null,-1)),ne=l(()=>e("span",{class:"pl-4 text-indigo-410"},"Github",-1)),le=l(()=>e("img",{src:Q,alt:"",class:"h-4 w-4"},null,-1)),re=l(()=>e("span",{class:"pl-4 text-indigo-410"},"Google",-1)),ce={class:"content-center items-center w-full lg:p-6"},ie=l(()=>e("div",{class:"text-muted text-center mb-5"},[e("small",null,"Or sign up with credentials ")],-1)),de={class:"authentication-form-icon z-10 absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"},me={class:"w-5 h-5"},pe={class:"authentication-form-icon z-10 absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none"},_e={class:"w-5 h-5"},ue={class:"authentication-form-icon z-10 absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none"},fe={class:"w-5 h-5"},he={class:"authentication-form-icon z-10 absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none"},xe={class:"w-5 h-5"},we={class:"authentication-form-icon z-10 absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none"},ge={class:"w-5 h-5"},ve=l(()=>e("div",{class:"italic"},[e("span",{class:"text-0.8125 text-muted font-normal"},[u(" password strength: "),e("strong",{class:"text-success"},"strong")])],-1)),be=u("I agree with the "),ye=l(()=>e("a",{href:"#!",class:"text-indigo-410 hover:text-indigo-410-active"},"Privacy Policy",-1)),Ie=u(" Create account ");function $e(o,a,f,v,b,y){const d=B,p=c("AcademicCapIcon"),i=z,r=N,I=c("MailIcon"),$=c("IdentificationIcon"),V=E,k=F,h=c("LockOpenIcon"),C=L,D=U,T=A;return m(),_("div",te,[t(T,{class:"bg-secondary text-center"},{header:s(()=>[oe,e("div",se,[t(d,{class:"bg-white border-white",href:"#"},{default:s(()=>[ae,ne]),_:1}),t(d,{class:"bg-white border-white ml-7",href:"#"},{default:s(()=>[le,re]),_:1})])]),default:s(()=>[e("div",ce,[ie,t(D,{ref:"form",model:o.formData,class:"authentication-form pb-6"},{default:s(()=>[t(r,{class:"mb-6 rounded-md",prop:"username"},{default:s(()=>[e("div",de,[e("div",me,[t(p,{class:"w-5 h-5 text-gray-210"})])]),t(i,{placeholder:"Name",modelValue:o.formData.username,"onUpdate:modelValue":a[0]||(a[0]=n=>o.formData.username=n)},null,8,["modelValue"])]),_:1}),t(r,{class:"mb-6 rounded-md",prop:"email"},{default:s(()=>[e("div",pe,[e("div",_e,[t(I,{class:"w-5 h-5 text-gray-210"})])]),t(i,{type:"email",placeholder:"Email",modelValue:o.formData.email,"onUpdate:modelValue":a[1]||(a[1]=n=>o.formData.email=n)},null,8,["modelValue"])]),_:1}),t(r,{class:"mb-6 rounded-md",prop:"type"},{default:s(()=>[e("div",ue,[e("div",fe,[t($,{class:"w-5 h-5 text-gray-210"})])]),t(k,{modelValue:o.formData.usrType,"onUpdate:modelValue":a[2]||(a[2]=n=>o.formData.usrType=n),placeholder:"User Type",class:"w-full","popper-class":"item-input-popper"},{default:s(()=>[(m(!0),_(P,null,j(o.userType,n=>(m(),G(V,{key:n.id,label:n.nameType,value:n.id},null,8,["label","value"]))),128))]),_:1},8,["modelValue"])]),_:1}),t(r,{class:"mb-6 rounded-md",prop:"password"},{default:s(()=>[e("div",he,[e("div",xe,[t(h,{class:"w-5 h-5 text-gray-210"})])]),t(i,{type:"password",placeholder:"Password",modelValue:o.formData.password,"onUpdate:modelValue":a[3]||(a[3]=n=>o.formData.password=n)},null,8,["modelValue"])]),_:1}),t(r,{class:"mb-6 rounded-md",prop:"password"},{default:s(()=>[e("div",we,[e("div",ge,[t(h,{class:"w-5 h-5 text-gray-210"})])]),t(i,{type:"password",placeholder:"Confirm Password",modelValue:o.formData.password,"onUpdate:modelValue":a[4]||(a[4]=n=>o.formData.password=n)},null,8,["modelValue"])]),_:1}),t(r,{class:"mb-6 rounded-md"},{default:s(()=>[ve]),_:1}),t(r,{class:"mb-6"},{default:s(()=>[t(C,{class:"w-4 h-4 text-muted font-normal"},{default:s(()=>[be,ye]),_:1})]),_:1})]),_:1},8,["model"]),t(d,{type:"primary"},{default:s(()=>[Ie]),_:1})])]),_:1})])}var Ve=w(ee,[["render",$e],["__scopeId","data-v-5fbeaa67"]]);const ke=g({components:{RegisterForm:Ve,SplitBackground:Y,WelcomeLabel:Z},setup(){const o=S();return{isAuthenticated:K(()=>o.auth.getAuthenticationState)}}}),Ce={key:0},De={class:"relative w-full bg-gradient-to-r from-indigo-410 to-indigo-450 py-24 lg:py-32 lg:pt-40"},Te={class:"container xl:max-w-5.75xl lg:max-w-4.5xl md:max-w-2.625xl sm:max-w-0.25xl w-full mx-auto px-3.75"},Se={class:"text-center mb-12"},Ee={class:"flex flex-wrap -mx-3.75 justify-center px-3.75"},Fe={class:"md:flex-9 md:max-w-9/12 lg:flex-8 lg:max-w-2/3"},Le={class:"container relative xl:max-w-5.75xl lg:max-w-4.5xl md:max-w-2.625xl sm:max-w-0.25xl w-full mx-auto px-4"},Ae={class:"relative lg:max-w-1/2 md:max-w-2/3 mx-auto md:px-1.5 -mt-32 mb-20"};function Be(o,a,f,v,b,y){const d=c("WelcomeLabel"),p=c("SplitBackground"),i=c("RegisterForm");return o.isAuthenticated?X("",!0):(m(),_("div",Ce,[e("div",De,[e("div",Te,[e("div",Se,[e("div",Ee,[e("div",Fe,[t(d)])])])]),t(p)]),e("div",Le,[e("div",Ae,[t(i)])])]))}var je=w(ke,[["render",Be]]);export{je as default};
//# sourceMappingURL=register.fdd57af9.js.map
