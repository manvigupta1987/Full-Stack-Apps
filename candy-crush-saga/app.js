document.addEventListener("DOMContentLoaded", () => {
  const grid = document.querySelector(".grid");
  const scoreDisplay = document.getElementById('score')
  const width = 8;
  const sqaures = [];
  let score = 0;

  const candyColors = ["url(images/alternative-red.png)",
    "url(images/alternative-yellow.png)", 
    "url(images/alternative-orange.png)", 
    "url(images/alternative-purple.png)", 
    "url(images/alternative-green.png)", 
    "url(images/alternative-blue.png)"];

  //create board
  function createBoard() {
    for (let i = 0; i < width * width; i++) {
      const sqaure = document.createElement("div");
      sqaure.setAttribute("id", i);
      sqaure.setAttribute("draggable", true);
      let randomColor = Math.floor(Math.random() * candyColors.length);
      sqaure.style.backgroundImage = candyColors[randomColor];
      grid.appendChild(sqaure);
      sqaures.push(sqaure);
    }
  }

  createBoard();

  let colorBeingDragged, sqaureBeingDragged;
  let colorBeingReplaced, sqaureBeingReplaced;

  //drag the candies
  sqaures.forEach(square => square.addEventListener("dragstart", dragStart));
  sqaures.forEach(square => square.addEventListener("dragend", dragEnd));
  sqaures.forEach(square => square.addEventListener("dragover", dragOver));
  sqaures.forEach(square => square.addEventListener("dragenter", dragEnter));
  sqaures.forEach(square => square.addEventListener("dragleave", dragLeave));
  sqaures.forEach(square => square.addEventListener("drop", dragDrop));

  function dragStart() {
    colorBeingDragged = this.style.backgroundImage;
    sqaureBeingDragged = parseInt(this.id);
  }

  function dragOver(e) {
    e.preventDefault();
  }
  function dragEnter() {}
  function dragLeave() {}
  function dragDrop() {
    colorBeingReplaced = this.style.backgroundImage;
    sqaureBeingReplaced = parseInt(this.id);
    this.style.backgroundImage = colorBeingDragged;
    sqaures[sqaureBeingDragged].style.backgroundImage = colorBeingReplaced;
  }
  function dragEnd() {
    //valid move
    let validMoves = [
      sqaureBeingDragged - 1,
      sqaureBeingDragged + 1,
      sqaureBeingDragged - width,
      sqaureBeingDragged + width
    ];
    let validMove = validMoves.includes(sqaureBeingReplaced);
    if (sqaureBeingReplaced && validMove) {
      sqaureBeingReplaced = null;
    } else if (sqaureBeingReplaced && !validMove) {
      sqaures[sqaureBeingDragged].style.backgroundImage = colorBeingDragged;
      sqaures[sqaureBeingReplaced].style.backgroundImage = colorBeingReplaced;
    } else {
      sqaures[sqaureBeingDragged].style.backgroundImage = colorBeingDragged;
    }
  }

  function checkForMatches(indexArr, inx) {
    let numberOfMatches = 0;
    if(checkifValidIndex(indexArr)) {
      let decidedColor = sqaures[inx].style.backgroundImage;
      const isBlank = sqaures[inx].style.backgroundImage === "";
      if (indexArr.every(index => sqaures[index].style.backgroundImage === decidedColor && !isBlank)) {
        numberOfMatches++;
        indexArr.forEach(index => sqaures[index].style.backgroundImage = "")
      }
    }
    return numberOfMatches;
  }

  function checkifValidIndex(arr) {
    return arr.every(index => index < (width*width))
  }

  //checking for matches
  function checkRowsForThree() {
    for (let i = 0; i < 61; i++) {
      if(checkIfMoveVaild(i, 3)) {
        let rowOfThree = [i, i + 1, i + 2];
        let matches = checkForMatches(rowOfThree, i)
        score += matches*3
        scoreDisplay.innerHTML = score
      }
    }
  }

  function checkRowsForFour() { 
    for (let i = 0; i < 60; i++) {
      if(checkIfMoveVaild(i, 4)) {
        let rowOfFour = [i, i + 1, i + 2, i+3];
        let matches = checkForMatches(rowOfFour, i)
        score += matches*4
        scoreDisplay.innerHTML = score
      }
    }
  }   

  function checkIfMoveVaild(idx, rowsNum) {
    if (rowsNum === 3) {
      return ((idx+2)%8 !==0 && (idx+1) % 8 !== 0)
    } else if (rowsNum === 4) {
      return ((idx+3)%8 !==0 && (idx+2)%8 !==0 && (idx+1) % 8 !== 0)
    }
    
  }

  function checkColumnsForThree() {
    for(let i=0; i< 47; i++) {
      let columnOfThree = [i, i+width, i+(width*2)];
      let matches = checkForMatches(columnOfThree, i) 
      score += matches*3
      scoreDisplay.innerHTML = score
    }
  }

  function checkColumnsForFour() {
    for(let i=0; i< 47; i++) {
      let columnOfFour = [i, i+width, i+(width*2), i+(width*3)];
      let matches = checkForMatches(columnOfFour, i) 
      score += matches*4
      scoreDisplay.innerHTML = score
    }
  }

  function moveDown() {
    for(let i =0; i<55; i++) {
      if(sqaures[i+width].style.backgroundImage === "") {
        sqaures[i+width].style.backgroundImage = sqaures[i].style.backgroundImage
        sqaures[i].style.backgroundImage = ''
        if(i >= 0 && i<8 && sqaures[i].style.backgroundImage === '') {
          let randomColor = Math.floor(Math.random() * candyColors.length)
          sqaures[i].style.backgroundImage = candyColors[randomColor]
        }
      }
    }
  }

  setInterval(function(){
    moveDown()
    checkRowsForFour();
    checkColumnsForFour();
    checkRowsForThree();
    checkColumnsForThree();
  }, 100);
});
