import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
      { duration: '10s', target: 1 },
  ],
};

export default function () {
  // 3 errors
  http.get('http://35.226.45.191/roulette/1');
  http.get('http://35.226.45.191/fast/!!!');
}
