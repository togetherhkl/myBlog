$(document).ready(function () {
    Register();
})

function Register() {
    /*注册的模态框*/
    $('#sing-in-btn').click(() => {
        $('#myModal').css('display', 'flex')
        $('.container').css('opacity', '0.5')
    })
    //确认按钮
    $('#btnSure').click(() => {
        let csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
        $.ajax({
            url: '/login/adduser/',
            type: 'post',
            data: $('#reg-form').serialize(),
            dataType: 'JSON',
            headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
            success: function (res) {
                console.log(res.status)
                if (res.status === 404) {
                    $('.error').empty();
                    for (var error in res.msg) {
                        console.log('#id_' + error)
                        // console.log(res.msg[error][0]);
                        // let html = "<span style=\"color: red\" id=\"error\">" + res.msg[error][0] + "</span"
                        $('#id_' + error).next().text(res.msg[error][0])
                    }
                }
                if (res.status === 200) {
                    $('#myModal').css('display', 'none')
                    $('.container').css('opacity', '1')
                    alert(res.msg)
                }
            }
        })
    })
    //取消按钮
    $('#btnCansel').click(() => {
        $('#myModal').css('display', 'none')
        $('.container').css('opacity', '1')
    })
    //右上角的关闭
    $('#close').click(() => {
        $('#myModal').css('display', 'none')
        $('.container').css('opacity', '1')
    })
    //刷新验证码
    $('#img-verify').click(() => {
        console.log('di')
        //刷新验证码
        $('#img-verify').attr("src","/image/code/"+"?" + Math.random());
    })
}