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
  http.get('http://35.224.140.127/fast/10');
  http.get('http://35.224.140.127/fast/20');
  http.get('http://35.224.140.127/fast/10');
  http.get('http://35.224.140.127/fast/20');

  http.get('http://35.224.140.127/fast/10');
  http.get('http://35.224.140.127/fast/10');
  http.get('http://35.224.140.127/fast/10');
  http.get('http://35.224.140.127/fast/10');
  http.get('http://35.224.140.127/fast/10');
  http.get('http://35.224.140.127/fast/10');

  // 3 roulette calls will fail 1 out of 10
  http.get('http://35.224.140.127/roulette/10');
  http.get('http://35.224.140.127/roulette/10');
  http.get('http://35.224.140.127/roulette/10');
  http.get('http://35.224.140.127/roulette/10');
  http.get('http://35.224.140.127/roulette/10');

  // 3 roulette calls will fail 1 out of 1000
  http.get('http://35.224.140.127/roulette/1000');
  http.get('http://35.224.140.127/roulette/1000');
  http.get('http://35.224.140.127/roulette/1000');

  // 2 slow calls with 2 second sleep times and 50kb response payloads
  http.get('http://35.224.140.127/slow/2/50');
  http.get('http://35.224.140.127/slow/2/50');

  // 1 round trip call with 3 second sleep time
  http.get('http://35.224.140.127/trip/3/1/10');
  http.get('http://35.224.140.127/slow/3/20');

  // 2 round trip call with 3 second sleep time
  http.get('http://35.224.140.127/trip/5/2/20');
}
