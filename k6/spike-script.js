import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
      { duration: '120s', target: 100 },
  ],
};

export default function () {
  http.get('http://35.226.45.191/fast/50');
}
