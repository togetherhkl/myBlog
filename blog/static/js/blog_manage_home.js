$(document).ready(function(){
    ChangePwd()
})
let csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
function ChangePwd(){
    $('#change-pwd-btn').click(function (){
        let old_pwd=$('#old_pwd').val()
        let new_pwd=$('#new_pwd').val()
        let confirm_pwd=$('#confirm_pwd').val()
        $.ajax({
            url: '/blog/manage/home/',
            type: 'post',
            data: {
                'type':'change_pwd',
                'old_pwd':old_pwd,
                'new_pwd':new_pwd,
                'confirm_pwd':confirm_pwd,
            },
            dataType: 'JSON',
            headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
            //获取数据成功
            success: function (res){
                console.log(res)
                if(res.status===400){
                    $('#old_pwd').next().text(res.old_pwd)
                    $('#new_pwd').next().text(res.new_pwd)
                    $('#confirm_pwd').next().text(res.confirm_pwd)
                }
                else if(res.status===200){
                    alert('密码修改成功')
                    //清空错误提示
                    $('#old_pwd').next().text(res.old_pwd)
                    $('#new_pwd').next().text(res.new_pwd)
                    $('#confirm_pwd').next().text(res.confirm_pwd)
                    //清空输入框内容
                    $('#old_pwd').val('')
                    $('#new_pwd').val('')
                    $('#confirm_pwd').val('')
                }
            }
        })
    })
}