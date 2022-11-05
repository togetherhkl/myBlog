$(document).ready(function () {
    InfoShow()
    ModalOption()
    ArticleTop()
    BarChart()
    LatestPopular()
})
var csrfToken = $("[name='csrfmiddlewaretoken']").val();//获取前端的csrf的taken值
function InfoShow(){
    /**
     * 个人信息轮播图
     * */
    var mySwiper = new Swiper('#info-swiper', {
            //direction: 'vertical', // 垂直切换选项
            loop: true, // 循环模式选项
            // 如果需要分页器
            pagination: {
                el: '.swiper-pagination',
            },
            speed: 300,
            autoplay: {
                delay: 3000
            },
        })
}
function ModalOption() {
    /**
     * 个人信息的模态框展示
     * */
    $('#base-info-btn').click(function () {
        $('#base-info-modal').iziModal('open', this)
    })
    $('#educate-info-btn').click(function () {
        $('#educate-info-modal').iziModal('open', this)
    })
    $('#society-info-btn').click(function () {
        $('#society-info-modal').iziModal('open', this)
    })
    $('#project-info-btn').click(function () {
        $('#project-info-modal').iziModal('open', this)
    })
    $('#base-info-modal').iziModal({
        title: "基础信息",
        subtitle: "",
        theme: "",
        headerColor: "#88A0B9",
        overlayColor: "rgba(0, 0, 0, 0.4)",
        iconColor: "",
        iconClass: null,
        width: 600,
        padding: 10,
    });
    $('#educate-info-modal').iziModal({
        title: "教育背景",
        subtitle: "",
        theme: "",
        headerColor: "#88A0B9",
        overlayColor: "rgba(0, 0, 0, 0.4)",
        iconColor: "",
        iconClass: null,
        width: 600,
        padding: 10,
    });
    $('#society-info-modal').iziModal({
        title: "社会实践",
        subtitle: "",
        theme: "",
        headerColor: "#88A0B9",
        overlayColor: "rgba(0, 0, 0, 0.4)",
        iconColor: "",
        iconClass: null,
        width: 600,
        padding: 10,
    });
    $('#project-info-modal').iziModal({
        title: "项目经历",
        subtitle: "",
        theme: "",
        headerColor: "#88A0B9",
        overlayColor: "rgba(0, 0, 0, 0.4)",
        iconColor: "",
        iconClass: null,
        width: 600,
        padding: 10,
    });
}
function ArticleTop() {
    /**
     * 推荐文章的展示
     * */
    $.ajax({
        url: '/home/display/',
        type: 'post',
        data: {'type': 'get_article_top'},
        dataType: 'JSON',
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        success: function (res) {
            // console.log(res)
            let temphtml = ''
            $.each($.parseJSON(res.article_set), (ind, item) => {
                temphtml += '<div class="swiper-slide">\n' +
                    '                            <img src="/media/article-cover-img/' + item['fields']['article_img'] + '" alt="">\n' +
                    '                            <a class="article-title" href="/article/' + item['pk'] + '/show/page/">' + item['fields']['article_title'] + '</a>\n' +
                    '                        </div>'
            })
            $('#article-swiper-wrapper').html(temphtml)
            var articleSwiper = new Swiper('#article-swiper', {
                //direction: 'vertical', // 垂直切换选项
                loop: true, // 循环模式选项
                // 如果需要分页器
                pagination: {
                    el: '.swiper-pagination',
                },
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                speed: 300,
                autoplay: {
                    delay: 5000
                },
            })
        }
    })
}
function BarChart() {
    /**
     * 柱状图的显示
     * */
    var myChart = echarts.init(document.getElementById('bar-chart'));
    var option;
    option = {
        title: {
            text: '博客分类数据',
            left: 'center'
        },
        xAxis: {
            type: 'category',
            data: [],
            name: '分类',
            axisLabel:{
                rotate:45,
                margin:8 ,
            },
        },
        yAxis: {
            type: 'value',
            name: '数量'
        },
        tooltip: {
            trigger: 'axis',
        },
        series: [
            {
                data: [],
                type: 'bar'
            }
        ]
    };
    $.ajax({
        url: '/home/display/',
        type: 'post',
        data: {'type': 'barchar'},
        dataType: 'JSON',
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        success: function (res) {
            option.xAxis.data = res.xAxis_data
            // console.log(res.xAxis_data)
            option.series[0].data = res.series_data
            myChart.setOption(option);
        }
    })
}
function LatestPopular(){
    /**
     * 最新文章，和热门文章的数据
     * */
    //最近文章
    $.ajax({
        url: '/home/display/',
        type: 'post',
        data: {'type': 'latest'},
        dataType: 'JSON',
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        success: function (res) {
            let temphtml=''
            $.each($.parseJSON(res.latest), (ind, item) => {
                temphtml+='<a href="/article/' + item['pk'] + '/show/page/">'+(ind+1)+'. ' + item['fields']['article_title'] + '</a>'
            })
            $('.latest-list').html(temphtml)
        }
    })
    //最新文章
    $.ajax({
        url: '/home/display/',
        type: 'post',
        data: {'type': 'popular'},
        dataType: 'JSON',
        headers: {"X-CSRFToken": csrfToken,},//添加crsf验证
        success: function (res) {
            let temphtml=''
            $.each($.parseJSON(res.popular), (ind, item) => {
                temphtml+='<a href="/article/' + item['pk'] + '/show/page/">'+(ind+1)+'. ' + item['fields']['article_title'] + '</a>'
            })
            $('.popular-list').html(temphtml)
        }
    })

}