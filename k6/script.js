import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
    { duration: '20s', target: 20 },
    { duration: '20s', target: 40 },
    { duration: '20s', target: 80 },
  ],
};

export default function () {
  http.get('http://35.226.45.191/fast');
  http.get('http://35.226.45.191/fast');
  http.get('http://35.226.45.191/fast');
  http.get('http://35.226.45.191/roulette');
  http.get('http://35.226.45.191/roulette');
  http.get('http://35.226.45.191/roulette');
  http.get('http://35.226.45.191/slow');
  http.get('http://35.226.45.191/trip/3');
}
