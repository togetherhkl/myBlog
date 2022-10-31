$(document).ready(function () {
    // console.log('llll')
    Animation();
})
//动画效果
function Animation(){
    $('.manage-subnavbtn').click(function (){
        if ($(this).next('.manage-subnav-content').css('display')==='flex'){
            $(this).next('.manage-subnav-content').css('display','none')
            $(this).children('.icon').addClass('gg-chevron-up')
            $(this).children('.icon').removeClass('gg-chevron-down')
        }
        else {
            $(this).next('.manage-subnav-content').css('display','flex')
            $(this).children('.icon').addClass('gg-chevron-down')
           $(this).children('.icon').removeClass('gg-chevron-up')
        }
    })
}