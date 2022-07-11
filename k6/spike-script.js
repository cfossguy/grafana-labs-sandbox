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
  http.get('http://35.224.140.127/fast/50', params);
}
