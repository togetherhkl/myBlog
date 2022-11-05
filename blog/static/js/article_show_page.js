$(document).ready(function () {
    InitModal();
    CommentShow();
    ArticleDetail();
    Render();
    VEdit();
})
let csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
function Render() {
    page_id = article_id
    $.ajax({
        url: '/article/get/content/',
        type: 'post',
        data: {'page_id': page_id},
        dataType: 'JSON',
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        success: function (res) {
            const outlineElement = document.getElementById('outline')
            const previewElement = document.getElementById('preview')
            //{#let markdown='# 1.标题'#}
            // console.log(res.msg)
            // let markdown = Vditor.html2md(res.page)
            let markdown = res.page

            // console.log(markdown)

            Vditor.preview(previewElement, markdown, {
                markdown: {
                    toc: true,
                },
                speech: {
                    enable: true,
                },
                anchor: 1,
                after() {
                    if (window.innerWidth <= 768) {
                        return
                    }
                    Vditor.outlineRender(previewElement, outlineElement)
                    if (outlineElement.innerText.trim() !== '') {
                        outlineElement.style.display = 'block'
                    }
                },
                renderers: {
                    renderHeading: (node, entering) => {
                        const id = Lute.GetHeadingID(node)
                        if (entering) {
                            return [
                                `<h${node.__internal_object__.HeadingLevel} id="${id}" class="vditor__heading"><span class="prefix"></span><span>`,
                                Lute.WalkContinue]
                        } else {
                            return [
                                `</span><a id="vditorAnchor-${id}" class="vditor-anchor" href="#${id}"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h${node.__internal_object__.HeadingLevel}>`,
                                Lute.WalkContinue]
                        }
                    },
                },
            })
            window.setTheme = (theme) => {
                if (theme === 'dark') {
                    Vditor.setCodeTheme('native')
                    outlineElement.classList.add('dark')
                    document.querySelector('html').style.backgroundColor = '#2f363d'
                } else {
                    Vditor.setCodeTheme('github')
                }
            }
        }
    })
}

function InitModal() {
    $('#success-comment-modal').iziModal({
        title: "提示",
        subtitle: "",
        theme: "",
        headerColor: "#27733e",
        overlayColor: "rgba(0, 0, 0, 0.4)",
        iconColor: "",
        iconClass: null,
        width: 400,
         height:200,
        padding: 10,
    });
}

function VEdit() {
    /**
     * 发表评论功能
     * */
    var csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
    var vditor = new Vditor(document.getElementById('vditor'), {
        cache: {
            enable: false
        },
        "height": 370,
        "width": 250,
        //字数统计
        counter: {
            enable: true,
            max: 400,//最多400字
        },
        //固定头部栏
        "toolbarConfig": {
            "hide": true,
        },
        //显示大纲
        "outline": {
            "enable": false,
        },
        "value": " ",
        "mode": "ir",/*及时渲染模式*/
        "preview": {
            "hljs": {
                "style": "native",//代码颜色主题
                "lineNumber": true,//启动行号
            }
        },
    })
    $('#publish-comment').click(function () {
        $.ajax({
            url: '/article/show/',
            type: 'post',
            data: {
                'article_id': page_id,
                'comment': vditor.getValue(),
                'type': 'add_comment'
            },
            dataType: 'JSON',
            headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
            success: function (res) {
                if (res.status === 200) {
                    $('#success-comment-modal').iziModal('open', this)
                }
                if (res.status === 400) {
                    alert(res.msg)
                }
            }
        })
    })
    document.getElementById('vditor').append(vditor)
}
//转换时间格式
function getMyDate(str) {
    /**
     * 对后台传过来的时间转换成可识别状态
     * */
    var oDate = new Date(str),
        oYear = oDate.getFullYear(),
        oMonth = oDate.getMonth() + 1,
        oDay = oDate.getDate(),
        oHour = oDate.getHours(),
        oMin = oDate.getMinutes(),
        oSen = oDate.getSeconds(),
        oTime = oYear + '-' + getzf(oMonth) + '-' + getzf(oDay);//最后拼接时间

//补0操作
    function getzf(num) {
        if (parseInt(num) < 10) {
            num = '0' + num;
        }
        return num;
    }
    return oTime;
}
function CommentShow(){
    page_id = article_id
    $.ajax({
        url: '/article/show/',
        type: 'post',
        data: {
                'article_id': page_id,
                'type':'get_comment',
            },
        dataType: 'JSON',
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        success:function(res){
            // console.log(res)
            temphtml='';
            $.each(res.values,(ind,item)=>{
                temphtml+='<div class="one-comment">\n' +
                    '                            <span class="author">'+item['user__user_name']+'：</span>\n' +
                    '                            <span class="date">'+getMyDate(item['comment_createdate'])+'</span>\n' +
                    '                        </div>\n' +
                    '                        <p class="comment-text">'+item['comment_content']+'</p>'
            })
            $('#comment').html(temphtml)
        }
    })
}

function ArticleDetail(){
    page_id = article_id
    $.ajax({
        url: '/article/show/',
        type: 'post',
        data: {
            'article_id': page_id,
            'type': 'article_detail',
        },
        dataType: 'JSON',
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        success:function (res){
            console.log(res)
            temphtml='<div class="detail-item"><span>标题：</span>'+res.article_detail[0]['article_title']+'</div>\n' +
                '  <div class="detail-item"><span>作者：</span>'+res.article_detail[0]['user__user_name']+'</div>\n' +
                '  <div class="detail-item"><span>发表时间：</span>'+getMyDate(res.article_detail[0]['article_createdate'])+'</div>\n' +
                '  <div class="detail-item"><span>最近更新时间：</span>'+getMyDate(res.article_detail[0]['article_updatedate'])+'</div>\n' +
                '  <div class="detail-item tags"><span>标签：</span>\n'
            $.each(res.tags,(ind,item)=>{
                temphtml+='<a href="#" value='+item['tag_id']+'>'+item['tag__tag_name']+'</a>'
            })
            temphtml+='</div>'
            $('.article-info-detail').html(temphtml)
        }
    })
}