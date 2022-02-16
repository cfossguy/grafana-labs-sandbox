import express from 'express';
var app = express();

import { collectDefaultMetrics, register } from 'prom-client';
collectDefaultMetrics();

app.get('/slow', async function (req, res) {
    await new Promise(resolve => setTimeout(resolve, 3000));
    res.send('Slow API!!!');
})

app.get('/fast', async function (req, res) {
    await new Promise(resolve => setTimeout(resolve, 300));
    res.send('Fast API');
})

app.get('/shutdown', function (req, res) {
    console.log("Exiting NodeJS server");
    process.exit();
})

app.get('/metrics', async (_req, res) => {
  try {
      res.set('Content-Type', register.contentType);
      res.end(await register.metrics());
  } catch (err) {
    res.status(500).end(err);
  }
});

var server = app.listen(4001, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("Example app listening at http://%s:%s", host, port)
})

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}