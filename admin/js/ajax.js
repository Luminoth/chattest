function getHTTPObject()
{
    if(window.XMLHttpRequest)
        return new XMLHttpRequest();
    else if(window.ActiveXObject)
        return new ActiveXObject("Microsoft.XMLHTTP");
    return null;
}

var http = getHTTPObject();

function handleAuthenticationResponse()
{
    if(http && http.readyState == 4) {
        var ajax_results = document.getElementById('ajax_results');
        if(http.status != 200) {
            ajax_results.innerHTML = 'Server error: ' + http.status;
            return;
        }

        // get the controls
        var username = document.getElementById('username');
        var password = document.getElementById('password');
        var login = document.getElementById('login');

        // verify success
        var success = http.responseXML.getElementsByTagName('success').item(0);
        if(success == null) {
            ajax_results.innerHTML = http.responseXML.getElementsByTagName('error').item(0).firstChild.data;

            // unlock the controls
            username.disabled = false;
            password.disabled = false;
            password.value = "";
            login.disabled = false;
            return;
        }

        // forward on
        ajax_results.innerHTML = success.firstChild.data;
        window.location = "administration.php";
    }
}

function authenticate()
{
    if(http) {
        // get the controls
        var username = document.getElementById('username');
        var password = document.getElementById('password');
        var login = document.getElementById('login');

        // lock out the controls
        username.disabled = true;
        password.disabled = true;
        login.disabled = true;

        // build the params string
        var params = "username=" + escape(username.value)
                   + "&password=" + escape(password.value);

        // post the query
        http.open("POST", "authenticate.php", true);
        http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=utf-8");
        http.onreadystatechange = handleAuthenticationResponse;
        http.send(params);

        document.getElementById('ajax_results').innerHTML = 'Authenticating...';
    }
}
