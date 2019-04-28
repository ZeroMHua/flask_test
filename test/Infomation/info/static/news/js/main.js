$(function(){

	// 打开登录框
	$('.login_btn').click(function(){
        $('.login_form_con').show();
	});
	
	// 点击关闭按钮关闭登录框或者注册框
	$('.shutoff').click(function(){
		$(this).closest('form').hide();
	});

    // 隐藏错误
    $(".login_form #mobile").focus(function(){
        $("#login-mobile-err").hide();
    });
    $(".login_form #password").focus(function(){
        $("#login-password-err").hide();
    });

    $(".register_form #mobile").focus(function(){
        $("#register-mobile-err").hide();
    });
    $(".register_form #imagecode").focus(function(){
        $("#register-image-code-err").hide();
    });
    $(".register_form #smscode").focus(function(){
        $("#register-sms-code-err").hide();
    });
    $(".register_form #password").focus(function(){
        $("#register-password-err").hide();
    });


	// 点击输入框，提示文字上移
	$('.form_group').on('click focusin',function(){
		$(this).children('.input_tip').animate({'top':-5,'font-size':12},'fast');
	});

	// 输入框失去焦点，如果输入框为空，则提示文字下移
	$('.form_group input').on('blur focusout',function(){
		$(this).parent().removeClass('hotline');
		var val = $(this).val();
		if(val=='')
		{
			$(this).siblings('.input_tip').animate({'top':22,'font-size':14},'fast');
		}
	});


	// 打开注册框
	$('.register_btn').click(function(){
		$('.register_form_con').show();
		// 打开注册框架时调用`获取图片验证码`函数
		generateImageCode();
	});


	// 登录框和注册框切换
	$('.to_register').click(function(){
		$('.login_form_con').hide();
		$('.register_form_con').show();
		// 打开注册框架时调用`获取图片验证码`函数
        generateImageCode();
	});

	// 登录框和注册框切换
	$('.to_login').click(function(){
		$('.login_form_con').show();
		$('.register_form_con').hide();
	});

	// 根据地址栏的hash值来显示用户中心对应的菜单
	var sHash = window.location.hash;
	if(sHash!=''){
		var sId = sHash.substring(1);
		var oNow = $('.'+sId);		
		var iNowIndex = oNow.index();
		$('.option_list li').eq(iNowIndex).addClass('active').siblings().removeClass('active');
		oNow.show().siblings().hide();
	}

	// 用户中心菜单切换
	var $li = $('.option_list li');
	var $frame = $('#main_frame');

	$li.click(function(){
		if($(this).index()==5){
			$('#main_frame').css({'height':900});
		}
		else{
			$('#main_frame').css({'height':660});
		}
		$(this).addClass('active').siblings().removeClass('active');
		$(this).find('a')[0].click();
	});

    // TODO 登录表单提交
    $(".login_form_con").submit(function (e) {
        // 阻止表单默认提交
        e.preventDefault();

        // 获取参数
        var mobile = $(".login_form #mobile").val();
        var password = $(".login_form #password").val();

        if (!mobile) {
            $("#login-mobile-err").show();
            return;
        }

        if (!password) {
            $("#login-password-err").show();
            return;
        }

        // 组织参数
        var params = {
            "mobile": mobile,
            "password": password
        };

        // TODO 发起登录请求
        $.ajax({
            url: '/passport/login',
            type: 'post',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            contentType: 'application/json',
            data: JSON.stringify(params),
            dataType: 'json',
            success: function (resp) {
                if (resp.errno == '0') {
                    // `登录`成功
                    // 刷新当前页面
                    location.reload();
                }
                else {
                    // `登录`失败
                    $("#login-password-err").html(resp.errmsg).show();
                }
            }
        })

    });


    // TODO 注册按钮点击
    $(".register_form_con").submit(function (e) {
        // 阻止默认提交操作
        e.preventDefault();

		// 取到用户输入的内容
        var mobile = $("#register_mobile").val();
        var smscode = $("#smscode").val();
        var password = $("#register_password").val();

		if (!mobile) {
            $("#register-mobile-err").show();
            return;
        }
        if (!smscode) {
            $("#register-sms-code-err").show();
            return;
        }
        if (!password) {
            $("#register-password-err").html("请填写密码!");
            $("#register-password-err").show();
            return;
        }

		if (password.length < 6) {
            $("#register-password-err").html("密码长度不能少于6位");
            $("#register-password-err").show();
            return;
        }

        // 注册参数
        var params = {
		    "mobile": mobile,
            "sms_code": smscode,
            "password": password
        };

        // TODO 发起注册请求
        $.ajax({
            url: '/passport/register',
            type: 'post',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            contentType: 'application/json',
            data: JSON.stringify(params),
            dataType: 'json',
            success: function (resp) {
                if (resp.errno == '0') {
                    // `注册`成功
                    // 刷新当前页面
                    location.reload();
                }
                else {
                    // `注册`失败
                    // 在页面上显示错误信息
                    $('#register-password-err').html(resp.errmsg).show();
                }
            }
        })

    });

    // TODO 用户退出功能
    $('#logout').click(function () {
        // 请求`退出登录`
        $.ajax({
            url: '/passport/logout',
            type: 'post',
            // 在发起post请求时，将csrf_token的值放在请求头中传递的服务器
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '0') {
                    // `退出登录`成功
                    location.reload();
                }
            }
        })
    })

});

