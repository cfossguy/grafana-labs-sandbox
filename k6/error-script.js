import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
      { duration: '10s', target: 1 },
  ],
};

export default function () {
  http.get('http://34.134.135.13/roulette/10')
}
