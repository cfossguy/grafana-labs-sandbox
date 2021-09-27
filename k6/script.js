import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
      { duration: '20s', target: 5 },
    { duration: '20s', target: 1 },
    { duration: '20s', target: 10 },
    { duration: '30s', target: 2 },
    { duration: '30s', target: 20 },
  ],
};

export default function () {
  // 4 fast calls with small(1)/med(2) response payloads
  http.get('http://35.226.45.191/fast/1');
  http.get('http://35.226.45.191/fast/2');
  http.get('http://35.226.45.191/fast/1');
  http.get('http://35.226.45.191/fast/2');

  // 1 roulette call with large(3) response payload, will fail 1 out of 3000
  // 1 roulette call with ex-large(10) response payload, will fail 1 out of 10000
  http.get('http://35.226.45.191/roulette/3');
  http.get('http://35.226.45.191/roulette/10');

  // 1 slow call with medium(2) response payload, will have medium(2) sleep time
  // 1 slow call with small(1) response payload, will have small(1) sleep time
  http.get('http://35.226.45.191/slow/2');
  http.get('http://35.226.45.191/slow/1');

  // 1 round trip call with large(3) response payload
  http.get('http://35.226.45.191/trip/3');
}
