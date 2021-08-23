import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  http.get('http://34.133.181.168/slow/');
  http.get('http://34.133.181.168/fast/');
  sleep(1);
}
