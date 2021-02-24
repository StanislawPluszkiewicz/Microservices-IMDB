<template>
<b-container v-if="!loading">
  <div class="movie-detail">
    <div class="header">
      <b-modal hide-footer ref="modal-loading" title="Sending comment...">
        <div style="padding: 15px; text-align:center;"><img src="src/assets/spinner.gif" width="50px" height="50px"/></div>
      </b-modal>
      <b-row>
        <h1><b>{{ movie.title }}</b></h1>
      </b-row>
      <b-row>
        <h3 v-if="movie.type === 'Movie'">{{ movie.type }} | {{ movie.date }}</h3> 
        <h3 v-else>
          <p v-if="movie.seasons > 1">{{ movie.type }} {{ movie.seasons }} seasons | {{ movie.date }}</p>
          <p v-else>{{ movie.type }} {{ movie.seasons }} season | {{ movie.date }}</p>
        </h3> 
      </b-row>
    </div>
    <div class="body">
        <div id="main">
            <div class="player">
              <b-embed
                type="iframe"
                aspect="16by9"
                :src="movie.trailer"
                allowfullscreen>
              </b-embed>
            </div>
            <div class="tags">
              <b-container>
                <b-row>
                  <b-col :style="{width: computeSizeTag(tag) +'px'}" class="tag" v-for="(tag, index) in movie.genres" :key='`tag-${index}`' cols="1">
                    {{tag}}
                  </b-col>
                </b-row>
              </b-container>
            </div>
            <div class="desc">
              <h3><b>Synopsis from the community</b></h3>
              <b-list-group>
                <b-list-group-item v-for="(desc, index) in movie.description" :key='`tag-${index}`'>{{desc}}</b-list-group-item>
              </b-list-group>
            </div>
        </div>
        <div id="cast_list">
          <h3><b>Cast</b></h3>
          <b-container>
                <b-row>
                  <b-col class="cast_unit" v-for="(cast, index) in movie.cast" :key='`tag-${index}`' cols="5">
                    <b-container>
                      <b-row>
                        <b-col>
                          <div class="circular--portrait"><img :src=cast.image></div>
                        </b-col>
                        <b-col>
                          <b-container>
                            <b-row>
                              <h5>{{cast.name}}</h5>
                            </b-row>
                            <b-row v-if="cast.role">
                              <b-col style="padding: 0px 0px 0px 0px;" v-for="(role, index) in cast.role" :key='`tag-${index}`'>
                                <p v-if="role != null && role != '...'">{{role}}</p>
                              </b-col>
                            </b-row>
                            <b-row v-if="cast.nb_episodes != null && cast.nb_episodes!= ''">
                              <h6>{{cast.nb_episodes}} episodes</h6>
                            </b-row>
                            <b-row v-if="cast.date != null && cast.date != ''">
                              <h6>{{cast.date}}</h6>
                            </b-row>
                          </b-container>
                        </b-col>
                      </b-row>
                    </b-container>
                  </b-col>
              </b-row>
          </b-container>
        </div>
        <div>
          <div id="comments">
            <h3><b>Comments</b></h3>
            <div v-if="this.$parent.isConnected === true" class="comment-editor">
              <b-container>
                <b-row>
                  <h4>Add a new comment</h4>
                </b-row>
                <b-row>
                  <b-form-textarea
                    v-model=content
                    placeholder="Enter something..."
                    rows="6"
                    max-rows="6"
                    style="margin-bottom: 1%;"
                  ></b-form-textarea>
                </b-row>
                <b-row>
                  <b-col cols="5" style="padding: 0px 0px 0px 0px;">
                    <div class="rating">
                      <star-rating v-model="rating"></star-rating>
                      <div><a href="#" @click.prevent="rating = 0"><i>Reset Rating</i></a></div>
                    </div>
                  </b-col>
                  <b-col cols="6" style="padding: 0px 0px 0px 0px;"/>
                  <b-col cols="1" style="padding: 0px 0px 0px 0px;" align-v="center">
                    <b-button class="mmdb-btn comment-btn" align-self="end" @click="sendComment()">Add</b-button>
                  </b-col>
                </b-row>
              </b-container>
            </div>
            <div v-if="this.$parent.isConnected === false" class="comment-editor">
              <b-container>
                <b-row>
                  <h4>You must be connected to add a new comment.</h4>
                </b-row>
              </b-container>
            </div>
            <div class="comment-list">
              <b-container v-if="movie.comments.length > 0">
                <b-row>
                  <h4>See the comments</h4>
                </b-row>
                <b-row class="comment" v-for="(comment, index) in movie.comments" :key='`tag-${index}`'>
                  <b-container>
                    <b-row class="comment-header">
                      <b-col cols="1" style="padding: 0px 0px 0px 0px;">
                        By {{comment.userName}}
                      </b-col>
                      <b-col cols="3" style="padding: 0px 0px 0px 0px;">
                        {{parseDate(comment.date)}}
                      </b-col>
                      <b-col cols="1" style="padding: 0px 0px 0px 0px;">
                        {{comment.note}}<v-icon style="color: gold;" name="star"/>
                      </b-col>
                    </b-row>
                    <b-row class="comment-review">
                      {{comment.review}}
                    </b-row>
                  </b-container>
                </b-row>
              </b-container>
              <b-container v-else>
                <b-row>
                  <h4>There aren't any comments for this {{ movie.type }} yet !</h4>
                </b-row>
              </b-container>
            </div>
          </div>
        </div>
    </div>
  </div>
