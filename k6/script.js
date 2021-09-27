import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
      { duration: '60s', target: 5 },
    { duration: '60s', target: 1 },
    { duration: '60s', target: 10 },
    { duration: '60s', target: 2 },
    { duration: '60s', target: 20 },
  ],
};

export default function () {
  // 4 fast calls with small(1)/med(2) response payloads
  http.get('http://35.226.45.191/fast/1');
  http.get('http://35.226.45.191/fast/2');
  http.get('http://35.226.45.191/fast/1');
  http.get('http://35.226.45.191/fast/2');

  // 1 roulette call with large(3) response payload, will fail 1 out of 3000
  // 1 fast call with large(3) response payload
  http.get('http://35.226.45.191/roulette/3');
  http.get('http://35.226.45.191/fast/3');

  // 1 slow call with large(3) response payload, will have large(3) sleep time
  // 1 fast call with large(3) response payload
  http.get('http://35.226.45.191/slow/3');
  http.get('http://35.226.45.191/fast/3');

  // 1 round trip call with large(3) response payload
  // 1 fast call with large(3) response payload
  http.get('http://35.226.45.191/trip/3');
  http.get('http://35.226.45.191/fast/3');
}
