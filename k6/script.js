import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
      { duration: '10s', target: 1 },
    { duration: '20s', target: 2 },
    { duration: '30s', target: 3 },
    { duration: '50s', target: 5 },
    { duration: '80s', target: 8 },
    { duration: '130s', target: 13 },
  ],
};

export default function () {
  // 4 fast calls with small(1)/med(2) response payloads
  http.get('http://35.226.45.191/fast/1');
  http.get('http://35.226.45.191/fast/2');
  http.get('http://35.226.45.191/fast/1');
  http.get('http://35.226.45.191/fast/2');

  // 3 roulette calls will fail 1 out of 5000
  http.get('http://35.226.45.191/roulette/5000');
  http.get('http://35.226.45.191/roulette/5000');
  http.get('http://35.226.45.191/roulette/5000');

  // 2 slow calls with 2 second sleep times
  http.get('http://35.226.45.191/slow/2');
  http.get('http://35.226.45.191/slow/2');

  // 1 round trip call with 3 second sleep time
  http.get('http://35.226.45.191/trip/3');
}
