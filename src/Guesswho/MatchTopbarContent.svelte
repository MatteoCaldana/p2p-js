<script>
  import { images } from "../lib/images.js";

  export let selectedCharacter;
  export let otherPlayerCharacter;
  export let myTurn;
  export let opponentTurn;
  export let activeImageIndex;
  export let possibleGuesses;
  export let gameStatus;
  export let messagesData;
  export let peer;

  const guessCategories = Object.keys(images[0])
    .filter((k) => k != "img")
    .filter((k) => k != "name");

  const computeQuestions = (possibleIndexes) => {
    console.log("Computing questions for", possibleIndexes);
    let questionMap = guessCategories.reduce((acc, key) => {
      acc[key] = new Set();
      return acc;
    }, {});
    console.log("Question map:", questionMap);
    let j = 0;
    for (let i = 0; i < images.length; i++) {
      if (possibleIndexes[j] === i) {
        guessCategories.forEach((key) => questionMap[key].add(images[i][key]));
        j++;
      }
    }
    console.log("Question map:", questionMap);

    let qs = [];
    for (let key in questionMap) {
      if (questionMap[key].size === 1) {
        continue;
      }
      for (let value of questionMap[key]) {
        qs.push({
          text: `Is the ${key} of X: ${value}?`,
          key: key,
          value: value,
        });
      }
    }
    return qs;
  };

  let questions = computeQuestions(possibleGuesses);
  let selectedQuestion = `${questions[0].key}:${questions[0].value}`;

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
    activeImageIndex = null;
  };

  const handleQuestion = (_) => {
    myTurn += 1;
    console.log("Asking question:", selectedQuestion);
    const [key, value] = selectedQuestion.split(":");
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
    questions = computeQuestions(possibleGuesses);
    selectedQuestion = `${questions[0].key}:${questions[0].value}`;
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
      <select name="questions" id="questions" bind:value={selectedQuestion}>
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