</b-container>
<div v-else>
  <img src="src/assets/spinner.gif" width="50px" height="50px"/>
  <p style="padding-top:20px">Our little Billys are trying hard to get this movie's informations !</p>
  <p>It'll be ready in a few seconds !</p>
</div>
</template>
<script>
  import {StarRating} from 'vue-rate-it';

  export default {
    name: 'Movie',
    components: {
        StarRating
    },
    data: function() {
      return {
        movie: {
          id: '',
          title: '',
          description: '',
          type: '',
          genres: '',
          trailer: '',
          date:'',
          cast:'',
          seasons:'',
          comments: []
        },
        content: '',
        rating: 0,
        loading: false,
        
      }
    },
    created: function() {
      this.fetchData()
    },
    mounted: function()
    {
      
    },

    watch: {
      '$route': 'fetchData'
    },

    methods: {
      //Own
      replaceSpaceByPlus: function(str)
      {
        str = str.replace(/ /g,"+")
        return str
      },
      computeSizeTag: function(tag)
      {
        //console.log(tag.length * 12)
        return tag.length * 12
      },
      getTrailer: function() {
        var yt_api = {
          baseUrl: 'https://www.googleapis.com/youtube/v3/search?',
          part: 'snippet',
          type: 'video',
          order: 'relevance',
          maxResults: 1,
          q: '',
          key: 'AIzaSyD4Rq20JXkApRJ4Z-kuG2cCiNn2tVmOie8',
        }
        var search = this.movie.title.replace(/ /g,"+")

        console.dir(search)
        console.log(`${yt_api.baseUrl}part=${yt_api.part}&type=${yt_api.type}&order=${yt_api.order}&q=${search}+trailer&maxResults=${yt_api.maxResults}&key=${yt_api.key}`)

        this.$axios
          .get(`${yt_api.baseUrl}part=${yt_api.part}&type=${yt_api.type}&order=${yt_api.order}&q=${search}+trailer&maxResults=${yt_api.maxResults}&key=${yt_api.key}`)
          .then(res => {
            this.movie.trailer = 'https://www.youtube.com/embed/'+res.data.items[0].id.videoId+'?width=200px'
            console.log(res.data.items)
          })
          .catch(error => console.log(error));
      },
      sendComment : function()
      {
        var that = this
        console.log("len: " + this.content.length)
        if(this.content.length > 0)
        {
          this.$refs['modal-loading'].show()
          var formated_content = this.content.replace("\""," ")
          
          var bodyFormData = new FormData()
          bodyFormData.append('movieID', this.movie.id)
          bodyFormData.append('userID', this.$parent.user.userId)
          bodyFormData.append('comment', formated_content)
          bodyFormData.append('note', this.rating)

          console.log(bodyFormData)

          this.$axios
            .post('http://127.0.0.1:5005/comments', bodyFormData, {'Content-Type': 'multipart/form-data' })
            .then(res => {
              console.log(res)
              this.$bvToast.toast('Comment added', {
                title: 'Success !',
                autoHideDelay: 5000
              })
              that.getComments()
            })
            .catch(error =>{
              console.log(error)
              if(error.response.status === 406)
              {
                this.$bvToast.toast('Username or password is incorrect. Please try again.', {
                  title: 'Wrong credentials',
                  autoHideDelay: 15000
                })
              }
              else if(error.response.status === 401)
              {
                this.$bvToast.toast('Unlucky', {
                  title: 'Session expired',
                  autoHideDelay: 15000
                })
              }
              else
              {
                this.$bvToast.toast('Please contact stanislaw.karol.pluszkiewicz@gmail.com for any inconvenience.', {
                  title: 'Somethin wrong happened.',
                  autoHideDelay: 15000
                })
              }
            }).finally( f => {
                this.$refs['modal-loading'].hide()
                that.content = ''
                that.rating = 0
            });
        }
        else
        {
          this.$bvToast.toast('Impossible to send a comment without any content.', {
                  title: 'Action Forbidden.',
                  autoHideDelay: 15000
                })
        }


        
      },
      RemoveEndDescription: function (description) {
        var regex = /\. -(.*)/
        return description.replace(regex, ".")
      },
      fetchData: function() {
        console.log("Id: " + this.$route.params.id)
        var that = this
        this.loading = true

        this.getComments()
        this.getMovieDetails()
      },
      parseDate: function (oldDate) {
        return oldDate.slice(4)
      },
      getComments: function() {
        var that = this

        this.$axios.get('http://127.0.0.1:5005/comments?movieID=' + this.$route.params.id)
          .then(res => {
            console.log(res)
            that.movie.comments = res.data.data.comments
          })
          .catch(error => console.log(error))
      },
      getMovieDetails: function(){
        var that = this

        this.$axios
          .get('http://127.0.0.1:5011/movie/' + this.$route.params.id + '/details')
          .then(res => {
            console.log(res)
            that.movie.id = res.data.data.id
            that.movie.title = res.data.data.title
            that.movie.description = res.data.data.description
            that.movie.genres = res.data.data.genres
            that.movie.date = res.data.data.date
            that.movie.cast = res.data.data.cast
            console.log("here")
            console.log(res.data.data.seasons)
            if(res.data.data.seasons == null || res.data.data.seasons === '')
            {
              that.movie.type = 'Movie'
            }
            else
            {
              that.movie.type = 'TV-Series'
              that.movie.seasons = res.data.data.seasons
            }
            
            this.getTrailer()
            //that.movie.comments = call comments of Gigi
            console.log(that.movie)
          })
          .catch(error => console.log(error))
          .finally(function(){
            that.loading = false
          });
      }
    }
  }
