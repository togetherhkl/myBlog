$(document).ready(function () {
    Animation();
    VditorEdit()
})

//一些动画效果
function Animation() {
    $('.title').mouseover(() => {
        $('.btn-img').css('opacity', 1);
    })
    $('.title').mouseleave(() => {
        $('.btn-img').css('opacity', 0);
    })
    $('.btn-img').mouseover(() => {
        $('.btn-img').css('opacity', 1);
    })
    $('.btn-img').mouseleave(() => {
        $('.btn-img').css('opacity', 0);
    })
}

/*载入markdown编辑器*/
function VditorEdit() {
    var csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
    var vditor = new Vditor(document.getElementById('vditor'), {
        cache: {
            enable: false
        },
        //字数统计
        counter: {
            enable: true,
        },
        //固定头部栏
        "toolbarConfig": {
            "pin": true
        },
        //显示大纲
        "outline": {
            "enable": true,
            "position": "right",
        },
        height: '800px',
        width: '100%',
        "value": " ",
        "mode": "ir",/*及时渲染模式*/
        "preview": {
            "hljs": {
                "style": "native",//代码颜色主题
                "lineNumber": true,//启动行号
            }
        },
        upload: {
            accept: 'image/*,.mp3, .wav, .rar',
            token: '',
            url: '/upload/inarticle/img/',
            linkToImgUrl: '',//后期可考虑上传到图床
            filename(name) {
                return name.replace(/[^(a-zA-Z0-9\u4e00-\u9fa5\.)]/g, '').replace(/[\?\\/:|<>\*\[\]\(\)\$%\{\}@~]/g, '').replace('/\\s/g', '')
            },
            headers: {
                "X-CSRFToken": csrfToken,
            },
            success(_, res) {
                console.log(res)
                res=JSON.parse(res)
                if (res.code === 200) {
                    for (i = 0; i < res.data.count; i++) {
                        // vditor.insertValue(`![${JSON.parse(res).data.name[i]}](${JSON.parse(res).data.url[i]})<br>`);
                        vditor.insertValue(`![${res.data.name[i]}](${window.location.origin}/${res.data.url[i]})`);
                    }
                }
                else {
                    alert(res.msg);
                }


            }
            // format: function (files, res) {
            //     // 字符串转换为对象
            //     const {code, data, msg} = JSON.parse(res);
            //     if (code === 200) {
            //         return JSON.stringify({
            //             "msg": msg,
            //             "code": code,
            //             "data": {
            //                 "errFiles": [],
            //                 "succMap": {
            //                     [data.name]: window.location.origin+'/'+data.url,
            //                 }
            //             }
            //         });
            //     } else {
            //         alert("图片上传失败: " + msg);
            //         return;
            //     }
            // }
        },

    });
    document.getElementById('vditor').append(vditor)
}
