
const fs =require('fs')
const express = require('express')
var cors = require('cors')
const {spawn} = require('child_process');
const app = express()
app.use(cors())
const port = 3040

const pyScriptFile='global-select-admin-centroids.py'


// serving the static files
app.use('/resources', express.static('docs'))

// Add headers
app.use(function (req, res, next) {
    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', 'https://map.globalassembly.org');
    // Pass to next layer of middleware
    next();
});

// Endpoint to run the script normaly
app.get('/run', (req, res) => {
    var dataSet = [];
    // spawn new child process to call the python script
    //  const python = spawn('python3', ['gaa.py']);
    const python = spawn('python3', [pyScriptFile]);
    python.stdout.on('data', function (data) {
        dataSet.push(data);
    });
    // in close event we are sure that stream is from child process is closed
    python.on('close', (code) => {
        //  console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataSet.join(""))
    });
})

// request to run the script by also passing the number to be selected from
app.get('/request', (req, res) => {
    var dataSet = [];
     // spawn new child process to call the python script
    //  const python = spawn('python3', ['gaa.py']);
    const python = spawn('python3', [pyScriptFile,req.query.payload]);
    python.stdout.on('data', function (data) {
        dataSet.push(data);
    });
     // in close event we are sure that stream is from child process is closed
    python.on('close', (code) => {
    //  console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataSet.join(""))
    });   
})

// Endpoint to read the locations of the selected people from .txt file
app.get('/read', (req, res) => {
    fs.readFile('/home/developer/projects/global-select-app/results.txt','utf8',(err,data)=>{
        var nameArr = data.split('___');
        var new_array=[]
        for (let i = 0; i < nameArr.length-1; i++) {
            const element = nameArr[i];
            var el = element.split(",");
            new_array.push({lat:el[0],long:el[1],address:el[2],country:el[3]})    
        }
        res.send(new_array)
   })
})

//Reading  from the previous .csv file
app.get('/read-extended', (req, res) => {
    fs.readFile('/home/developer/projects/ga-people-api/docs/gobal-ca-people-points.csv','utf8',(err,data)=>{
        var resp= data.split('region_name, region_max, region_count')
        res.send(resp)
    })    
})

app.listen(port, () => console.log(`Listening on port ${port}!`))
