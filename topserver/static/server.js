const path = require('path');
const express = require('express');

var App = function () {
    const app = express();
    const indexPath = path.join(__dirname, 'index.html');
    const buildPath = express.static(path.join(__dirname, 'build'));
    const srcPath = express.static(path.join(__dirname, 'src'));
    const bowerPath = express.static(path.join(__dirname, 'bower_components'));

    app.use('/build', buildPath);
    app.use('/bower_components', bowerPath);
    app.use('/src', srcPath);
    app.get('/', function (_, res) { res.sendFile(indexPath) });

    return app
};

var app = App();
app.set('port', process.env.PORT || 5000);
app.listen(app.get('port'), function () {
        console.log('Express server listening on port ' + app.get('port'));
});
