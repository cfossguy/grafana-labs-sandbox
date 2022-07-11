import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
      { duration: '10s', target: 1 },
  ],
};

export default function () {
  http.get('http://35.224.140.127/roulette/10')
}
