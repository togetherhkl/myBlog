$(document).ready(function(){
    AddTags();
})
function AddTags(){
    $('.entry-meta-tags .tags').each(function (){
        let csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
        article_id=$(this).attr('value')
        var temp=$(this)//临时储存标签，用于查到数据后的修改
        // console.log(article_id)
        //获取文章的标签
        $.ajax({
             url: '/article/gettags/',
             type: 'post',
             data: {'article_id':article_id},
             dataType: 'JSON',
             headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
             success: function (res) {
                 //添加错误消息
                 if (res.status === 400) {
                     console.log('没有数据')
                 }
                 if (res.status === 200) {
                     // console.log(res.tags)
                     let html=''
                     for(let tag in res.tags){
                         // console.log(res.tags[tag])
                         html+=' <a href="#">'+res.tags[tag]+'</a>,'
                     }
                     console.log(html)
                     // $(this).html(html)
                     temp.html(html)//修改显示的标签
                 }
             }
         })
    })
}