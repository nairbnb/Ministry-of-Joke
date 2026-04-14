// JokeCount.jsx — Displays the total number of jokes
//
// This component receives 'count' as a prop and renders it.
// It has no state of its own — it is a pure display component.
//
// NEXT WEEK: This hardcoded count will be replaced by a fetch() call
// to GET /api/v1/jokes/count — the endpoint you built in ICEX 9.
// The component will not change. Only the data source will.

function JokeCount({ count }) {
  return (
    <p>Jokes on file: {count}</p>
  );
}

export default JokeCount;
