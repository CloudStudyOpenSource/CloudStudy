function cs_checkLogin() {}

function cs_login(email, pwd) {
    $.ajax({
        method: 'GET',
        url: '/api/login',
        async: false,
        headers: {
            cs_email: email,
            cs_password: sha512(pwd)
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.message == "success") {
                Cookies.set("cs_token", data.data, {
                    expires: 0.5, //day
                    path: '/'
                })
                window.location.href = "/dashbroad"
            } else {
                $("#result").html(data.data);
            }
        }
    });
}

function cs_register(name, email, pwd) {
    $.ajax({
        method: 'GET',
        url: '/api/register',
        async: false,
        headers: {
            cs_name: name,
            cs_email: email,
            cs_password: sha512(pwd)
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.message == "success") {
                mdui.alert('', '注册成功', function () {
                    window.location.href = "/login"
                }, {
                    modal: true,
                    closeOnEsc: false,
                    history: false
                });
            } else {
                $("#result").html(data.data);
            }
        }
    });
}