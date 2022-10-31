$(document).ready(function () {
    Pagination()
})

function Pagination() {


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
        page_str_list += `<li><a class="width-auto" href="${changeURLArg(window.location.href, 'page', 1)}">首页</a></li>`;
        // # 添加上一页
        if (page > 1) {
            prev = `<li><a class="width-auto" href="${changeURLArg(window.location.href, 'page', page - 1)}">上一页</a></li>`;
        } else {
            prev = `<li><a class="width-auto" href="${changeURLArg(window.location.href, 'page', 1)}">上一页</a></li>`;
        }
        page_str_list += prev;
        for (i = show_start_page; i < (show_end_page + 1); i++) {
            if (i == page) {
                ele = `<li><a class="active" href="${changeURLArg(window.location.href, 'page', i)}">${i}</a></li>`;
            } else {
                ele = `<li><a href="${changeURLArg(window.location.href, 'page', i)}">${i}</a></li>`;
            }
            page_str_list += ele;
        }
        // # 添加下一页
        if (page < page_count) {
            prev = `<li><a class="width-auto" href="${changeURLArg(window.location.href, 'page', page + 1)}">下一页</a></li>`;
        } else {
            prev = `<li><a class="width-auto" href="${changeURLArg(window.location.href, 'page', page_count)}">下一页</a></li>`;
        }
        page_str_list += prev;
        // # 添加尾页
        page_str_list += `<li><a class="width-auto" href="${changeURLArg(window.location.href, 'page', page_count)}">尾页</a></li>`;
        labclass.innerHTML = page_str_list;
    }

//修改URL中的参数值
    function changeURLArg(url, arg, arg_val) {
        var pattern = arg + '=([^&]*)';//匹配url中除了&的字符串，并且前面是=号的，匹配0次或者多次
        var replaceText = arg + '=' + arg_val;
        if (url.match(pattern)) {//如果URL中包含要匹配的字段
            var tmp = '/(' + arg + '=)([^&]*)/gi';//忽略大小写的全局匹配
            tmp = url.replace(eval(tmp), replaceText);//eval将tmp以代码的方式执行
            return tmp;
        } else {//如果url中不包含要匹配的字段
            if (url.match('[\?]')) {//p匹配？，如果有？号
                return url + '&' + replaceText;
            } else {//如果没有？号，则添加？
                return url + '?' + replaceText;
            }
        }
        return url + '\n' + arg + '\n' + arg_val;//如果失败则返回字段
    }

//跳转功能
    $('#skip-page').click(function () {
        page = $('#page-input').val()
        if (page === "" || isNaN(page)) {
            alert('请输入要跳转的页码')
        }
        if (page > page_count) {
            alert('超出范围')
        } else {
            skipurl = changeURLArg(window.location.href, 'page', page)
            window.location.href = skipurl
        }
    })
}