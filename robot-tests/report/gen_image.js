var system = require('system');
var args = system.args;
var page = require('webpage').create();
page.open(args[1], function (status) {
    console.log("Status: " + status);
    if (status === "success") {
        page.render(args[2]);
    }
    phantom.exit();
});
