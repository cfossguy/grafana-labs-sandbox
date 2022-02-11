import http from 'k6/http';

export let options = {
  stages: [
      { duration: '24h', target: 1 }
  ],
};

export default function () {
  http.get('http://localhost:8080/log-demo-1.0-SNAPSHOT/');
}
