import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  http.get('http://34.136.36.166/hello-world/');
  http.get('http://34.136.36.166/hello-world/');
  http.get('http://34.136.36.166/hello-world/');
  http.get('http://34.136.36.166/badurl/');
  sleep(1);
}

