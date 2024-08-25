<script>
  import { images } from "../lib/images.js";
  import MatchTopbarContent from "./MatchTopbarContent.svelte";

  export let messagesData;
  export let peer;

  // aesthetics
  let primaryColor = "#e4d5b7";
  let primaryColorDark = "#c0891c";
  let columns = 4;
  let activeImageIndex = null;

  // Calculate the number of columns based on screen width
  const updateColumns = () => {
    const width = window.innerWidth;
    if (width >= 1200) {
      columns = 6;
    } else if (width >= 992) {
      columns = 5;
    } else if (width >= 768) {
      columns = 4;
    } else if (width >= 576) {
      columns = 3;
    } else {
      columns = 2;
    }
  };

  // game state
  let selectedCharacter = null;
  let otherPlayerCharacter = null;
  let gameStatus = "picking";
  let possibleGuesses = [...Array(images.length).keys()];
  let myTurn = 1;
  let opponentTurn = 1;

  const resetState = () => {
    selectedCharacter = null;
    otherPlayerCharacter = null;
    gameStatus = "picking";
    possibleGuesses = [...Array(images.length).keys()];
    myTurn = 1;
    opponentTurn = 1;
  };

  const handleClick = (index) => {
    activeImageIndex = index === activeImageIndex ? null : index;
  };

  const handleConfirm = () => {
    if (activeImageIndex !== null) {
      console.log("Confirmed character:", activeImageIndex);
      selectedCharacter = activeImageIndex;
      activeImageIndex = null;
      messagesData = [
        ...messagesData,
        {
          id: peer.id,
          type: "action",
          subType: "guesswho",
          timestamp: new Date().getTime(),
          action: "pick",
          value: selectedCharacter,
        },
      ];
    } else {
      console.log(
        "Error: should never be able to confirm character without any selection."
      );
    }
  };

  const parseMessage = (message) => {
    if (
      message.id !== peer.id &&
      message.type === "action" &&
      message.subType === "guesswho"
    ) {
      if (message.action === "pick") {
        otherPlayerCharacter = parseInt(message.value);
        if (selectedCharacter !== null) {
          console.log("Force start game");
          // TODO: if I reorder the reactive updates, it this necessary?
          gameStatus = "playing";
          primaryColor = "#61cfed";
          primaryColorDark = "#0b9fde";
        }
      } else if (message.action === "guess" || message.action === "question") {
        opponentTurn = parseInt(message.turn);
      } else if (message.action === "won") {
        gameStatus = "lost";
      }
    }
  };

  // Update columns on load and resize
  updateColumns();
  window.addEventListener("resize", updateColumns);

  $: messagesData.length && parseMessage(messagesData[messagesData.length - 1]);

  $: if (selectedCharacter !== null && otherPlayerCharacter !== null) {
    console.log("Game started!");
    gameStatus = "playing";
  }
  $: if (gameStatus === "playing") {
    console.log("Should be changing colors");
    primaryColor = "#61cfed";
    primaryColorDark = "#0b9fde";
  } else {
    primaryColor = "#e4d5b7";
    primaryColorDark = "#c0891c";
  }
</script>

<div>
  <div class="topbar" style="--primary-color: {primaryColor}">
    <h1>Guess Who?</h1>
    {#if gameStatus === "won"}
      <div>
        <h2 style="margin-left:10px;margin-right:10px">
          You won! Congratulations!
        </h2>
        <button on:click={resetState}>Play again</button>
      </div>
    {:else if gameStatus === "lost"}
      <div>
        <h2 style="margin-left:10px;margin-right:10px">
          You lost! Better luck next time!
        </h2>
        <button on:click={resetState}>Play again</button>
      </div>
    {:else if selectedCharacter === null}
      <button disabled={activeImageIndex === null} on:click={handleConfirm}>
        <h4 style="margin-left:10px;margin-right:10px">
          Pick {activeImageIndex
            ? images[activeImageIndex].name
            : "your character"}
        </h4>
      </button>
    {:else if otherPlayerCharacter === null}
      <h4 style="margin-left:10px;margin-right:10px">
        Waiting for the other player to pick their character...
      </h4>
    {:else}
      <h4 style="margin-left:10px;margin-right:10px">
        <MatchTopbarContent
          bind:selectedCharacter
          bind:otherPlayerCharacter
          bind:myTurn
          bind:opponentTurn
          bind:activeImageIndex
          bind:possibleGuesses
          bind:gameStatus
          bind:messagesData
          bind:peer
        />
      </h4>
    {/if}
  </div>

  <div class="grid" style="--columns: {columns}">
    {#each images as image, index}
      {#if gameStatus === "picking" || (gameStatus === "playing" && possibleGuesses.includes(index))}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <div
          class="image-wrapper {index === activeImageIndex ? 'active' : ''}"
          style="--primary-color-dark: {primaryColorDark}"
          on:click={() => handleClick(index)}
        >
          <img src={image.img} alt={image.img} />
          <div class="overlay">{image.name}</div>
        </div>
      {/if}
    {/each}
  </div>
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(var(--columns), 1fr);
    gap: 10px;
    margin: 0 auto;
    padding: 10px;
    max-width: 1200px;
  }

  .topbar {
    position: sticky;
    top: 0;
    width: 100%;
    background-color: var(--primary-color);
    color: black;
    text-align: center;
    padding: 15px;
    z-index: 100; /* Ensure the top bar is above other content */
  }

  .image-wrapper {
    position: relative;
    width: 100%;
    padding-top: 120%; /* Aspect ratio of 4:5 */
    overflow: hidden;
    background: #f0f0f0;
    cursor: pointer;
    transition: border 0.3s;
  }

  .image-wrapper img {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transform: translate(-50%, -50%);
    filter: grayscale(100%);
    transition:
      filter 0.3s,
      border 0.3s;
  }

  .image-wrapper.active img {
    filter: grayscale(0%);
  }

  .image-wrapper .overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding-top: 10px;
    padding-bottom: 10px;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    text-align: center;
    font-size: 16px;
  }

  .image-wrapper.active {
    box-shadow: 0 0 15px var(--primary-color-dark);
  }

  button {
    border: 2px solid;
    border-radius: 10px;
    background-color: #f3ebdd;
    cursor: pointer;
  }

  button:disabled {
    cursor: not-allowed;
  }

  button:hover:enabled {
    background-color: #e0d7c9;
  }

  button:active {
    background-color: #e0d7c9;
  }
</style>
