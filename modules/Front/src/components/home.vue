<template>
      <b-container v-if="!loading">
      <b-row>
        <h3>Movies List</h3>
      </b-row>
      <b-row class="card-list">
        <b-card-group deck>
          <b-col v-for="movie in movies_titles" :key='movie.id' cols="6" style="padding: 5px">
            <b-card no-body class="overflow-hidden" style="max-height: 325px; text-align:left;">
              <b-row no-gutters>
                <b-col md="6" >
                  <b-card-img :src="movie.image" :alt="movie.title" class="rounded-0"></b-card-img>
                </b-col>
                <b-col md="6">
                  <b-card-body :title="movie.title" style="height:270px">
                    <b-card-text>
                      {{movie.description}}
                    </b-card-text>
                  </b-card-body>
                  <b-card-footer align="center">
                  <b-button href="#" class="mmdb-btn" @click="$router.push('movie/' + movie.id)">See More</b-button>
                </b-card-footer>
                </b-col>
                
              </b-row>
            </b-card>
          </b-col>
        </b-card-group>
      </b-row>
      </b-container>
      <div v-else>
        <img src="src/assets/spinner.gif" width="50px" height="50px"/>
        <p style="padding-top:20px">Mining all the necessary data from russian data centers...</p>
        <p>It'll be ready in a few seconds !</p>
      </div>
</template>

<script>
  export default {
  name: "app",
  data() {
      return { 
        movies_titles: '',
        loading: false
      }
  },
  created: function() {
    this.getMovies()
  },
  computed: {
    movie() {
      return this.$route.params.movie
    },
    profile() {
      return this.$route.params.profile
    }
  },
  methods: {
      goBack: function () {
        window.history.length > 1 ? this.$router.go(-1) : this.$router.push('/')
      },
      TruncateDescription: function (description) {
          var limit = 170
          var returnValue = description
          var toTruncate = false
          if (description.length > limit)
          {

            var idLastSpace = -1
            for(var i = limit; i > 0; i--)
            {
              if(description.charAt(i) === " ")
              {
                idLastSpace = i
                break
              }
            }
            
            returnValue = description.slice(0, idLastSpace)
            toTruncate = true
          }
          var regex = /\. -(.*)/
          returnValue = returnValue.replace(regex, "")
          if(toTruncate)
            returnValue = returnValue + '...'
          return returnValue
      },
      getMovies(){
        var that = this
        this.loading = true

        if(this.$parent.search === '')
        {
          this.$axios
          .get('http://127.0.0.1:5011/movie/homepage')
          .then(res => {
            console.log(res)
            that.movies_titles = res.data.data
            that.movies_titles.forEach(e => {
              
              var new_desc = e.description[0]
              var trunc = that.TruncateDescription(new_desc)
              e.description = trunc
            });
          })
          .catch(error => console.log(error))
          .finally(function(){
            that.loading = false
          });
        }
        else
        {
          this.$axios
          .get(`http://127.0.0.1:5012/search/movie?name=${that.$parent.search}`)
          .then(res => {
            console.log(res)
            that.movies_titles = res.data.data
            that.movies_titles.forEach(e => {
              
              var new_desc = e.description[0]
              var trunc = that.TruncateDescription(new_desc)
              e.description = trunc
            });
          })
          .catch(error => console.log(error))
          .finally(function(){
            that.loading = false
            that.$parent.search = ''
          });
        }
        
      }
  }
};
</script>
<style>
  @import '../assets/style/mmdb-style.css';
  .card-list{
    padding-top: 20px;
  }

</style>