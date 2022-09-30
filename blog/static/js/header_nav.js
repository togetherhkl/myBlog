$(document).ready(function (){
    NavLoad();//加载头部信息
})
function NavLoad(){
    $.ajax({
        url:'/home/',
        dataType:'JSON',
        success:function (res){
            $.each(res.menu,(index,value)=>{
                //console.log(index,value)
                html='<div class="subnav">' +
                    '<button class="subnavbtn">'+value+'</button><div class="subnav-content">'
                $.each(res.category[index],(ind,item)=>{
                    html+='<a href="'+item[1]+'">'+item[0]+'</a>'
                })
                html+='</div></div>'
                $('#subnav').before(html)//在设置前加入html元素
            })
        }
    })
}