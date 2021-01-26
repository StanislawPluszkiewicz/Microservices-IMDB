<template>
  <div class="movie-detail">
    <div class="header">
      <b-row>
        <h1><b>{{ movie.title }}</b></h1>
      </b-row>
      <b-row>
        <h3>{{ movie.type }} | {{ movie.date.begin }}-{{ movie.date.end }}</h3> 
      </b-row>
    </div>
    <div class="body">
      <b-row>
        <div class="images">
          <b-col>
            <b-carousel
              id="carousel-1"
              v-model="slide"
              :interval="4000"
              controls
              indicators
              background="#ababab"
              img-width="1024"
              img-height="480"
              style="text-shadow: 1px 1px 2px #333;"
              @sliding-start="onSlideStart"
              @sliding-end="onSlideEnd">
              <div cols="2" v-for="(image, index) in movie.images" :key='`image-${index}`'>
                <b-carousel-slide :img-src="image"></b-carousel-slide>
              </div>  
            </b-carousel>
          </b-col>
        </div>
      </b-row>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'Movie',

    data() {
      return {
        movie: {}
      }
    },

    created() {
      this.fetchData()
    },

    watch: {
      '$route': 'fetchData'
    },

    methods: {
      fetchData() {
        console.log("Id: " + this.$route.params.id)

        var movies_titles = [
        {},
        {
          id: 1,
          title: 'Doctor Who',
          images: ['https://upload.wikimedia.org/wikipedia/en/0/05/Doctor_Who_-_Current_Titlecard.png','https://upload.wikimedia.org/wikipedia/commons/e/ef/The_Walking_Dead_2010_logo.svg','https://upload.wikimedia.org/wikipedia/fr/5/52/Logo_Lupin-Dans-l%27ombre-d%27Ars%C3%A8ne.jpg'],
          description: 'The further adventures in time and space of the alien adventurer known as the Doctor and their companions from planet Earth.',
          type: 'TV-Series',
          date: {
            begin:'2005',
            end:''
          },
          
        
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

        this.movie = movies_titles[this.$route.params.id]
      }
    }
  }
</script>