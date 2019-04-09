<template lang="html">
    <div class="img-403">
        <div class="img-box">
            <img src="../common/images/403.png" alt="">
            <div class="tips-403">
              <p class="name">
                Sorry，您没有该页面的权限，请联系应用管理员
              </p>
            </div>
        </div>
    </div>
</template>

<style media="screen" lang="scss">
    .img-403{
        position: relative;
        height: 100%;
        .img-box{
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            width: 650px;
            text-align: center;
            font-size: 16px;
        }
        img{
            display: block;
            margin: 0 auto;
        }
        .tips-403{
            margin-top: 10px;
            font-size: 20px;
            color: #979797;
            .name{
                margin: 10px auto 0;
                width: 500px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: break-word;
                white-space: nowrap;
            }
        }
    }
</style>
