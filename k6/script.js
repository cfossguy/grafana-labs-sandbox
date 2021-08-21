import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  http.get('http://localhost:8082/slow/');
  http.get('http://localhost:8082/fast/');
  sleep(1);
}
