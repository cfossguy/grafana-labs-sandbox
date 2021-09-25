import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '30s', target: 20 },
    { duration: '30s', target: 30 },
  ],
};

export default function () {
  http.get('http://35.226.45.191/fast/1');
  http.get('http://35.226.45.191/fast/2');
  http.get('http://35.226.45.191/fast/3');

  http.get('http://35.226.45.191/roulette/300');
  http.get('http://35.226.45.191/slow/3');
  http.get('http://35.226.45.191/trip/3');
}
