$(document).ready(function () {
    Animation();
    PublishArticle();
    VditorEdit();
    CoverImg();
})

//一些动画效果
function Animation() {
    $('.title').mouseover(() => {
        $('.button-img').css('opacity', 1);
    })
    $('.title').mouseleave(() => {
        $('.button-img').css('opacity', 0);
    })
    $('.button-img').mouseover(() => {
        $('.button-img').css('opacity', 1);
    })
    $('.button-img').mouseleave(() => {
        $('.button-img').css('opacity', 0);
    })
    $('#article-img').mouseover(() => {
        $('#btn-mod-img').css('visibility', 'visible')
    })
    $('#article-img').mouseleave(() => {
        $('#btn-mod-img').css('visibility', 'hidden')
        $('#mod-select-content').css('visibility', 'hidden');
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
                res = JSON.parse(res)
                if (res.code === 200) {
                    for (let i = 0; i < res.data.count; i++) {
                        // vditor.insertValue(`![${JSON.parse(res).data.name[i]}](${JSON.parse(res).data.url[i]})<br>`);
                        vditor.insertValue(`![${res.data.name[i]}](${window.location.origin}/${res.data.url[i]})`);
                    }
                } else {
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

    // 一键提取摘要
    $('#btn-get-digest').click(() => {
        let digest_text = vditor.getValue();
        if (digest_text.length < 400) {
            $('#id_article_digest').val(digest_text)
        } else {
            $('#id_article_digest').val(digest_text.substring(0, 400))
        }
    })
    //发表确认确认按钮
    $('#btnSure').click(() => {
        let option = 2
        SaveArticle(option)
    })
    //保存按钮
    $('#btn-save').click(() => {
        console.log('点击了保存')
        $('#id_article_title').val($('#title').val())
        $('#id_article_digest').val('none');
        let option = 1
        //模态框封面显示
        if ($("#article-img").attr('"background-image"')) {
            //获取背景图片的地址的css
            let imgurl = $('#article-img').css("background-image");
            //获取图片的url
            let temp = imgurl.split('\"')[1];
            //获取图片的名称
            let url = temp.split('/');
            let imgname = url[url.length - 1];
            $('#id_article_img').val(imgname);
        }
        SaveArticle(option)
    })

    function SaveArticle(option) {
        let csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
        let content = $('#add-article-form').serialize();
        content += '&article_data=' + vditor.getHTML();
        content += '&article_status=' + option;
        // console.log(content)
        $.ajax({
            url: '/create/article/',
            type: 'post',
            // data: $('#add-article-form').serialize(),
            data: content,
            dataType: 'JSON',
            headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
            success: function (res) {
                //添加错误消息
                if (res.status === 400) {
                    $('.error').empty();
                    for (var error in res.msg) {
                        $('#id_' + error).next().text(res.msg[error][0])
                    }
                }
                if (res.status === 200) {
                    alert(res.msg)
                    $('#myModal').css('display', 'none');
                }
            }
        })
    }

    return vditor
}


//添加封面图片
function CoverImg() {
    let csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
    let flag = 0
    let labbtn = 0//判断更换还是添加
    $('#btn-img').change(() => {
            let file = $('#btn-img').get(0).files[0];
            let formData = new FormData();//生存formdata对象
            formData.append("img", file);//添加键值与对象
            formData.append('labflag', labbtn)
            if (labbtn === 1) {
                //获取背景图片的地址的css
                let imgurl = $('#article-img').css("background-image");
                // console.log(imgurl);
                //获取图片的url
                let temp = imgurl.split('\"')[1];
                // console.log(temp)
                //获取图片的名称
                let url = temp.split('/')
                let imgname = url[url.length - 1]
                // console.log(imgname)
                formData.append('imgname', imgname)
            }
            //console.log(file)
            //向后台发送图像
            if (file) {
                $.ajax({
                    type: 'post',
                    url: '/upload/cover/img/',
                    data: formData,
                    processData: false,//不希望发送的数据序列化
                    contentType: false,//不检查数据的类型
                    headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
                    success: function (data) {
                        // console.log(data);
                        //显示图片
                        $('#article-img').addClass('article-cover-size')
                            .css("background-image", "url(" + window.location.origin + "/" + data.url + ")")
                        $('.button-img').css('visibility', ' hidden')

                        flag += 1
                        //只在第一次添加页面点击添加页面时才添加页面
                        if (flag === 1) {
                            //添加修改图片的标签
                            htmltext = "<input type=\"button\" name=\"btn-mod-img\" class=\"btn-mod-img\" id=\"btn-mod-img\" value=\"编辑封面\">\n" +
                                "                    <div class=\"mod-select-content\" id=\"mod-select-content\">\n" +
                                "                        <div style=\"height: 8px;background-color: white\"></div>\n" +
                                // "                        <input type=\"file\" class=\"btn-img-file\"  name=\"选择封面\" accept=\"image/*\">\n" +
                                "                        <label for=\"btn-img\" id=\"lab-modimg\"><span class=\"span1\" ><i class=\"gg-image\"></i></span><span class=\"span2\">更换封面</span></label>\n" +
                                "                        <button id=\"btn-delimg\"><span class=\"span1\"><i class=\"gg-trash\"></i></span><span class=\"span2\">删除封面</span></button>\n" +
                                "                    </div>"
                            $('#mod-img-container').append(htmltext)
                            /*动态显示修改的框架,等控件出现后才可以添加click事件*/
                            $('#btn-mod-img').click(function () {
                                // console.log('点击了')
                                let cssstyle = $('#mod-select-content').css('visibility');
                                if (cssstyle === 'hidden') {
                                    $('#mod-select-content').css('visibility', 'visible');
                                } else {
                                    $('#mod-select-content').css('visibility', 'hidden');
                                }
                            })
                            //修改封面的点击事件
                            $('#lab-modimg').click(() => {
                                labbtn = 1
                            })
                            //删除封面的点击事件
                            $('#btn-delimg').click(() => {
                                //获取背景图片的地址的css
                                let imgurl = $('#article-img').css("background-image");
                                //获取图片的url
                                let temp = imgurl.split('\"')[1];
                                //获取图片的名称
                                let url = temp.split('/')
                                let imgname = url[url.length - 1]
                                $.ajax({
                                    type: 'post',
                                    url: '/upload/cover/img/',
                                    data: {
                                        'imgname': imgname,
                                    },
                                    headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
                                    dataType: 'JSON',
                                    success: function (data) {
                                        $('#btn-mod-img').remove()
                                        $('#mod-select-content').remove()
                                        $('#article-img').removeClass('article-cover-size')
                                        $('#article-img').css("background-image", "")
                                        $('.button-img').css('visibility', ' visible')
                                        flag = 0
                                        labbtn = 0
                                    }
                                })
                            })
                        }
                    }
                })

            }
        }
    )

}

//发表文章的模态框
function PublishArticle() {
    let csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
    $.ajax({
        url: '/create/publish/',
        type: 'post',
        dataType: 'JSON',
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        success: function (res) {
            // console.log(res.fcatagory)
            // console.log(res.fcatagory[0][1])
            //插入分类标签
            let html1 = "<select class=\"fcatagory\" id=\"fcatagory\"><option value=\"\" selected=\"\">---------</option>"
            $.each(res.fcatagory, (ind, item) => {
                html1 += "<option class=\"opt-fcat\" value=" + item[0] + ">" + item[1] + "</option>";
            })
            html1 += "</select>";
            // console.log(html1);
            $('#id_category').before(html1);
            $('#id_category').empty();
            //父分类改变更新子分类
            $('#fcatagory').change(() => {
                $('#id_category').empty();
                let fcatagory_id = $('#fcatagory').val()
                $.ajax({
                    url: '/create/publish/',
                    type: 'post',
                    data: {
                        'fcatagory_id': fcatagory_id,
                    },
                    dataType: 'JSON',
                    headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
                    success: function (res) {
                        if (res.status) {
                            let html2 = "";
                            $.each(res.catagory, (ind, item) => {
                                html2 += "<option class=\"opt-fcat\" value=" + item[0] + ">" + item[1] + "</option>";
                            })
                            $('#id_category').append(html2)
                        } else {
                            alert('该分类没有子分类')
                        }
                    }
                })
            })
            //添加父标签
            html1 = "<select class=\"ftag\" id=\"ftag\"><option value=\"\" selected=\"\">---------</option>"
            $.each(res.ftag, (ind, item) => {
                html1 += "<option class=\"opt-ftag\" value=" + item[0] + ">" + item[1] + "</option>";
            })
            html1 += "</select>";
            $('#id_tag').before(html1);
            $('#id_tag').empty();
            //父标签改变子标签改变
            $('#ftag').change(() => {
                $('#id_tag').empty();
                let ftag_id = $('#ftag').val()
                $.ajax({
                    url: '/create/publish/',
                    type: 'post',
                    data: {
                        'ftag_id': ftag_id,
                    },
                    dataType: 'JSON',
                    headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
                    success: function (res) {
                        if (res.status2) {
                            let html2 = "";
                            $.each(res.tag, (ind, item) => {
                                html2 += "<option class=\"opt-fcat\" value=" + item[0] + ">" + item[1] + "</option>";
                            })
                            $('#id_tag').append(html2)
                        } else {
                            alert('该标签没有子标签')
                        }
                    }
                })
            })
        }
    })
    //添加一键获取摘要
    html3 = "<button type=\"button\" class=\"btn-get-digest\" id=\"btn-get-digest\">一键获取</button>"
    $('#id_article_digest').next().after(html3)
    //添加封面图片的显示
    html4 = "<img id=\"show-article-cover\" src=\"#\" alt=\"无封面图\">"
    $('#id_article_img').after(html4)
    //发表文章按钮
    $('.btn-publication').click(() => {
        $('#myModal').css('display', 'block');
        $('#id_article_title').val($('#title').val())
        //先清空digest
        $('#id_article_digest').val('');
        //模态框封面显示
        if ($("#article-img").attr('"background-image"')) {
            //获取背景图片的地址的css
            let imgurl = $('#article-img').css("background-image");
            //获取图片的url
            let temp = imgurl.split('\"')[1];
            //获取图片的名称
            let url = temp.split('/')
            let imgname = url[url.length - 1]
            $('#show-article-cover').attr('src', temp)
            $('#id_article_img').val(imgname)
        }
    })
    //模态框的关闭
    $('.close').click(() => {
        $('#myModal').css('display', 'none')
    })
    //取消按钮
    $('#btnCansel').click(() => {
        $('#myModal').css('display', 'none');
    })
}