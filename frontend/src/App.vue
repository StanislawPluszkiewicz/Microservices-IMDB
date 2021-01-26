<template>
  <div id="app">
    <div id="header">
      <b-container>
      <b-row>
        <b-col cols="2">LOGO</b-col>
        <b-col >
          <b-input-group>
            <b-form-input class="nav-search" placeholder="Search"></b-form-input>
            <b-button class="btn-search" variant="info"><v-icon name="search"/></b-button>
          </b-input-group>
        </b-col>
        <b-col cols="2">
          <b-dropdown text="Profile">
            <b-dropdown-item>Sign in</b-dropdown-item>
            <b-dropdown-item><b>Sign Up</b></b-dropdown-item>
          </b-dropdown>
        </b-col>
      </b-row>
      </b-container>
    </div>
    <div id="body">
      <b-container>
      <b-row>
        Movies List
      </b-row>
      <b-row class="card-list">
        <b-card-group deck>
          <b-col v-for="movie in movies_titles" :key='movie.id' cols="3">
            <b-card
              :title="movie.title"
              :img-src="movie.image"
              :img-alt="movie.title"
              img-height="120"
              img-top
              class="mb-2 card1">
              <b-card-text>
                {{TruncateDescription(movie.description)}}
              </b-card-text>
              <template #footer>
                <b-button href="#" variant="primary">See more</b-button>
              </template>
            </b-card>
          </b-col>
        </b-card-group>
      </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
export default {
  name: "app",
  data() {
      return { 
        movies_titles: [
        {
          id: 1,
          title: 'Doctor Who',
          image: 'https://upload.wikimedia.org/wikipedia/en/0/05/Doctor_Who_-_Current_Titlecard.png',
          description: 'The further adventures in time and space of the alien adventurer known as the Doctor and their companions from planet Earth.'
        },
        {
          id: 2,
          title: 'The Walking Dead',
          image: 'https://upload.wikimedia.org/wikipedia/commons/e/ef/The_Walking_Dead_2010_logo.svg',
          description: 'Sheriff Deputy Rick Grimes wakes up from a coma to learn the world is in ruins and must lead a group of survivors to stay alive.'
        },
        {
          id: 3,
          title: 'Lupin',
          image: 'https://upload.wikimedia.org/wikipedia/fr/5/52/Logo_Lupin-Dans-l%27ombre-d%27Ars%C3%A8ne.jpg',
          description: 'Inspired by the adventures of Arsène Lupin, gentleman thief Assane Diop sets out to avenge his father for an injustice inflicted by a wealthy family.'
        },
        {
          id: 4,
          title: 'Orphan Black',
          image: 'https://help.redbubble.com/hc/article_attachments/360002359006/Orphan-Black_logo.png',
          description: 'A streetwise hustler is pulled into a compelling conspiracy after witnessing the suicide of a girl who looks just like her.'
        },
        {
          id: 5,
          title: 'The Queen\'s Gambit',
          image: 'https://degustationslitteraires.files.wordpress.com/2020/11/the-queens-gambit-review-netflix-tv-series.jpg',
          description: 'Orphaned at the tender age of nine, prodigious introvert Beth Harmon discovers and masters the game of chess in 1960s USA. But child stardom comes at a price.'
        },
        {
          id: 6,
          title: 'Modern Family',
          image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Modern_Family-Logo.svg/233px-Modern_Family-Logo.svg.png',
          description: 'Three different but related families face trials and tribulations in their own uniquely comedic ways.'
        },
        {
          id: 7,
          title: 'Bojack Horseman',
          image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/BoJack_Horseman_Logo.svg/1280px-BoJack_Horseman_Logo.svg.png',
          description: 'BoJack Horseman was the star of the hit television show "Horsin\' Around" in the \'80s and \'90s, now he\'s washed up, living in Hollywood, complaining about everything, and wearing colorful sweaters.'
        },
        {
          id: 8,
          title: 'South Park',
          image: 'https://fr.timecity.eu/_clientfiles/brands/south_park_logo.jpg',
          description: 'Follows the misadventures of four irreverent grade-schoolers in the quiet, dysfunctional town of South Park, Colorado.'
        },
        {
          id: 9,
          title: 'Breaking Bad',
          image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Breaking_Bad_logo.svg/1024px-Breaking_Bad_logo.svg.png',
          description: 'A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine in order to secure his family\'s future.'
        },
        {
          id: 10,
          title: 'How I Met Your Mother',
          image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/HowIMetYourMother.svg/1200px-HowIMetYourMother.svg.png',
          description: 'A father recounts to his children - through a series of flashbacks - the journey he and his four best friends took leading up to him meeting their mother.'
        }]
      }
  },
  methods: {
      CreateListCard: function () {

      },
      TruncateDescription: function (description) {
        
          var limit = 100
          var returnValue = description
          if (description.length > limit)
          {
            returnValue = description.slice(0, limit) + '...'
          }
          return returnValue
      }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #d6d7d2;
  min-height: 100%;
}

body{
  min-height: 100%;
}

#header {
  color: #ffffff;
  background-color: #17a2b8;
  padding-top: 15px;
  padding-bottom: 15px;
}

#body {
  color: #000000;
  padding-top: 100px;
  padding-bottom: 15px;
  min-height: 100%;
}

.nav-search {
  border: #ffffff;
  max-width: 700px;
}

.btn-search {
  color: #17a2b8;
  background-color: #ffffff;
  border: #ffffff;
  border-width: 1px;
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
}

.btn-search:hover {
  color: #ffffff;
  background-color: #e0e0e0;
  border: #e0e0e0;
  border-width: 1px;
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
}

.card-list{
  padding-top: 20px;
}

.card1{
  margin-top: 10px;
  max-width: 20rem;
  min-width: 15rem;
  width: 15rem;
  min-height: 25rem;
  max-height: 25rem;
}

.card-card_header {

}

</style>
