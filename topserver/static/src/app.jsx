import React from 'react';
import {render} from 'react-dom';
import Hello from './components/hello.jsx';

var App = React.createClass({
    render: function () {
        return <Hello />
    }
});

render(
    <App />,
    document.getElementById('app')
);
