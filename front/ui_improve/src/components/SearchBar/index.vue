<template>
    <div class="input-box">
        <span><el-icon><Search/></el-icon></span>
      <input type="text" class="input" />
      <div
        class="closePlace items-center lg:hidden md:hidden sm:hidden"
        :class="{ hidden: isSBPin }">
        <el-icon
          :size="20"
          class="cursor-pointer w-4 h-4 text-black hover:text-slate-300"
          @click="$emit('close-search')"
        >
          <Close />
        </el-icon>
      </div>
    </div>

</template>
<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import useStore from 'store'
import { Close,Search } from '@element-plus/icons-vue'
export default defineComponent({
  name: 'SearchBar',
  components: {
    Close,
    Search,
  },
  setup() {
    const store = useStore()
    const textInput = ref('')
    const isSBPin = computed(() => store.dashboard.isSBPin)
    
    return {
      isSBPin,
      textInput,
    }
  },
})
</script>

<style lang="scss" scoped> 
    .input-box {
      position: relative;
    }
    .input {
      width: 220px;
      height: 42px;
      font-size: 14px;
      padding: 0 40px 0px 40px;
      border: 1px solid #eee;
      border-radius: 40px;
      transition: width 0.5s;
      transition-delay: 0.1s;
      //透明度
      opacity: 0.65;
    }
    .input-box span{
      background-color: transition;
      border-radius: 30%;
      width: 20px;
      height: 10px;
      font-size: large;
      margin-right: 2px;
      position: absolute;
      top: 2px;
      left: 12px;
      opacity: 1;
    }
    .input-box span .el-icon{
      color: black !important;
      border: black 2px;
      margin-top: 10px;
      font-size: 19px;
      opacity: 1 !important;
    }
    // .input-box span {
    //   width: 30px;
    //   height: 30px;
    //   line-height: 30px;
    //   color: #969696;
    //   text-align: center;
    //   background: #222;
    //   border-radius: 50%;
    //   font-size: 15px;
    //   cursor: pointer;
    //   position: absolute;
    //   top: 4px;
    //   right: 5px;
    // }
    /* 添加input 的focus事件 */
    .input:focus {
      width: 330px;
      outline: none;
      box-shadow: none;
      transition-delay: 20;
      opacity: 1;
    }
    .input:focus + .closePlace {
      position: absolute;
      left: 290px;
      top: 10px;
      opacity: 1;
      color: black;
      transition-delay: 20;
      outline: none;
      box-shadow: none;
    }
    .closePlace{
      position: absolute;
      left: 180px;
      top: 10px;
      width: 40px;
      height: 40px;
      line-height: 30px;
      color: black;
      text-align: center;
      background: transparent;
      border-radius: 50%;
      font-size: 15px;
      cursor: pointer;
      opacity: 0.4;
      transition: left 0.5s;
      transition-delay: 0.1s;
    }
//   .input {
//   @apply w-full;
//   ::v-deep(.el-input__inner) {
//     @apply relative transition-all duration-200 pt-2.5 pl-10.25 placeholder:text-sm placeholder:text-gray-500/90 text-sm w-full sm:w-[291px] h-11.5 resize-y leading-6 rounded-full bg-[#eff1fc] font-normal shadow-none border-none #{!important};
//     &:focus {
//       @apply w-full sm:w-98 bg-white text-black border-indigo-410 #{!important};
//     }
//   }
// }
</style>
