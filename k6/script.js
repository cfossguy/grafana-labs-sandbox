import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
    { duration: '20s', target: 10 },
    { duration: '20s', target: 30 },
    { duration: '20s', target: 50 },
  ],
};

export default function () {
  http.get('http://35.226.45.191/fast');
  http.get('http://35.226.45.191/fast');
  http.get('http://35.226.45.191/fast');
  http.get('http://35.226.45.191/fast');
  http.get('http://35.226.45.191/roulette/300');
  http.get('http://35.226.45.191/slow');
  http.get('http://35.226.45.191/trip/3');
}