var imageCodeId = "";

// TODO 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    // 产生图片验证码标识(uuid)
    imageCodeId = generateUUID();

    // 获取图片验证码img标签并设置它的src属性
    // prop
    $('.get_pic_code').attr('src', '/passport/image_code?image_code_id=' + imageCodeId);
}

// 发送短信验证码
function sendSMSCode() {
    // 移除获取验证码a标签的点击事件
    $(".get_code").removeAttr("onclick");

    // 前端校验参数，保证输入框有数据填写
    var mobile = $("#register_mobile").val();
    if (!mobile) {
        $("#register-mobile-err").html("请填写正确的手机号！");
        $("#register-mobile-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err").html("请填写验证码！");
        $("#image-code-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }

    // TODO 发送短信验证码
    // 组织参数
    var params = {
        "mobile": mobile,
        "image_code": imageCode,
        "image_code_id": imageCodeId
    };

    // TODO 发送ajax请求，请求发送短信验证码
    $.ajax({
        url: '/passport/sms_code',  // 请求的url地址
        type: 'post', // 请求方式，默认'get'
        headers: {
            'X-CSRFToken': getCookie('csrf_token')
        },
        contentType: 'application/json', // 指定给服务器发送数据的类型
        data: JSON.stringify(params), // 给服务器传递的数据
        dataType: 'json', // 服务器返回的数据的类型
        success: function (resp) {
            // 回调函数
            // alert('发送短信');
            // console.log(resp);
            if (resp.errno == '0') {
                // `发送短信`成功
                // 倒计时60s
                var num = 60;
                var tid = setInterval(function () {
                    if (num <= 0) {
                        // 倒计时完成
                        // 清除定时器
                        clearInterval(tid);
                        // 重置`点击获取验证码`内容
                        $('.get_code').html('点击获取验证码');
                        // 给`点击获取验证码`添加点击事件
                        $(".get_code").attr("onclick", "sendSMSCode();");
                    }
                    else {
                        // 在页面上提示倒计时剩余秒数
                        $('.get_code').html(num+'秒');
                        // 倒计时剩余秒数减1
                        num -= 1;
                    }

                }, 1000);
            }
            else {
                // `发送短信`失败
                $("#register-sms-code-err").html(resp.errmsg).show();
                // 给`点击获取验证码`a标签添加点击事件
                $(".get_code").attr("onclick", "sendSMSCode();");
            }
        }
    })

}

// 调用该函数模拟点击左侧按钮
function fnChangeMenu(n) {
    var $li = $('.option_list li');
    if (n >= 0) {
        $li.eq(n).addClass('active').siblings().removeClass('active');
        // 执行 a 标签的点击事件
        $li.eq(n).find('a')[0].click()
    }
}

// 一般页面的iframe的高度是660
// 新闻发布页面iframe的高度是900
function fnSetIframeHeight(num){
	var $frame = $('#main_frame');
	$frame.css({'height':num});
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}
