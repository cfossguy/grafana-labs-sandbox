import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
      { duration: '120s', target: 10 },
  ],
};

export default function () {
    let params = {
    timeout: '120s'
  };
  http.get('http://34.134.135.13/fast/50', params);
}
