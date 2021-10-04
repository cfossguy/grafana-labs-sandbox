import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
      { duration: '120s', target: 100 },
  ],
};

export default function () {
  http.get('http://34.133.2.247/fast/50');
}
