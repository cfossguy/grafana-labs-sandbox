import http from 'k6/http';

export let options = {
  stages: [
      { duration: '60s', target: 10 },
    { duration: '60s', target: 2 },
    { duration: '60s', target: 20 },
    { duration: '60s', target: 25 },
    { duration: '60s', target: 30 },
    { duration: '60s', target: 50 },
  ],
};

export default function () {
  // 4 fast calls with 10kb and 20kb response payloads
  http.get('http://34.134.135.13/fast/10');
  http.get('http://34.134.135.13/fast/20');
  http.get('http://34.134.135.13/fast/10');
  http.get('http://34.134.135.13/fast/20');

  // 3 roulette calls will fail 1 out of 10
  http.get('http://34.134.135.13/roulette/10');
  http.get('http://34.134.135.13/roulette/10');
  http.get('http://34.134.135.13/roulette/10');

  // 2 slow calls with 2 second sleep times and 50kb response payloads
  http.get('http://34.134.135.13/slow/3000/50');
  http.get('http://34.134.135.13/slow/3000/50');

  // 2 round trip call with 3 second sleep time
  http.get('http://34.134.135.13/trip/2000/2/50');
}
