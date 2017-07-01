import React from 'react';
import Sidebar from './sidebar.jsx'
import InfoPage from './info_page.jsx'
import {getJSON} from '../tools/request.jsx';

var TEST_GPU_DATA = {"timestamp": "Fri Jun 99 20:20:20 2017", "gpu": [{"memory_used": "11964 MiB", "name": "GPU 01", "memory_total": "12189 MiB", "usage": 0.44, "model": "TITAN X (Pascal)", "temperature": "66 C"}, {"memory_used": "11710 MiB", "name": "GPU 02", "memory_total": "12189 MiB", "usage": 0.56, "model": "TITAN X (Pascal)", "temperature": "84 C"}, {"memory_used": "11964 MiB", "name": "GPU 03", "memory_total": "12189 MiB", "usage": 0.46, "model": "TITAN X (Pascal)", "temperature": "81 C"}, {"memory_used": "8717 MiB", "name": "GPU 04", "memory_total": "12186 MiB", "usage": 0.28, "model": "TITAN X (Pascal)", "temperature": "80 C"}]};
var TEST_CPU_DATA = {"timestamp": "20:20:20", "processes": [{"cmd": "python", "pid": 31299, "user": "user_a", "cpu": 100.0}, {"cmd": "python", "pid": 31213, "user": "user_b", "cpu": 81.2}]};

var Main = React.createClass({

    getInitialState: function(){
        return {
            'info_machine': null,
            'cpu_data': null,
            'gpu_data': null,
        }
    },

    switch_machine: function(machine){
        var this_ = this;
        console.log('Clicking:', machine);

        this.setState({'info_machine': machine,
                        'cpu_data': null, 'gpu_data': null});

        getJSON('../api/top/'+machine, function(cpu_data){
            this_.setState({'cpu_data': cpu_data});
        });
        getJSON('../api/nvidia/'+machine, function(gpu_data){
            this_.setState({'gpu_data': gpu_data});
        });

        //this.setState({
        //    'gpu_data': TEST_GPU_DATA,
        //    'cpu_data': TEST_CPU_DATA
        //})
    },
    
    render: function () {
        return <div className="container-fluid container-global">
            <div className="row">
                <div className="col-md-3 sidebar">
                <Sidebar machine_url="../api/machines" machine_callback={this.switch_machine}/>
                    </div>
                <div className="col-md-9 infobar" >
                    <InfoPage host_name={this.state.info_machine} cpu_data={this.state.cpu_data} gpu_data={this.state.gpu_data} />
                </div>
            </div>
        </div>;
    }
});

export default Main
