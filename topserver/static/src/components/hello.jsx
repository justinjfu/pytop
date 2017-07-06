import React from 'react';
import Sidebar from './sidebar.jsx'
import InfoPage from './info_page.jsx'
import {getJSON} from '../tools/request.jsx';

var TEST_GPU_DATA = {"timestamp": "2017-07-06 00:40:22.044303", "gpu": [{"usage": 0.57, "memory_used": "11964 MiB", "name": "GPU 01", "memory_total": "12189 MiB", "model": "TITAN X (Pascal)", "temperature": 68}, {"usage": 0.0, "memory_used": "11 MiB", "name": "GPU 02", "memory_total": "12189 MiB", "model": "TITAN X (Pascal)", "temperature": 50}, {"usage": 0.52, "memory_used": "11964 MiB", "name": "GPU 03", "memory_total": "12189 MiB", "model": "TITAN X (Pascal)", "temperature": 76}, {"usage": 0.38, "memory_used": "8717 MiB", "name": "GPU 04", "memory_total": "12186 MiB", "model": "TITAN X (Pascal)", "temperature": 83}], "processes": [{"used_gpu_memory": "4239 MiB", "pid": "3238", "user": "user_a", "process_name": "python", "gpu_id": 1}, {"used_gpu_memory": "4239 MiB", "pid": "5076", "user": "user_a", "process_name": "python", "gpu_id": 1}, {"used_gpu_memory": "3475 MiB", "pid": "9861", "user": "user_a", "process_name": "python", "gpu_id": 1}, {"used_gpu_memory": "4239 MiB", "pid": "2780", "user": "user_b", "process_name": "python", "gpu_id": 3}]}
var TEST_CPU_DATA = {"timestamp": "2017-07-06 00:44:20.034940", "processes": [{"pid": 9179, "memory": 2.8, "user": "user_a", "cmd": "python", "cpu": 131.2}, {"pid": 2780, "memory": 2.8, "user": "user_a", "cmd": "python", "cpu": 125.0}, {"pid": 11895, "memory": 2.8, "user": "user_a", "cmd": "python", "cpu": 125.0}, {"pid": 27617, "memory": 2.8, "user": "user_b", "cmd": "python", "cpu": 125.0}, {"pid": 3238, "memory": 2.8, "user": "user_b", "cmd": "python", "cpu": 118.8}, {"pid": 9861, "memory": 2.7, "user": "user_b", "cmd": "python", "cpu": 118.8}]}

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

        ///*
        getJSON('../api/top/'+machine, function(cpu_data){
            this_.setState({'cpu_data': cpu_data});
        },
        function(){
            console.log('timeout');
            this_.setState({'cpu_data': 'timeout'})
        },
            function(){
                this_.setState({'cpu_data': 'error'})
            }
        );
        getJSON('../api/nvidia/'+machine, function(gpu_data){
            this_.setState({'gpu_data': gpu_data});
        }, function(){
            console.log('timeout');
            this_.setState({'gpu_data': 'timeout'})
        },function(){
            this_.setState({'cpu_data': 'error'})
        });
        //*/

        /*
        this.setState({
            'gpu_data': TEST_GPU_DATA,
            'cpu_data': TEST_CPU_DATA
        })
        */
    },
    
    render: function () {
        return <div className="container-fluid container-global">
            <div className="row">
                <div className="col-md-3 sidebar">
                <Sidebar machine_url="../api/machines" machine_callback={this.switch_machine}
                         selected_machine={this.state.info_machine}/>
                    </div>
                <div className="col-md-9 infobar" >
                    <InfoPage host_name={this.state.info_machine}
                              cpu_data={this.state.cpu_data}
                              gpu_data={this.state.gpu_data} />
                </div>
            </div>
        </div>;
    }
});

export default Main
