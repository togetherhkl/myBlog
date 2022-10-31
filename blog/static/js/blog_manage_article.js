$(document).ready(function () {
    AllPages()
    PubPages()
    ReclaimPages()
    AuditPages()
    DraftPages()
    DeleteFun()
    btnSure()
    StatuCategorySearch()
})

var search_op = 0//按状态查询的记录
function ArticleAjax(search_op, temppage,category=0,search_text='') {
    /**
     * 向后台发送ajax信息，刷新文章的显示
     * */
    let csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
    $.ajax({
        url: '/blog/manage/article/',
        type: 'post',
        data: {
            'search_op': search_op,
            'page': temppage,
            'category_id':category,
            'search_text':search_text
        },
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        dataType: 'JSON',
        success: function (res) {
            article_set = $.parseJSON(res.article_set)
            //设置分页参数
            page_count = res.page_count
            page = res.page
            show_start_page = res.show_start_page
            show_end_page = res.show_end_page
            // console.log(page_count, page)
            // console.log(article_set)
            //更新状态栏的文章数据
            let temp='全部('+res.article_all+')'
            $('#all-pages').text(temp)
            temp='已发表('+res.article_pub+')'
            $('#pub-pages').text(temp)
            temp='草稿('+res.article_draft+')'
            $('#draft-pages').text(temp)
            temp='审核中('+res.article_audit+')'
            $('#audit-pages').text(temp)
            temp='回收站('+res.article_delete+')'
            $('#reclaim-pages').text(temp)
            ArticleShow(article_set)
            Pagination()
        }
    })
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
        oTime = oYear + '年' + getzf(oMonth) + '月' + getzf(oDay) + '日 ' + getzf(oHour) + ':' + getzf(oMin);//最后拼接时间

//补0操作
    function getzf(num) {
        if (parseInt(num) < 10) {
            num = '0' + num;
        }
        return num;
    }
    return oTime;
}

let del_id//删除的id
let op_del//删除的方式
function DeleteFun() {
    //删除的动画效果
    $('.close').click(() => {
        $('.modal').css('display', 'none')
    })
    $('#btnCansel').click(() => {
        $('.modal').css('display', 'none')
    })
    $('.op-delete').click(function () {
        //放入回收站
        $('.modal').css('display', 'flex')
        $('.modal-header').css('background-color', '#9B703F')
        $('.prompt').text('删除提示')
        $('.modal-body .body-text p').text('删除的文章不会被彻底删除，会放入到回收站，如果想彻底删除，请进入回收站点击删除！')
        temp = $(this).attr('value')
        del_id = temp
        op_del = 'recycle'
    })
    $('.op-del-complete').click(function () {
        //彻底删除
        $('.modal').css('display', 'flex')
        $('.modal-header').css('background-color', 'red')
        $('.prompt').text('警告')
        $('.modal-body .body-text p').text('文章将会被彻底删除，删除后不能找回，请确认！')
        temp = $(this).attr('value')
        del_id = temp
        op_del = 'del_complete'
    })

}
function btnSure(){
    /**
     * 删除的确认按钮
     * */
    $('#btnSure').click(function () {
        console.log('ssss')
        let csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
        $.ajax({
            url: '/article/delete/',
            type: 'post',
            data: {
                'id': del_id,
                'op_del': op_del,
            },
            headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
            dataType: 'JSON',
            success: function (res) {
                if (res.status === 200) {
                    // console.log(res.msg)
                    alert(res.msg)
                    $('.modal').css('display', 'none')
                } else if (res.status === 400) {
                    // console.log(res.msg)
                    alert(res.msg)
                }
                //刷新页面
                ArticleAjax(search_op,1)
            }
        })
    })
}

function ArticleShow(article_set) {
    /**
     *局部刷新，草稿，发表，审核，全部，回收下的文章
     * */
    let del_option//放回回收站，或彻底删除
    if (search_op === 4) {//如果是回收操作
        del_option = 'op-del-complete'//彻底删除
    } else
        del_option = 'op-delete'//放回回收站
    temphtml = ''
    //循环每篇文章
    $.each(article_set, (ind, item) => {
        // console.log(getMyDate(item['fields']['article_createdate']))
        // console.log(item['fields']['article_title'])//获取文章的title

        temphtml += "<div class=\"one-article-op\">\n" +
            "                    <div class=\"one-header\">\n" +
            "                        <h2>" + item['fields']['article_title'] + "</h2>\n" +
            "                        <span>" + getMyDate(item['fields']['article_createdate']) + "</span>\n" +
            "                    </div>\n" +
            "                    <p>" + item['fields']['article_digest'] + "</p>\n" +
            "                    <div class=\"one-footer\">\n" +
            "                        <div class=\"entry-meta\">\n" +
            "                            <span class=\"view\">阅读量：" + item['fields']['article_view'] + " </span>\n" +
            "                            <span class=\"like\">点赞量：" + item['fields']['article_like'] + " </span>\n" +
            "                            <span class=\"comment\">评论数：" + item['fields']['article_comment'] + " </span>\n" +
            "                            <span class=\"collect\">收藏数：" + item['fields']['article_collect'] + "</span>\n" +
            "                        </div>\n" +
            "                        <div class=\"ont-op\">\n" +
            "                            <a href=\"/create/article/" + item['pk'] + "/mod/\" id=\"op-edit\">编辑</a>\n" +
            "                            <a href=\"/article/" + item['pk'] + "/show/page/\" id=\"op-view\">浏览</a>\n" +
            "                            <a href=\"#\" id=\"op-delete\" value=\"" + item['pk'] + "\" class=\"" + del_option + "\">删除</a>\n" +
            "                            <a href=\"#\" id=\"op-more\">更多</a>\n" +
            "                        </div>\n" +
            "                    </div>\n" +
            "                </div>"
    })
    temphtml += "<div class=\"pagination-div\">\n" +
        "                <ul class=\"pagination\"></ul>\n" +
        "                <div class=\"form-jump\">\n" +
        "                    <input type=\"text\" name=\"page\" id=\"page-input\">\n" +
        "                    <button id=\"skip-page\">跳转</button>\n" +
        "                </div>\n" +
        "            </div>"
    $('#article-option').html(temphtml)
    DeleteFun()
}