</script>
<style>
@import '../assets/style/mmdb-style.css';

.player{
  width: 80%;
}

.desc{
  margin-top: 3%;
  text-align: left;
}

.desc p{
  font-size: 20px;
}

.tag{
  margin: 10px;
  background-color: #FFFFFF;
  border-radius: 25px;
  border-color:#17a2b8 ;
  padding-left: 5px;
  padding-right: 5px;
}

.circular--portrait {
  position: relative;
  width: 150px;
  height: 150px;
  overflow: hidden;
  border-radius: 50%;
}

.circular--portrait img {
  width: 100%;
  height: auto;
}

#cast_list{
  text-align: left;
  margin-top: 3%;
}

.cast_unit{
  border: solid;
  border-radius: 10px;
  border-width: 1px;
  border-color: #17a2b8;
  background-color: #f7f7f7;
  margin: 15px 15px 15px 15px;
  padding: 10px 10px 10px 10px;
}

#comments
{
  text-align: left;
  margin-top: 3%;
}

.comment-editor{
  margin-top: 5%;
}

.comment-btn{
  width: 75px;
  margin-top: 2%;
  
}

.comment-list{
  margin-top: 5%;
}

.comment{
  margin-top: 3%;
  margin-bottom: 3%;
  border: solid 2px;
  border-color: #17a2b8;
}

.comment{
  padding: 20px;
  margin-top: 3%;
  margin-bottom: 3%;
  border: solid 2px;
  border-color: #17a2b8;
  border-radius: 10px;
  background-color: #f7f7f7;
}

.comment-header{
  padding-bottom: 2%;
}

.comment-review{
  text-align:left;
}

</style>