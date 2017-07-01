import React from 'react';

var InfoPage = React.createClass({

    render: function () {
        if(this.props.host_name== null) {
            return <div className="big_info">
                Please select a machine
            </div>;
        }else if(this.props.cpu_data == null || this.props.gpu_data == null ) {
            return <div className="big_info">
                Loading data for {this.props.host_name}...
            </div>;
        }

        var gpu_display = null;

        var cpu_display = null;

        var gpu_data = this.props.gpu_data;
        if(gpu_data != null && gpu_data.hasOwnProperty('gpu')){
            var gpu_list = gpu_data.gpu.map(function(item, idx){
                return <tr key={idx}>
                        <td>{item.model}</td>
                        <td>{item.usage}</td>
                        <td>{item.memory_used}/{item.memory_total}</td>
                        <td>{item.temperature}</td>
                </tr>;
            });
            gpu_display = <div>
                <table className="table">
                    <tbody>
                    <tr>
                        <th>Model</th>
                        <th>Usage</th>
                        <th>Memory</th>
                        <th>Temp</th>
                    </tr>
                    {gpu_list}
                    </tbody>
                </table>

                Data Received: {gpu_data.timestamp}
            </div>;
        }

        var cpu_data = this.props.cpu_data;
        if(cpu_data != null && cpu_data.hasOwnProperty('processes')){
            var proc_list = cpu_data.processes.map(function(item, idx){
                return <tr key={idx}>
                    <td>{item.pid}</td>
                    <td>{item.cpu}</td>
                    <td>{item.user}</td>
                    <td>{item.cmd}</td>
                </tr>;
            });

            if(proc_list.length == 0){
                proc_list = <div>No processes</div>;
            }

            cpu_display = <div>
                <table className="table">
                    <tbody>
                    <tr>
                        <th>PID</th>
                        <th>CPU</th>
                        <th>User</th>
                        <th>Cmd</th>
                    </tr>
                    {proc_list}
                    </tbody>
                </table>

                Data Received: {cpu_data.timestamp}
            </div>;
        }

        return <div className="row">

            <div className="col-md-6">
                <div className="panel panel-default">
                    <div className="panel-heading">
                        <h3 className="panel-title">GPU</h3>
                    </div>
                    <div className="panel-body">
                        {gpu_display}
                    </div>
                </div>
            </div>

            <div className="col-md-6">
                <div className="panel panel-default">
                    <div className="panel-heading">
                        <h3 className="panel-title">CPU</h3>
                    </div>
                    <div className="panel-body">
                        {cpu_display}
                    </div>
                </div>
            </div>
        </div>;
    }
});

export default InfoPage
