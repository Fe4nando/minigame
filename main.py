import streamlit as st
import streamlit.components.v1 as components

PASSWORD = "milo"

st.set_page_config(page_title="Milo & Frosty Game", layout="centered")
st.title("🐾 Milo & Frosty Apology Game")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter Password:", type="password")
    if st.button("Submit"):
        if password.strip().lower() == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password! Try again.")
else:
    st.markdown("### ❤️ I'm sorry for being a bitch. I love you. Please don't be mad. ❤️")
    st.markdown("👇 Choose your pet and play the game!")

    game_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.2/p5.min.js"></script>
      <style>
        html, body {
          margin: 0;
          padding: 0;
          background: #0E1117;
          height: 100%;
          width: 100%;
          overflow: hidden;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: start;
        }
        canvas {
          border-radius: 20px;
          box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.6);
          margin-top: 10px;
        }
        .top-buttons {
          margin-top: 10px;
        }
        .button-style {
          font-size: 18px;
          padding: 10px 20px;
          margin: 0 10px;
          background-color: #1f77b4;
          color: white;
          border: none;
          border-radius: 10px;
          cursor: pointer;
          transition: 0.3s ease;
        }
        .button-style:hover {
          background-color: #135b91;
        }
      </style>
    </head>
    <body>
    <div class="top-buttons">
      <button class="button-style" onclick="selectPet('dog')">🐶 Milo</button>
      <button class="button-style" onclick="selectPet('cat')">🐱 Frosty</button>
    </div>
    <script>
      let player;
      let foods = [], foreigns = [];
      let score = 0, totalObjects = 0;
      let pet = null, petLabel = '';
      let gameStarted = false;
      let movingLeft = false, movingRight = false;

      let dogImg, catImg, cookieImg, tunaImg, poisonImg;

      function preload() {
        dogImg = loadImage("https://raw.githubusercontent.com/Fe4nando/minigame/main/dog.png");
        catImg = loadImage("https://raw.githubusercontent.com/Fe4nando/minigame/main/cat.png");
        cookieImg = loadImage("https://raw.githubusercontent.com/Fe4nando/minigame/main/chicken.png");
        tunaImg = loadImage("https://raw.githubusercontent.com/Fe4nando/minigame/main/tuna.png");
        poisonImg = loadImage("https://raw.githubusercontent.com/Fe4nando/minigame/main/posion.png");
      }

      function setup() {
        let canvas = createCanvas(windowWidth * 0.98, windowHeight * 0.85);
        canvas.parent(document.body);
        textAlign(CENTER, CENTER);
        textSize(20);
        player = new Player();
      }

      function selectPet(selected) {
        pet = selected;
        petLabel = selected === 'dog' ? 'Milo' : 'Frosty';
        resetGame();
      }

      function resetGame() {
        score = 0;
        totalObjects = 0;
        foods = [];
        foreigns = [];
        gameStarted = true;
        player = new Player();
      }

      function draw() {
        background("#1A1C23");

        if (!gameStarted) {
          fill(255);
          textSize(24);
          text("Choose Milo 🐶 or Frosty 🐱 to start the game", width/2, height/2);
          return;
        }

        if (movingLeft) player.move(-1);
        if (movingRight) player.move(1);

        player.show();

        if (frameCount % 60 === 0) {
          foods.push(new Food());
          totalObjects++;
        }

        if (totalObjects >= 15 && frameCount % 120 === 0) {
          foreigns.push(new Foreign());
        }

        for (let i = foods.length - 1; i >= 0; i--) {
          foods[i].move();
          foods[i].show();

          if (foods[i].offscreen()) {
            foods.splice(i, 1);
          } else if (foods[i].hits(player)) {
            score++;
            foods.splice(i, 1);
          }
        }

        for (let i = foreigns.length - 1; i >= 0; i--) {
          foreigns[i].move();
          foreigns[i].show();

          if (foreigns[i].offscreen()) {
            foreigns.splice(i, 1);
          } else if (foreigns[i].hits(player)) {
            score = max(0, score - 5);
            foreigns.splice(i, 1);
          }
        }

        fill(255);
        textSize(20);
        text("Score: " + score, 100, 20);
      }

      function keyPressed() {
        if (keyCode === LEFT_ARROW || key === 'A' || key === 'a') movingLeft = true;
        if (keyCode === RIGHT_ARROW || key === 'D' || key === 'd') movingRight = true;
      }

      function keyReleased() {
        if (keyCode === LEFT_ARROW || key === 'A' || key === 'a') movingLeft = false;
        if (keyCode === RIGHT_ARROW || key === 'D' || key === 'd') movingRight = false;
      }

      class Player {
        constructor() {
          this.x = width / 2;
          this.size = 70;
        }

        move(dir) {
          this.x += dir * 10;
          this.x = constrain(this.x, 0, width - this.size);
        }

        show() {
          let img = pet === 'dog' ? dogImg : catImg;
          image(img, this.x, height - this.size - 10, this.size, this.size);
        }
      }

      class Food {
        constructor() {
          this.x = random(0, width - 30);
          this.y = 0;
          this.size = 40;
          this.speed = 2.0;
        }

        move() {
          this.y += this.speed;
        }

        show() {
          let img = pet === 'dog' ? cookieImg : tunaImg;
          image(img, this.x, this.y, this.size, this.size);
        }

        offscreen() {
          return this.y > height;
        }

        hits(player) {
          return this.x < player.x + player.size &&
                 this.x + this.size > player.x &&
                 this.y < height - 10 &&
                 this.y + this.size > height - player.size - 10;
        }
      }

      class Foreign {
        constructor() {
          this.x = random(0, width - 30);
          this.y = 0;
          this.size = 40;
          this.speed = totalObjects >= 30 ? 3.5 : 2.2;
        }

        move() {
          this.y += this.speed;
        }

        show() {
          image(poisonImg, this.x, this.y, this.size, this.size);
        }

        offscreen() {
          return this.y > height;
        }

        hits(player) {
          return this.x < player.x + player.size &&
                 this.x + this.size > player.x &&
                 this.y < height - 10 &&
                 this.y + this.size > height - player.size - 10;
        }
      }
    </script>
    </body>
    </html>
    """

    components.html(game_html, height=700)
