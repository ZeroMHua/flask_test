var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据


$(function () {
    // 获取首页新闻信息
    updateNewsData();

    // 首页分类切换
    $('.menu li').click(function () {
        // 获取点击分类的id
        var clickCid = $(this).attr('data-cid');

        $('.menu li').each(function () {
            $(this).removeClass('active');
        });

        $(this).addClass('active');

        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid;

            // 重置分页参数
            cur_page = 1;
            total_page = 1;
            updateNewsData();
        }
    });

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100) {
            // TODO 判断页数，去更新新闻数据
            // 判断`是否正在向服务器请求获取数据`
            if (!data_querying) {
                // 设置`是否正在向服务器请求获取数据`data_querying为true
                // 防止页面滚动时多次向服务器请求数据
                data_querying = true;

                // 判断是否还有`下一页`，如果有则获取`下一页`内容
                if (cur_page < total_page) {
                    updateNewsData();
                }
                else {
                    data_querying = false;
                }
            }
        }
    })
});

// 获取指定页码的`分类新闻信息`
function updateNewsData() {
    // 组织参数
    var params = {
        "cid": currentCid,
        "page": cur_page,
        "per_page": 10
    };

    // TODO 更新新闻数据
    $.ajax({
        url: '/news',
        type: 'get',
        data: params,
        success: function (resp) {
            // 设置`是否正在向后端请求数据标志`data_querying=false
            data_querying = false;

            if (resp.errno == '0') {
                // 获取`分类新闻信息`成功
                // 设置分页之后`总页数`
                total_page = resp.total_page;

                if (cur_page == 1) {
                    // 首先清空页面原有的内容
                    $(".list_con").html("");
                }

                // 获取返回的新闻信息
                var news_li = resp.news_li;

                // 遍历news_li获取每个新闻的信息并展示在页面上
                for (var i=0; i < news_li.length; i++) {
                    // 获取每个新闻信息
                    var news = news_li[i];

                    // 拼接新闻显示内容
                    var content = '<li>';
                    content += '<a href="/news/' + news.id + '" class="news_pic fl"><img src="' + news.index_image_url + '?imageView2/1/w/170/h/170"></a>';
                    content += '<a href="/news/' + news.id + '" class="news_title fl">' + news.title + '</a>';
                    content += '<a href="/news/' + news.id + '" class="news_detail fl">' + news.digest + '</a>';
                    content += '<div class="author_info fl">';
                    content += '<div class="source fl">来源：' + news.source + '</div>';
                    content += '<div class="time fl">' + news.create_time + '</div>';
                    content += '</div>';
                    content += '</li>';

                    // 将新闻显示内容添加到首页上
                    $(".list_con").append(content);
                }

                // 设置页码加1
                cur_page += 1;
            }
            else
            {
                // 获取`分类新闻信息`失败
                alert(resp.errmsg);
            }
        }
    })
}
