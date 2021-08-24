import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  http.get('http://35.226.45.191/slow/');
  http.get('http://35.226.45.191/fast/');
  sleep(1);
}
