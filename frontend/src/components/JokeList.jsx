// JokeList.jsx — Renders an array of jokes as a list
//
// This component receives a 'jokes' array as a prop and renders each joke
// using .map() — the React equivalent of Jinja2's {% for joke in jokes %}.
//
// WHY .map() and not a for loop:
//   JSX requires expressions (values), not statements (instructions).
//   .map() returns a new array of <li> elements — that array is the value
//   JSX renders. A for loop does not return a value.
//
// WHY key={joke.id}:
//   React needs a unique identifier for each list item so it can
//   efficiently update the DOM when the list changes. Without keys,
//   React re-renders the entire list on every change.

function JokeList({ jokes }) {
  return (
    <ul>
      {jokes.map(joke => (
        <li key={joke.id}>
          <strong>{joke.text}</strong> — {joke.author}
        </li>
      ))}
    </ul>
  );
}

export default JokeList;