function AllPages() {
    /**
     * 展示所有的文章
     * */
    $('#all-pages').click(function () {
        $('.status-look span').each(function () {
            $(this).removeClass('status-active')
        })
        $(this).addClass('status-active')
        search_op = 0//发表
        ArticleAjax(search_op, 1)
    })
}

function DraftPages() {
    /**
     * 展现草稿的数目
     * */
    $('#draft-pages').click(function () {
        $('.status-look span').each(function () {
            $(this).removeClass('status-active')
        })
        $(this).addClass('status-active')
        search_op = 1//草稿
        ArticleAjax(search_op, 1)
    })
}

function PubPages() {
    /**
     * 展现发表的文章数目
     * */
    $('#pub-pages').click(function () {
        $('.status-look span').each(function () {
            $(this).removeClass('status-active')
        })
        $(this).addClass('status-active')
        search_op = 2//发表
        ArticleAjax(search_op, 1)
    })
}

function AuditPages() {
    /**
     * 展现审核的文章数目
     * */
    $('#audit-pages').click(function () {
        $('.status-look span').each(function () {
            $(this).removeClass('status-active')
        })
        $(this).addClass('status-active')
        search_op = 3//审核
        ArticleAjax(search_op, 1)
    })
}

function ReclaimPages() {
    /**
     * 展示回收站的所有文章
     * */
    $('#reclaim-pages').click(function () {
        $('.status-look span').each(function () {
            $(this).removeClass('status-active')
        })
        $(this).addClass('status-active')
        search_op = 4//审核
        ArticleAjax(search_op, 1)
    })
}

function StatuCategorySearch(){
    $('#search-btn').click(function (){
        search_op=5
        search_text=$('#search-text').val()
        catogory_id=$('#select-list').val()
        console.log(search_text,catogory_id)
        ArticleAjax(search_op,1,catogory_id,search_text)
    })
}

function Pagination() {
    /**
     * 基于ajax的分页逻辑
     * */
    //分页逻辑
//跳转页的隐藏
// if(typeof(page_count)!="undefined") {
    const jump = document.querySelector('.form-jump')
    const pagenation = document.querySelector('.pagination-div')
    if (page_count <= 1) {
        jump.style.visibility = "hidden";
    }
    if (page_count == 0) {
        pagenation.style.visibility = 'hidden'
    }
    /*
    * 给页面添加分页
    *
    * */
    const uls = document.querySelector('.pagination');
    PagInation(uls, page, show_start_page, show_end_page, page_count);

    function PagInation(labclass, page, show_start_page, show_end_page, page_count) {
        /*
        * labclass为需要添加分页的<ul>标签的类名
        * page:当前的页码
        * show_start_page：展现的页码数的开始
        * show_end_page：展现页码数的结尾
        * page_count：总共的页码数
        * */
// # 添加首页
        let page_str_list = "";
        let prev = '';
        let ele = '';
        page_str_list += `<li><a class="width-auto skip" page=1>首页</a></li>`;
        // # 添加上一页
        if (page > 1) {
            prev = `<li><a class="width-auto skip" page=${page-1}>上一页</a></li>`;
        } else {
            prev = `<li><a class="width-auto skip" page=1>上一页</a></li>`;
        }
        page_str_list += prev;
        for (i = show_start_page; i < (show_end_page + 1); i++) {
            if (i == page) {
                ele = `<li><a class="active skip" page=${i}>${i}</a></li>`;
            } else {
                ele = `<li><a  class="skip" page=${i}>${i}</a></li>`;
            }
            page_str_list += ele;
        }
        // # 添加下一页
        if (page < page_count) {
            prev = `<li><a class="width-auto skip" page=${page + 1}>下一页</a></li>`;
        } else {
            prev = `<li><a class="width-auto skip" page=${page_count}>下一页</a></li>`;
        }
        page_str_list += prev;
        // # 添加尾页
        page_str_list += `<li><a class="width-auto skip" page=${page_count}>尾页</a></li>`;
        labclass.innerHTML = page_str_list;
    }
    //点击每一页刷新
    $('.skip').click(function (){
        let page=$(this).attr('page')
        ArticleAjax(search_op,page)
    })
//跳转功能
    $('#skip-page').click(function () {
        page = $('#page-input').val()
        if (page === "" || isNaN(page)) {
            alert('请输入要跳转的页码')
        }
        if (page > page_count) {
            alert('超出范围')
        } else {
            ArticleAjax(search_op,page)
        }
    })
}