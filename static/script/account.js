function cs_checkLogin() {
    //console.log("token", Cookies.get("cs_token"))
    $.ajax({
        method: 'GET',
        url: '/api/checklogin',
        async: false,
        cache: false,
        success: function (data) {
            data = JSON.parse(data);
            //console.log("data", data)
            if (data.message == "success") {
                Cookies.set("cs_token", data.data, {
                    expires: 0.5,
                    path: '/'
                })
                if (window.location.pathname == "/login" || window.location.pathname == "/register") {
                    mdui.alert('', '您已登录', function () {
                        window.location.href = "/dashbroad"
                    }, {
                        modal: true,
                        closeOnEsc: false,
                        history: false
                    });
                }
            } else {
                Cookies.remove("cs_token")
                if (window.location.pathname == "/login" || window.location.pathname == "/register") { } else {
                    mdui.alert('', data.data, function () {
                        window.location.href = "/login"
                    }, {
                        modal: true,
                        closeOnEsc: false,
                        history: false
                    });
                }
            }
        }
    });

}

function cs_login(email, pwd) {
    $.ajax({
        method: 'GET',
        url: '/api/login',
        async: false,
        cache: false,
        headers: {
            cs_email: email,
            cs_password: sha512(pwd)
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.message == "success") {
                Cookies.set("cs_token", data.data, {
                    expires: 0.5,
                    path: '/'
                })
                window.location.href = "/dashbroad"
            } else {
                $("#result").html(data.data);
            }
        }
    });
}

function cs_register(name, email, pwd,redirect=true) {
    $.ajax({
        method: 'GET',
        url: '/api/register',
        async: false,
        cache: false,
        headers: {
            cs_name: name,
            cs_email: email,
            cs_password: sha512(pwd)
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.message == "success") {
                if (redirect == true) {
                    mdui.alert('', '注册成功', function () {
                        window.location.href = "/login"
                    }, {
                        modal: true,
                        closeOnEsc: false,
                        history: false
                    });
                } else {
                    return(true)
                }
            } else {
                $("#result").html(data.data);
            }
        }
    });
}

function cs_logout() {
    Cookies.remove("cs_token")
    cs_checkLogin()
}

