$(document).ready(function (){
    NavLoad();//加载头部信息
    ArticleSearch()
})
function NavLoad(){
    $.ajax({
        url:'/home/',
        dataType:'JSON',
        success:function (res){
            // console.log(res)
            $.each(res.menu,(index,value)=>{
                // console.log(index,value)
                html='<div class="subnav">' +
                    '<button class="subnavbtn">'+value+'</button><div class="subnav-content">'
                $.each(res.category[index],(ind,item)=>{
                    // console.log(item[1])
                    // html+='<a class="articles" href="'+item[1]+'">'+item[0]+'</a>'
                    html+='<a class="articles" href="/article/show/?category_id='+item[1]+'">'+item[0]+'</a>'
                })
                html+='</div></div>'
                $('#subnav').before(html)//在设置前加入html元素
            })
        }
    })
}

function ArticleSearch(){
    /*
    * 头部的模糊搜索
    * */
    $('#home-search-input').bind('keypress',function(event){
        if (event.keyCode === 13) {
            search_text=$('#home-search-input').val()
            window.location.href='/article/show/?search_text='+search_text
        }
    })
}
