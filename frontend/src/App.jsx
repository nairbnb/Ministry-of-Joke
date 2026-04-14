// App.jsx — MoJ root component
//
// This is the entry point for the React frontend.
// It owns the joke data and passes it down to child components via props.
//
// TODAY: The jokes array is hardcoded below. This is intentional.
//   Learning React's component model is enough for one session.
//
// NEXT WEEK: fetch() will replace this hardcoded array with real data
//   from the Flask API. The components below will not change —
//   only the data source will. That is Separation of Concerns:
//   the display components do not know (or care) where the data comes from.

import { useState } from 'react';
import JokeList from './components/JokeList';
import JokeCount from './components/JokeCount';

// Hardcoded joke data — stands in for the Flask API until ICEX 11
const JOKES = [
  { id: 1, text: "Why did the chicken cross the road?", author: "alice" },
  { id: 2, text: "A priest and a rabbi walk into a bar...", author: "bob" },
  { id: 3, text: "Why do programmers prefer dark mode?", author: "carol" },
];

function App() {
  // useState(true) — jokes are visible by default
  // setShowJokes toggles visibility when the button is clicked
  const [showJokes, setShowJokes] = useState(true);

  return (
    <div>
      <h1>Ministry of Jokes</h1>

      {/* Count is derived from the array length — not a separate variable */}
      <JokeCount count={JOKES.length} />

      {/* Button toggles showJokes between true and false */}
      <button onClick={() => setShowJokes(!showJokes)}>
        {showJokes ? "Hide Jokes" : "Show Jokes"}
      </button>

      {/* Conditional rendering: show JokeList only when showJokes is true */}
      {showJokes && <JokeList jokes={JOKES} />}
    </div>
  );
}

export default App;
