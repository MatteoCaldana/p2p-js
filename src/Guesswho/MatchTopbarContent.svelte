<script>
  import { images } from "../lib/images.js";

  export let selectedCharacter;
  export let otherPlayerCharacter;
  export let myTurn;
  export let opponentTurn;
  export let activeImageIndex;
  export let questions;
  export let possibleGuesses;
  export let gameStatus;
  export let messagesData;
  export let peer;

  let selected = `${questions[0].key}:${questions[0].value}`;

  const addMessage = (message) => {
    messagesData = [
      ...messagesData,
      {
        id: peer.id,
        type: "action",
        subType: "guesswho",
        turn: myTurn,
        timestamp: new Date().getTime(),
        ...message,
      },
    ];
  };

  const handleGuess = (e) => {
    myTurn += 1;
    console.log("Guessing character:", e.target.id);
    const guess = parseInt(e.target.id);
    if (guess === otherPlayerCharacter) {
      console.log("You won!");
      gameStatus = "won";
      addMessage({
        action: "won",
      });
    } else {
      console.log("Next try!");
      possibleGuesses = possibleGuesses.filter((i) => i !== guess);
      addMessage({
        action: "guess",
        value: guess,
        result: "incorrect",
      });
    }
  };
  const handleQuestion = (_) => {
    myTurn += 1;
    console.log("Asking question:", selected);
    const [key, value] = selected.split(":");
    let result;
    if (images[otherPlayerCharacter][key] === value) {
      console.log("Correct!");
      possibleGuesses = possibleGuesses.filter((i) => images[i][key] === value);
      result = "correct";
    } else {
      console.log("Incorrect!");
      possibleGuesses = possibleGuesses.filter((i) => images[i][key] !== value);
      result = "incorrect";
    }
    addMessage({
      action: "question",
      value: value,
      key: key,
      result: result,
    });
  };
</script>

<div>
  <p>
    Current turn: {myTurn}. Possible choices: {possibleGuesses.length}.
  </p>
  <p>
    Opponent must guess: {images[selectedCharacter].name}.
  </p>
  {#if myTurn <= opponentTurn}
    <form action="" onsubmit="return false">
      <label for="cars">Ask a question:</label>
      <select name="questions" id="questions" bind:value={selected}>
        {#each questions as question}
          <option value={`${question.key}:${question.value}`}
            >{question.text}</option
          >
        {/each}
      </select>
      <input
        style="padding:5px;font-size:12pt;max-width:150px"
        type="submit"
        value="Ask!"
        on:click={(e) => handleQuestion(e)}
      />
    </form>
    <div>
      Or make a guess!
      <button
        id={activeImageIndex}
        style="padding:5px"
        disabled={activeImageIndex === null}
        on:click={(e) => handleGuess(e)}
      >
        Guess {activeImageIndex
          ? images[activeImageIndex].name
          : "your character"}
      </button>
    </div>
  {:else}
    <p>Waiting for your opponent to make a move...</p>
  {/if}
</div>
