import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
      { duration: '120s', target: 100 },
  ],
};

export default function () {
    let params = {
    timeout: '120s'
  };
  http.get('http://34.134.135.13/slow/2000/20', params);
}
