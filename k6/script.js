import http from 'k6/http';

export let options = {
  stages: [
      { duration: '10s', target: 1 },
    { duration: '20s', target: 2 },
    { duration: '30s', target: 3 },
    { duration: '50s', target: 5 },
    { duration: '80s', target: 8 },
    { duration: '130s', target: 13 },
  ],
};

export default function () {
  // 4 fast calls with 10kb and 20kb response payloads
  http.get('http://34.134.135.13/fast/10');
  http.get('http://34.134.135.13/fast/20');
  http.get('http://34.134.135.13/fast/10');
  http.get('http://34.134.135.13/fast/20');

  // 3 roulette calls will fail 1 out of 1000
  http.get('http://34.134.135.13/roulette/1000');
  http.get('http://34.134.135.13/roulette/1000');
  http.get('http://34.134.135.13/roulette/1000');

  // 2 slow calls with 2 second sleep times and 50kb response payloads
  http.get('http://34.134.135.13/slow/2/50');
  http.get('http://34.134.135.13/slow/2/50');

  // 1 round trip call with 3 second sleep time
  http.get('http://34.134.135.13/trip/3/1/10');
}
