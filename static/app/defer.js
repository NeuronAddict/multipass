domain = document.currentScript.getAttribute('domain');
defered = document.currentScript.getAttribute('defered');

if (defered === undefined || defered === null || defered === '') {
    throw 'No defered attribute';
}

if (domain === undefined || domain === null || domain === '') {
    throw 'No domain attribute';
}

// Add a script element as a child of the body
function downloadJSAtOnload() {
    const element = document.createElement("script");
    element.setAttribute('domain', domain);
    element.src = defered;
    document.body.appendChild(element);
}

// Check for browser support of event handling capability
if (window.addEventListener)
    window.addEventListener("load", downloadJSAtOnload, false);
else if (window.attachEvent)
    window.attachEvent("onload", downloadJSAtOnload);
else window.onload = downloadJSAtOnload;