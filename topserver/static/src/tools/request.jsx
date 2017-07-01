function hello(){
    return 'hello';
}

function getJSON(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('get', url, true);
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');  // for debugging
    xhr.responseType = "json";
    xhr.onload = function() {
        var status = xhr.status;
        if (status == 200) {
            callback(xhr.response);
        }
    };
    xhr.send();
    return null;
}

export {getJSON};