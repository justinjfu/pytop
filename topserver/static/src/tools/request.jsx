function hello(){
    return 'hello';
}

function getJSON(url, callback, timeout_callback, error_callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('get', url, true);
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');  // for debugging
    xhr.responseType = "json";
    xhr.timeout = 5000;
    xhr.onload = function() {
        var status = xhr.status;
        if (status == 200) {
            callback(xhr.response);
        }else{
            error_callback(xhr.status);
        }
    };
    xhr.ontimeout = function (e) {
        timeout_callback()
    };
    xhr.send();
    return null;
}

export {getJSON};